#!/usr/bin/env bash
set -u
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
REPORT="$ROOT/reports/doctor.txt"
STATUS="$ROOT/Vault/00-System/Environment Status.md"
mkdir -p "$ROOT/reports"
tmp=$(mktemp)
base=$(mktemp)
trap 'rm -f "$tmp" "$base"' EXIT

version_line() {
    local name=$1; shift
    if command -v "$1" >/dev/null 2>&1; then
        printf '%-18s %s\n' "$name" "$("$@" 2>&1 | head -n 1)"
    else
        printf '%-18s not installed\n' "$name"
    fi
}
{
    echo "ABLPC doctor"
    echo "Generated: $(date --iso-8601=seconds)"
    echo
    . /etc/os-release
    printf '%-18s %s\n' "Fedora" "$PRETTY_NAME"
    printf '%-18s %s\n' "Kernel" "$(uname -r)"
    printf '%-18s %s\n' "Architecture" "$(uname -m)"
    if grep -Eqm1 '\b(vmx|svm)\b' /proc/cpuinfo; then
        printf '%-18s %s\n' "CPU virtualization" "available"
    else
        printf '%-18s %s\n' "CPU virtualization" "not detected"
    fi
    if test -r /dev/kvm -a -w /dev/kvm; then
        printf '%-18s %s\n' "KVM" "/dev/kvm accessible"
    else
        printf '%-18s %s\n' "KVM" "not accessible"
    fi
    version_line "Python" python3 --version
    version_line "Java" java -version
    version_line "Wine" wine --version
    if command -v gamescope >/dev/null 2>&1; then
        gamescope_package=$(rpm -q gamescope 2>/dev/null || true)
        printf '%-18s %s\n' "Gamescope" "${gamescope_package:-installed; package version unavailable}"
    else
        printf '%-18s not installed\n' "Gamescope"
    fi
    version_line "QEMU" qemu-system-x86_64 --version
    version_line "libvirt" virsh --version
    version_line "virt-manager" virt-manager --version
    version_line "virt-install" virt-install --version
    version_line "radare2" radare2 -v
    version_line "Git" git --version
    version_line "strace" strace --version
    version_line "GDB" gdb --version
    version_line "rr" rr --version
    version_line "apitrace" apitrace version
    printf '%-18s %s\n' "perf_event_paranoid" "$(cat /proc/sys/kernel/perf_event_paranoid 2>/dev/null || echo unknown) (rr needs <=1)"
    printf '%-18s %s\n' "ptrace_scope" "$(cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null || echo unknown)"
    version_line "ripgrep" rg --version
    version_line "fzf" fzf --version
    version_line "Codex" codex --version
    version_line "Claude" claude --version
    if test -x "$ROOT/tools/jdk/current/bin/java"; then
        printf '%-18s %s\n' "Ghidra JDK" "$("$ROOT/tools/jdk/current/bin/java" -version 2>&1 | head -n 1)"
    else
        printf '%-18s not installed\n' "Ghidra JDK"
    fi
    if test -x "$ROOT/tools/ghidra/current/ghidraRun"; then
        prop="$ROOT/tools/ghidra/current/Ghidra/application.properties"
        ver=$(sed -n 's/^application.version=//p' "$prop" 2>/dev/null | head -n 1)
        printf '%-18s %s\n' "Ghidra" "${ver:-installed; version unavailable}"
    else
        printf '%-18s not installed\n' "Ghidra"
    fi
    if test -x "$ROOT/tools/ghidra/.venv/bin/python"; then
        pyghidra_version=$("$ROOT/tools/ghidra/.venv/bin/python" -c 'import importlib.metadata; print(importlib.metadata.version("pyghidra"))' 2>/dev/null)
        printf '%-18s %s\n' "PyGhidra" "${pyghidra_version:-installed; version unavailable}"
    else
        printf '%-18s not installed\n' "PyGhidra"
    fi
    box="$ROOT/tools/86box/86Box-Linux-x86_64-b9001.AppImage"
    if test -x "$box"; then
        printf '%-18s %s\n' "86Box" "6.0 build 9001 (project-local)"
    else
        printf '%-18s not installed\n' "86Box"
    fi
    if command -v pcem >/dev/null 2>&1; then
        printf '%-18s %s\n' "PCem" "$(command -v pcem)"
    else
        printf '%-18s not installed\n' "PCem"
    fi
    if command -v obsidian >/dev/null 2>&1; then
        printf '%-18s %s\n' "Obsidian" "1.13.6 (official extracted AppImage payload)"
    else
        printf '%-18s not installed\n' "Obsidian"
    fi
    if test -x "$ROOT/.venv/bin/python"; then
        printf '%-18s %s\n' "Python venv" "$("$ROOT/.venv/bin/python" --version 2>&1)"
    else
        printf '%-18s not installed\n' "Python venv"
    fi
    printf '%-18s %s\n' "virtqemud socket" "$(systemctl is-active virtqemud.socket 2>/dev/null || true)"
    if virsh -c qemu:///system uri >/dev/null 2>&1; then
        printf '%-18s %s\n' "libvirt system" "reachable"
    else
        printf '%-18s %s\n' "libvirt system" "unreachable"
    fi
    if virsh -c qemu:///system net-info default >/dev/null 2>&1; then
        netstate=$(virsh -c qemu:///system net-info default 2>/dev/null | awk '/^Active:/{print $2}')
        printf '%-18s %s\n' "default network" "$netstate"
    else
        printf '%-18s %s\n' "default network" "not defined"
    fi
} > "$tmp"
cp "$tmp" "$REPORT"
awk '
    /<!-- BEGIN GENERATED: doctor -->/ {skip=1; next}
    /<!-- END GENERATED: doctor -->/ {skip=0; next}
    !skip {lines[++count]=$0}
    END {
        while (count > 0 && lines[count] == "") count--
        for (line = 1; line <= count; line++) print lines[line]
    }
' "$STATUS" > "$base"
cat "$base" > "$STATUS"
{
    echo
    echo "<!-- BEGIN GENERATED: doctor -->"
    echo
    echo '```text'
    cat "$tmp"
    echo '```'
    echo
    echo "<!-- END GENERATED: doctor -->"
} >> "$STATUS"
cat "$REPORT"
