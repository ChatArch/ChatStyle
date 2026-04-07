# chatstyle

Reusable CLI interaction and scaffold helpers extracted from ChatTool practices.

Current goal:

- collect reusable CLI interaction rules
- package common prompt / masking / interactive-mode helpers
- provide a light runtime that future `cli-style` scaffolds can depend on

This repository is currently an extraction target. At this stage, code may be copied
from ChatTool first, then refined here before any upstream decoupling happens.

## Layout

- `src/`: reusable runtime code
- `tests/`: lightweight package tests
- `docs/`: long-lived package notes
- `.github/workflows/`: CI and publish automation skeleton

## Local Checks

```bash
python -m pytest -q
python -m build
```
