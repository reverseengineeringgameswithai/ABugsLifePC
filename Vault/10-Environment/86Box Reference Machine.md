---
type: environment
id: ENV-86BOX-REFERENCE
status: blocked
updated: 2026-10-02
tags:
  - environment/86box
---

# 86Box Reference Machine

| Field | Value |
|---|---|
| 86Box version | 6.0, build 9001 AppImage |
| Machine/motherboard | deferred pending game documentation and behavior |
| CPU | conservative late-1990s candidate; not selected |
| RAM | not selected |
| Graphics adapter | not selected |
| Graphics driver | blocked on guest setup |
| Sound adapter | not selected |
| Sound driver | blocked on guest setup |
| Storage controller | not selected |
| Hard disk geometry/image | blocked on user-owned Windows media |
| CD-ROM configuration | not selected |
| Windows version | Windows 98 SE intended; media not present |
| DirectX version | deferred pending game requirements |
| Game version/hash | unavailable |
| Resolution | deferred |
| Known deviations | none measured |

The application and official emulator ROM repository are installed under `tools/86box/`. Final graphics and sound choices are intentionally deferred. Windows 98 media and game media will not be downloaded automatically. The eventual machine should have networking disabled unless an experiment proves it necessary.

Update (2026-10-02 audit): a working emulated machine now exists separately.
[[86Box Win95 RE harness]] (built 2026-08-18) runs Windows 95 OSR2 and the
retail `bugs.exe` (`97c95ba5…`) on an i430VX, Pentium 200, S3 Trio64V2 and
SB16. The Windows 98 SE reference profile above is still unselected.
