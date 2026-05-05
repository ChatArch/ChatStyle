# ChatStyle Docs

ChatStyle is a reusable CLI interaction style and runtime package for Click CLIs that need consistent prompts, missing-argument recovery, `-i/-I`, TTY handling, secret masking, and setup-stage display.

## Core Modules

- `chatstyle.prompt`
- `chatstyle.choice`
- `chatstyle.output`
- `chatstyle.mask`
- `chatstyle.setup`
- `chatstyle.schema`
- `chatstyle.resolve`
- `chatstyle.click`
- `chatstyle.interactive`
- `chatstyle.errors`

## CommandSchema

`CommandSchema` is a core ChatStyle feature. It declares CLI fields and centralizes defaults, missing-argument prompting, validation, and interactive policy.

```python
from chatstyle import CommandField, CommandSchema

SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField("path", prompt="output path", kind="path", default="./out.txt"),
    ),
)
```

## Local Preview

```bash
pip install -e ".[docs]"
mkdocs serve
```
