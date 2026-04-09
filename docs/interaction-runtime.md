# Interaction Runtime

`chatstyle` currently extracts the most reusable part of the ChatTool CLI interaction model while staying generic and dependency-light.

## Module Boundaries

- `chatstyle.interactive`
  - TTY availability checks
  - interactive mode normalization
  - auto-prompt decision rules for `None` / `True` / `False`
- `chatstyle.errors`
  - shared Click-facing abort and error helpers
- `chatstyle.mask`
  - secret masking utilities
- `chatstyle.schema`
  - declarative field and constraint objects
- `chatstyle.resolve`
  - shared input completion and validation flow
- `chatstyle.click`
  - Click integration helpers such as `add_interactive_option()`
- `chatstyle.prompt`
  - minimal prompt primitives for text, path, confirm, and select

## Current Scope

The runtime is intentionally scoped to Click-based CLIs.

This means:

- resolver errors use `click.ClickException`
- option wiring is provided for Click commands
- parameter source normalization currently depends on Click context

## Deliberate Non-Goals

The following are intentionally left outside `chatstyle` for now:

- product-specific page flow and copywriting
- complex checkbox controls and advanced TUI widgets
- Rich-based presentation choices that are mainly UX polish
- business helpers tied to one application or repository

## Dependency Strategy

- `click` is a core dependency for the current extraction stage
- `questionary` remains optional and only improves `ask_select()` when installed
- more advanced TUI dependencies should stay optional unless a clear reusable contract emerges

## Recommended Downstream Usage

1. Define command input shape with `CommandSchema`
2. Keep Click options recoverable with `required=False`
3. Add `@add_interactive_option`
4. Call `resolve_command_inputs()` once in the command callback
5. Keep business logic outside the resolver and prompt layer
