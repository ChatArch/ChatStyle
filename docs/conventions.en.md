# Interaction Conventions

This document defines the interaction rules ChatStyle must preserve as a foundational ChatArch CLI runtime.

## Interactive Mode

ChatStyle uses a tri-state interactive model:

- `interactive is True`: force interactive mode, from `-i` or `--interactive`.
- `interactive is False`: disable prompts, from `-I` or `--no-interactive`.
- `interactive is None`: automatic mode; prompt only when recoverable values are missing and a TTY is available.

Rules:

- `-i` enters only the current command's interactive flow.
- `-I` must keep scripts and CI from blocking on prompts.
- Non-TTY environments must not auto-prompt.
- Forced interactive mode without TTY must use the shared no-TTY error.

## Missing Arguments

Use `CommandSchema` for recoverable arguments:

```python
from chatstyle import CommandField, CommandSchema

SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField("output", prompt="output path", kind="path", default="./out.txt"),
    ),
)
```

Rules:

- Do not mark recoverable Click options as `required=True`; Click would stop before the callback.
- Defaults should come from `default` or `default_factory` and match prompt display.
- Use `prompt_if_missing=True` when a cached value exists but the user should confirm or refresh it.
- Field validation belongs in `validator`.
- Cross-field validation belongs in `CommandConstraint`.

## Prompt Types

Field-to-prompt mapping:

- `text`: `ask_text()`
- `path`: `ask_path()`
- `select`: `ask_select()`
- `confirm`: `ask_confirm()`
- `int`: collect text/default first, then cast to `int`
- `float`: collect text/default first, then cast to `float`

Rules:

- Prompt copy should be short, clear, and business-neutral.
- Select/checkbox choices should be readable and carry machine values separately.
- Empty choices should not become business exceptions; return an empty result or `BACK_VALUE` for the caller to handle.
- User cancellation should become a Click abort.

## Secrets

Secrets include tokens, passwords, API keys, app secrets, and webhook secrets.

Rules:

- Use `password=True` or `prompt_sensitive_value()` for input.
- Always use `mask_secret()` for display.
- Display existing values as `current: <masked>`.
- If empty input keeps the old value, the prompt must say `enter to keep` or equivalent.
- Never write raw secrets to logs, exceptions, or summaries.

## Output And Setup

Rules:

- Use `chatstyle.output` for common headings and notes.
- Use `chatstyle.setup` for setup-stage display.
- Setup flows should distinguish start, stage, success, warning, and failure.
- For sudo or high-risk commands, print suggested commands by default instead of executing them.
- Config source priority should be clear in setup output or docs.

## Automation Compatibility

Interactive features must remain automation-friendly:

- Explicit arguments should fully express intent.
- `-I` should disable prompting.
- Non-TTY errors should fail fast.
- Errors should include the missing field or usage for automation debugging.
