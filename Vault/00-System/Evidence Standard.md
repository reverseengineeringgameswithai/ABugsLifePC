---
type: policy
status: active
updated: 2026-08-11
tags:
  - research/evidence
---

# Evidence Standard

A significant claim must cite at least one concrete locator:

- executable SHA-256 and virtual address;
- file SHA-256 and byte offset;
- static export path and symbol/reference;
- experiment ID;
- runtime run ID and artifact path;
- debugger observation with environment and configuration.

For important conclusions, seek two independent evidence forms. Correlated output from the same tool is not necessarily independent.

## Confidence language

**Confirmed** means the stated behavior was directly demonstrated. **Inferred** means evidence supports an interpretation while alternatives remain. **Unknown** means evidence is absent or nondiscriminating.

Screenshots and prose are supporting context, not substitutes for reproducible artifacts. Decompiler pseudocode must retain its address and binary identity. Negative results must state exactly what was tested.
