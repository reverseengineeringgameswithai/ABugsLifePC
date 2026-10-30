# Bounded evidence packets

AI research must use bounded questions, not "reverse engineer the entire game."

A packet has this shape:

```text
research/tasks/TASK-level-reader-001/
|-- question.md
|-- decompiler/
|-- callers.txt
|-- callees.txt
|-- strings.txt
|-- imports.txt
|-- runtime/
|-- hexdumps/
`-- result.md
```

`question.md` must identify the binary SHA-256, addresses or offsets in scope, available evidence, exclusions, and the exact discriminating question. Preserve raw artifacts; put interpretation in `result.md`.

Example prompt:

```text
Determine whether function 0x00418A20 reads a record count and
allocates a corresponding array.

Separate:
- confirmed facts,
- inferences,
- unknowns.

Cite each claim using an address, offset, run ID, or experiment ID.

Suggest the smallest runtime experiment that distinguishes the
leading interpretations.
```

The result must state contradictions and missing evidence. A task is complete when it answers the bounded question or identifies the smallest evidence needed to do so.
