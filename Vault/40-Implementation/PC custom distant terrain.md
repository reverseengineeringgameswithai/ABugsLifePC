---
type: implementation
status: implemented
created: 2026-09-11
updated: 2026-10-29
evidence: [EXP-20260911-017]
tags: [implementation/modding, re/rendering]
---

# PC custom distant terrain

EXP-20260911-017 generates simpler distant (secondary) versions of authored
floors, walls and supported opaque rock surfaces, and owns the bounded
native/hardware evidence. [[PC custom distant objects]] (EXP-20260911-018)
extends the approach to placed mesh objects. The figures below describe the
terrain-only EXP017 baseline, which excludes foliage.

## Geometry and depth

The EXP017 writer partitions whole unrefined lit faces into8192-unit regions.
Selected tags60/61/160 retain material, UV, colour and unknown vertex bytes;
other decoration commands are omitted. Quantizing absolute coordinates to
quarters before choosing local origins keeps shared corners consistent, with
at most2 original stored units of coordinate error. Native secondary camera
quartering then preserves projected placement. Existing detail and collision
remain exact. This is authored near/distant geometry, not runtime decimation.

The PC initializer copies256 visibility bytes at0044BB70. Secondary traversal
reads from005BA23F backwards at0044D430. New bits are enabled only after every
original grid transition is checked not to own them. Primary and original
secondary records retain their geometry; only necessary pointer relocations and
three unused mask bytes change in the old DAT. A -1 footer's potentially shared
mesh terminator is retained before a new footer. Original Anthill and Training
native loader tests cover both footer cases.

The unmodified distant hardware depth is unsuitable for new terrain at2x:
at world depth12000 it emits Z0.57373047 versus primary0.732421875. An overlapping
far copy could overwrite nearer geometry. The EXP017 depth patch marks only the
new unscaled secondary objects (object+18 word00D1, zero animation selector). The00448FB1 wrapper marks
its private hardware mesh-call argument;21 native x87 depth sites apply
`Z_new = Z_original_secondary / 32 + 27/32` only for that argument. Ordinary
geometry uses the exact original multiplication. New distant depth is ordered
behind the2x primary cutoff while retaining ordering among distant surfaces.
No writable global flag or new PE section is needed. The132-byte PIC helper
uses guarded padding at004BC200;21 displaced HIGHLOW relocations are retired.
The patch proves exact inverse and operates at both tested PE bases.

## Validation boundary

A fixed-camera hardware comparison shows distant terrain that the control lacks.
Near geometry/depth parity, representative near/distant overlap, 19 resident
meshes, code bytes and new visibility bits pass. Exhaustive transitions,
all camera angles, all original secondary-scene overlaps, native Windows,
software rendering and other resolutions remain open.
