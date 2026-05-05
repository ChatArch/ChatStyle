# Modules

ChatStyle is split into input declaration, interactive policy, prompts, output display, secret masking, and flow display. Modules stay generic and do not include ChatTool business logic.

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

- `render_heading()` for common headings.
- `render_note()` for low-emphasis notes.
- `render_status()` for business-neutral info/success/warning/error status lines.
- `render_suggested_commands()` for commands users may run manually, without executing them.
- `render_priority_chain()` for config or resolution priority chains.

Rich is optional. Click fallback is required. Output helpers only render; they do not parse business errors or execute commands.

## Mask And Sensitive Input

Module:

- `chatstyle.mask`

Purpose:

- Mask tokens, passwords, API keys, app secrets, and webhook secrets.
- Format current secret hints.
- Prompt for sensitive values while allowing empty input to keep the current value.

## Flow Display

Modules:

- `chatstyle.flow`
- `chatstyle.setup`

Purpose:

- `render_flow_start()` for starting a multi-step CLI flow.
- `render_stage()` for the current stage.
- `render_success()` / `render_warning()` / `render_failure()` for generic results.
- `render_commands()` for commands users may run manually.
- `render_priority_chain()` for config-source or resolution priority.

`flow` does not install dependencies, execute system commands, call remote APIs, check environments, or write configuration. `setup` remains a setup-scenario compatibility wrapper backed by generic `flow` / `output` helpers.
