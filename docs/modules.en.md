# Modules

ChatStyle is split into input declaration, interactive policy, prompts, output display, secret masking, and setup display. Modules stay generic and do not include ChatTool business logic.

## Command Schema Runtime

Modules:

- `chatstyle.schema`
- `chatstyle.resolve`
- `chatstyle.click`

Purpose:

- Describe CLI fields with `CommandField`.
- Group command input with `CommandSchema`.
- Express cross-field validation with `CommandConstraint`.
- Merge explicit arguments, defaults, interactive prompts, and validation with `resolve_command_inputs()`.
- Attach `--interactive/--no-interactive` and `-i/-I` to Click commands with `add_interactive_option()`.

Use it when a CLI command has recoverable missing arguments, defaults that must match prompt display, field validators, or cross-field constraints.

## Interactive Policy

Modules:

- `chatstyle.interactive`
- `chatstyle.errors`
- `chatstyle.constants`

Purpose:

- Detect TTY availability.
- Normalize Click default interactive parameters.
- Decide whether prompting is needed.
- Provide shared `-i/-I` copy and no-TTY error messages.

## Prompt And Choice

Modules:

- `chatstyle.prompt`
- `chatstyle.choice`

Purpose:

- `ask_text()` for text input.
- `ask_path()` for path input.
- `ask_confirm()` for confirmation.
- `ask_select()` for single selection.
- `ask_checkbox()` for multiple selection.
- `ask_checkbox_with_controls()` for checkbox selection with a select-all control.
- `create_choice()` and `get_separator()` for reusable choices and separators.

`questionary` and `prompt_toolkit` are imported lazily. Click fallback keeps the package usable without optional TUI dependencies.

## Output Style

Module:

- `chatstyle.output`

Purpose:

- Render headings.
- Render notes.
- Provide future common status, summary, table, and key-value display helpers.

Rich is optional. Click fallback is required.

## Mask And Sensitive Input

Module:

- `chatstyle.mask`

Purpose:

- Mask tokens, passwords, API keys, app secrets, and webhook secrets.
- Format current secret hints.
- Prompt for sensitive values while allowing empty input to keep the current value.

## Setup Display

Module:

- `chatstyle.setup`

Purpose:

- Display setup start, stage, success, warning, and failure messages.
- Print commands users should run manually.
- Display config source priority.

This module does not install dependencies, check environments, or write configuration.
