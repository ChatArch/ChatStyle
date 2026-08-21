# Modules

ChatStyle is split into input declaration, terminal interaction, output display, sensitive-value handling, core policy, and reusable patterns. Modules stay generic and do not include ChatTool business logic.

## `chatstyle.input`

Owns CLI input declaration, resolution, and Click integration:

- `CommandField`: describes one CLI field, including `required`, `default`, `kind`, validators, and more.
- `CommandSchema`: groups one command input contract.
- `CommandConstraint`: expresses cross-field constraints.
- `resolve_command_inputs()`: merges explicit arguments, defaults, interactive prompts, and validation.
- `add_interactive_option()`: attaches `--interactive/--no-interactive` and `-i/-I` to Click commands.
- `render_click_tree()`: renders a command tree from registered Click command/group metadata, including parameter signatures by default.
- `add_tree_option()`: attaches standard `--tree` and `--tree-brief` flags; brief mode omits parameter signatures and keeps nodes plus descriptions.

Semantic rules:

- A field with no default that is needed to run the command should be `required=True`.
- A field with a default may still be `required=True`; this means a missing explicit value should enter prompt mode when TTY auto mode is available, using the default as the prompt default.
- In non-TTY or `-I` mode, fields with defaults can use defaults directly; required fields without defaults fail fast.

## `chatstyle.tui`

Owns terminal input primitives:

- `ask_text()` for text input.
- `ask_path()` for path input.
- `ask_confirm()` for confirmation.
- `ask_select()` for single selection.
- `ask_checkbox()` for multiple selection.
- `ask_checkbox_with_controls()` for checkbox selection with a select-all control.
- `create_choice()` / `get_separator()` for reusable choices and separators.

`questionary` and `prompt_toolkit` are imported lazily. Click fallback keeps the package usable without optional TUI dependencies.

## `chatstyle.render`

Owns business-neutral output and flow display:

- `render_heading()` / `render_note()` for headings and low-emphasis notes.
- `render_status()` plus `render_info()` / `render_success()` / `render_warning()` / `render_error()` for status output.
- `render_suggested_commands()` for commands users may run manually, without executing them.
- `render_priority_chain()` for config or resolution priority chains.
- `render_key_values()` / `render_summary()` for stable key-value summaries.
- `render_list()` / `render_table()` for generic lists and plain-text tables.
- `render_flow_start()` / `render_stage()` / `render_plan()` / `render_dry_run()` for multi-step flows.
- `render_config_priority()` / `render_config_sources()` for config priority and source summaries.

Setup-like needs are composed from generic `render` helpers, not a separate core module.

## `chatstyle.security`

Owns sensitive-value handling:

- `mask_secret()` masks secrets.
- `format_current_secret()` formats `current: ****` hints.
- `prompt_sensitive_value()` prompts for a secret while allowing empty input to keep the current value.

Use it for tokens, passwords, API keys, app secrets, webhook secrets, and similar values.

## `chatstyle.core`

Owns low-level policy, constants, and errors:

- TTY detection.
- Tri-state interactive resolution.
- Shared `-i/-I` copy.
- No-TTY error messages.
- `BACK_VALUE` and checkbox indicators.
- Click-friendly error helpers.

## `chatstyle.patterns`

Owns cross-module recipes:

- `resolve_value()` chooses the first usable value by priority.
- `prompt_text_value()` prompts for text when a value is missing, with fallback support.
- `prompt_sensitive_value_with_mask()` prompts for a sensitive value with a custom mask display.
