# Static Anthill inventory

EXP-20260926-001 compares the pinned original PC Anthill DAT/RAW with the
explicit donor footprints of the Moonlit authoring library. It also compares
original geometry with scene references in the base and saved production DAT.
It never executes native code, opens Blender or changes compiler inputs.

Run from the repository using a **fresh output directory** under `work/`:

```bash
.venv/bin/python research/anthill-inventory/census.py --out work/experiments/EXP-20260926-001/repeat
.venv/bin/python research/anthill-inventory/gallery.py work/experiments/EXP-20260926-001/repeat
PYTHONPATH=reimplementation .venv/bin/python -m pytest -q tests/test_anthill_inventory.py
```

The defaults bind the September 26 leaf-flat source/export and September 16
production path. Changed Blender source/export bindings reject. Alternate
production DAT copies may be selected with `--production-dat`; their hashes
are recorded. Donor coverage is a reviewed, explicit mapping, not automatic
semantic recognition of every authored mesh. Counts will need review when the
library grows. The original DAT/RAW/EXE hashes are enforced.

`census.json` contains metadata suitable for a research report. `artwork.json`,
page PNGs, previews and `index.html` contain derived artwork and must remain
private under `work/`. The committed report contains no decoded mesh/texture
payload. `appearance-labels.json` records human-reviewed appearance inferences;
these labels are not authoritative game object names or behavior claims.

The negative-count mesh view follows the original PC header instructions at
0045A82E..0045A8B4, retains the unknown auxiliary span in its immutable source
and records its extent/hash. Its temporary positive mesh is for inspection
only. This is not production support for the negative format.

The gallery uses two double-sided orthographic local views with stored UVs,
texture colours and approximate vertex colour modulation. It omits instance
rotation/scale, animation, native material/lighting behavior and collision.
Rasterization is diagnostic, not a claim of native render equivalence.

Accepted results: `work/experiments/EXP-20260926-001/verified/` and
`reports/anthill-inventory/EXP-20260926-001.json`. Earlier folders are exploratory:
`census-01` omitted texture page3; later provisional runs used an incorrect
unscaled selector offset. Geometry and preview surfaces were unaffected, but
their selector labels are superseded. The final reader uses +19 for unscaled
objects and +25 for scaled objects, with synthetic layout regressions.
