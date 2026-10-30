"""Bounded PC LEVEL.RAW packets, independently modeled from 0049A200.

EXP-20260908-020 compares 169 decoded packets against the original PC routine.
Only edited packets are re-encoded. The six opaque header bytes and the complete
terminator suffix are retained; their semantics are deliberately unspecified.
"""
import struct

MAX_PACKET = 4 * 1024 * 1024
MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 64 * 1024 * 1024


def decode(packet):
    if not isinstance(packet, bytes) or len(packet) < 15:
        raise ValueError('RAW packet header truncated')
    expected, packed = struct.unpack_from('>II', packet)
    if not 0 < expected <= MAX_PACKET or packed != len(packet)-14:
        raise ValueError('RAW packet extent invalid')
    cursor = 14; control = 0; bits = 0; output = bytearray()

    def byte():
        nonlocal cursor
        if cursor >= len(packet):
            raise ValueError('RAW bitstream truncated')
        value = packet[cursor]; cursor += 1
        return value

    def bit():
        nonlocal control, bits
        if not bits:
            control = byte(); bits = 8
        bits -= 1
        return (control >> bits) & 1

    def number(count):
        value = 0
        for _ in range(count): value = value*2 + bit()
        return value

    def literals(count):
        if len(output)+count > expected:
            raise ValueError('RAW output overrun')
        for _ in range(count): output.append(byte())

    number(2)
    while True:
        if not bit():
            literals(1); continue
        short = False; high = 0
        if bit():
            if not bit(): length = 2; short = True
            elif not bit(): length = 3
            else:
                length = byte()
                if not length:
                    if not bit(): break
                    continue
                length += 8
        else:
            first = bit(); length = 4+first
            if bit():
                length = (first+3)*2+bit()
                if length == 9:
                    literals((number(4)+3)*4); continue
        if not short and bit():
            high = bit()
            if not bit():
                if not high: high = 2+bit()
            else:
                high = 4+high*2+bit()
                if not bit(): high = high*2+bit()
        distance = (high << 8)+byte()+1
        if distance > len(output) or len(output)+length > expected:
            raise ValueError('RAW invalid backreference')
        for _ in range(length): output.append(output[-distance])
    if len(output) != expected:
        raise ValueError('RAW decoded size mismatch')
    return bytes(output)


def literal_packet(raw, header):
    """Emit a native-compatible literal stream; do not invent opaque fields."""
    if not isinstance(raw, bytes) or not 0 < len(raw) <= MAX_PACKET:
        raise ValueError('RAW replacement size invalid')
    if not isinstance(header, bytes) or len(header) < 14:
        raise ValueError('RAW replacement header truncated')
    data = bytearray(); control = 0; bits = 0

    def bit(value):
        nonlocal control, bits
        if not bits:
            control = len(data); data.append(0); bits = 8
        bits -= 1; data[control] |= value << bits

    bit(0); bit(0)
    for value in raw: bit(0); data.append(value)
    for _ in range(4): bit(1)
    data.append(0); bit(0)
    return struct.pack('>II', len(raw), len(data))+header[8:14]+data


def packets(raw):
    """Return (offset, original packet, decoded payload) rows and exact suffix."""
    if not isinstance(raw, bytes) or not 4 <= len(raw) <= MAX_FILE:
        raise ValueError('RAW file extent invalid')
    cursor = 0; total = 0; rows = []
    while True:
        if cursor+4 > len(raw): raise ValueError('RAW missing terminator')
        if raw[cursor:cursor+4] == b'\xff'*4:
            # 00465030 tests only the first dword. PC Level03 has a nine-byte
            # suffix, unlike Anthill's twelve; retain all remaining bytes.
            return rows, raw[cursor:]
        if len(rows) >= 512: raise ValueError('RAW packet count exceeded')
        if cursor+14 > len(raw): raise ValueError('RAW header truncated')
        count, packed = struct.unpack_from('>II', raw, cursor)
        total += count
        if total > MAX_TOTAL: raise ValueError('RAW aggregate output budget exceeded')
        if packed < 1 or cursor+14+packed > len(raw):
            raise ValueError('RAW packet truncated')
        packet = raw[cursor:cursor+14+packed]
        rows.append((cursor, packet, decode(packet)))
        cursor += 14+packed
