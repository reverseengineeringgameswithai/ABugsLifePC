---
type: environment
id: ENV-OBSIDIAN
status: active
updated: 2026-10-02
tags:
  - environment/obsidian
---

# Obsidian Setup

Obsidian 1.13.6 was downloaded as the official x86-64 AppImage into `~/Applications/`, with a user-local command and desktop URI handler. Because Fedora lacks FUSE 2, the AppImage payload is run from its official extracted form. No pre-existing `~/.config/obsidian` directory was overwritten.

The only vault is `~/ABLPC/Vault`. Stable vault settings enable ordinary Markdown, wikilinks, search, backlinks, graph, tags, bookmarks, and templates. No community plugin is installed. First-run UI confirmation and opening the vault remain human actions if the application has not previously run.

Update (2026-10-02 audit): the application has since run with this vault
open. Obsidian's own `obsidian.json` registers it, and the ignored
`.obsidian/workspace.json` was last written 2026-08-21. The committed
`.obsidian/core-plugins.json` also enables canvas, properties, outline, page
preview and bases. There is still no community plugin.
