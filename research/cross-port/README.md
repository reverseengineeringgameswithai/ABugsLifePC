# Cross-port evidence packets

This directory contains ABLPC-authored, bounded comparison packets. It is not a mirror, checkout, symlink, submodule, or artifact cache for the PS1 project.

Each packet must contain:

```text
research/cross-port/XPORT-<topic>-NNN/
|-- question.md
|-- ps1-citations.md
|-- pc-evidence.md
|-- comparison.md
`-- result.md
```

Every PS1 citation records `SRC-PS1-ABL`, the full Git commit object, a repository-relative path, and an address/offset/line or artifact hash. Every PC claim cites the PC ISO or executable SHA-256 and a PC locator. Copy only the minimum text or measurement required for the comparison; never copy external binaries, assets, saves, dumps, images, databases, or whole notes.

PS1 evidence may create a PC hypothesis. Only PC evidence can confirm a PC claim. See `Vault/00-System/Cross-Port Evidence Policy.md`.
