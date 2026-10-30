---
type: experiment
id: EXP-20260911-016
date: 2026-09-11
status: confirmed-bounded
created: 2026-09-11
updated: 2026-09-11
binary_sha256: f55c3612f60fb1fba373c55d8cab6afcac96cf00d4156c542963234aa58b7059
environment: Same owned muted Wine Gamescope hardware run; copied-state native rendering and collision
question: Is the grass at Flik a real boundary, and why does it persist farther than the custom walls?
result: Solid boundary has detailed primary meshes and a simplified quarter-coordinate distant representation; collision and near/distant draws corroborated
tags: [experiment/training, re/rendering, re/collision]
---

# Training grass boundary near and distant representations

**Confirmed:** Flik is against a real grass boundary. Its close appearance is
primary255/256, while secondary15 is the simplified distant representation of
the boundary. Calling it background without explaining this relationship was
misleading. **Both the distant geometry and its camera are quarter-scaled**,
so its projected world placement is retained; quarter camera translation alone
does not establish slower parallax or unrelated decorative scenery.

## Identity and current view

Same muted EXP013 game91321/start5734777/group91091. EXE SHA256
`f55c3612f60fb1fba373c55d8cab6afcac96cf00d4156c542963234aa58b7059`, Training DAT
`d5ed5105a41814ae7a0acfc1d25793eb589428494373dd98046a67542a995bcc`.
New read-only capture brackets identical Flik(-205749,-34847,50162), camera
(-178291,-47662,42081), matrix `5c040000640fefff001004009cf0eeff5c04`.
No gameplay keys, writes, suspension, launches, closes, settings or asset edits.

Original retail SHA256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Renderer spans are unchanged from retail. Native per-object projection gives
28 vertices for primary255 and49 for256; all77 complete32-byte vertices match
the captured live buffers. They cover the close green blades in the screenshot.
Secondary15 is admitted but emits0 vertices here. At the earlier two poses it
emits60/92, all matching the live buffers under [[EXP-20260911-015 - Training grass uses secondary background geometry]]. Conversely,
primary257/258 emit0 at the initial pose and fail distance admission farther away.
This demonstrates distinct near/distant draws, not a single mesh-pointer swap.

## Detailed and distant geometry

Primary255..261 are681 vertices/444 faces. Secondary15 has60 vertices/29 faces.
Every relevant staged origin/local coordinate is checked against the original
Training mapping. Secondary15's simplified bounds scaled by4 nearly reproduce
the detailed boundary's bounds:

| Axis | Detailed primary bounds | Distant bounds ×4 |
| --- | --- | --- |
| X | -7350..6849 | -7276..6768 |
| Y | -2236..-722 | -2220..-724 |
| Z | -7091..6445 | -7088..6440 |

Original0044D83D's secondary tail also divides the camera by4, and00448D70
renders the result. Shared far still participates in secondary admission;
this is not unlimited distance. The different clipping rules and simplified
representation let this boundary remain visible after its detailed portions
stop drawing. Custom walls291..315 have only primary meshes; the16 secondary
records remain the original set, with no custom-wall counterpart.

## Boundary collision

Flik's stored position is(-6429.65625,-1088.96875,1567.5625),9.60445 units inside
terrain source25 segment19, file offset47748. Endpoints are(-6291,2039) and
(-6609,1031). Native004AB1A0 copied-state queries collect the exact live segment
at008DFCE7. Two outward requests would cross it but return inside; an inward
request proceeds. All three use the current captured position/terrain. Flag257
occurs in both directions and is not by itself the blocking evidence.

A broad retail-equality check for collision code failed on existing relocated
pool-address operands. The final three cases restore captured resident `.text`
in the offline process, retaining those relocations, and reproduce the same
positions as the retail-code comparison. No live memory is written. Do not
extend the renderer's byte-equality claim to the collision coordinator.

## Scope and correction

[[EXP-20260911-015 - Training grass uses secondary background geometry]] identified the distant render record correctly but did not explain
its relationship to the physical boundary. It also omitted the matching scale
of the geometry. Its152 distant vertex matches remain valid. Earlier panorama
and13-primary-plant measurements describe other objects. The current evidence
supports the boundary's near/distant representation and collision at this pose,
not exact proxy topology, exhaustive transition quality or a measured wall fix.

`reports/render-distance/EXP-20260911-016.json` hashes private captures, geometry
comparison, three-view replay, collision cases and code checks. Assets stay
private. [[2026-09-11 - Codex - Confirm the solid grass boundary and distant representation]] owns validation and closure. Next: user feedback;
a custom-wall distant representation would be a separate implementation task.
