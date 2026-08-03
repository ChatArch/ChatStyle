# ChatStyle Documentation

ChatStyle is ChatArch's reusable CLI interaction convention and runtime. It centralizes input schemas, missing-value prompts, `-i/-I`, TTY handling, secret safety, and flow output for Click CLIs. Downstream packages should depend on these public primitives instead of copying another interaction implementation.

## Choose By Scenario

| Goal | Entry |
| --- | --- |
| Add ChatStyle to a Click command for the first time | [Quickstart](quickstart.md) |
| Choose an input, terminal, output, or security module | [Modules](modules.md) |
| Align `-i/-I`, automatic prompting, and script behavior | [Interaction Conventions](conventions.md) |
| Understand high-level schema versus low-level resolver boundaries | [Interaction Runtime](interaction-runtime.md) |
| Change public APIs, tests, docs, or release workflows | [Development Guide](development.md) |
| Read the package design goals and trade-offs | [Design Draft](design.md) |

## Documentation Entries

<div class="grid cards" markdown>

- **Quick Integration**

    Follow installation, `CommandSchema`, Click options, and a minimal command as one reusable path.

    [Open Quickstart](quickstart.md)

- **Interaction Contract**

    Review automatic prompts, explicit `-i/-I`, non-TTY behavior, sensitive input, and automation rules.

    [Open Interaction Conventions](conventions.md)

- **Modules And Boundaries**

    Choose stable APIs across `input`, `tui`, `render`, `security`, `core`, and `patterns`.

    [Open Modules](modules.md)

- **Maintenance And Release**

    Review API stability, dependency boundaries, test matrices, MkDocs, and Trusted Publisher gates.

    [Open Development Guide](development.md)

</div>

## Runtime Boundaries

<div class="grid cards" markdown>

- **High-Level Command Inputs**

    `resolve_command_inputs()` owns defaults, equivalent validation, and recoverable missing-value prompts. Automatic mode honors `CHATARCH_AUTO_PROMPT=0/false/no/off`; explicit `-i` still wins.

- **Low-Level Interactive Resolver**

    `resolve_interactive_mode()` keeps environment handling opt-in so existing adapters can control confirmation flows without inheriting high-level automatic-prompt behavior unexpectedly.

- **Non-Interactive Automation**

    CI, scripts, and agents should pass `-I`. Missing required values fail fast, and machine output must not contain prompt chatter.

- **Secret Safety**

    Passwords, tokens, and secrets use sensitive prompts and masking helpers. Documentation, logs, and exceptions must never echo raw values.

</div>

## Minimal Schema

```python
from chatstyle import CommandField, CommandSchema

SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField(
            "path",
            prompt="output path",
            kind="path",
            default="./out.txt",
        ),
    ),
)
```

Build the documentation locally:

```bash
pip install -e ".[docs]"
mkdocs build --strict
```
