# Development Guide

## Goal

ChatStyle is an independent CLI interaction runtime. Implementations should stay generic, lightweight, testable, and reusable by Click CLI projects beyond ChatTool.

## Module Boundary

- Generic interaction helpers live under `src/chatstyle/`.
- Product-specific commands, business semantics, and third-party API parsing must not enter ChatStyle.
- `CommandSchema` runtime is core: field declaration, prompting, validation, and interactive policy.
- prompt/output/flow/mask helpers handle presentation, not business decisions.

## Dependency Strategy

- `click` is the core dependency.
- `questionary`, `prompt_toolkit`, and `rich` stay optional and are imported lazily.
- Add hard dependencies only when they are required by the runtime contract.

## API Design

- `chatstyle.__init__` exports stable user-facing APIs only.
- Underscore helpers may support compatibility layers, but are not long-term public contracts.
- Prefer simple parameter types over project-specific objects.
- Errors should remain readable and actionable in CLI output.
- New APIs should be reusable by multiple Click CLIs; helpers that serve one product command do not belong in ChatStyle.

## Interaction Rules

- `-i` forces the current command's interactive flow; `-I` disables prompts for scripts and CI.
- Recoverable missing arguments go through `CommandSchema`; do not mark those Click options as `required=True`.
- Non-TTY environments must not block on input.
- Sensitive fields must hide input and mask displayed values.
- Prompt copy should stay short, clear, and business-neutral.

## Testing

- Runtime behavior belongs in `tests/`.
- New public APIs require tests.
- Prompt fallback, masking, CommandSchema resolution, and Click integration are critical coverage areas.
- Tests around optional dependencies should remain stable when those dependencies are absent.

## Documentation

- README provides the short introduction and minimal example.
- Chinese is the default documentation language; English mirror files use the `.en.md` suffix and are built under `/en/` by `mkdocs-static-i18n`.
- `docs/index.md` is the Chinese entrypoint and `docs/index.en.md` is the English entrypoint.
- `docs/modules.md` explains module responsibilities.
- `docs/conventions.md` explains interaction conventions.
- `docs/development.md` explains maintenance rules.
- `docs/interaction-runtime.en.md` explains runtime boundaries and downstream usage.
- Public behavior changes require README, docs, and CHANGELOG updates.

## Workflows

- CI should run tests, package build, and mkdocs build.
- Docs deploy uses mkdocs GitHub Pages.
- PR preview uses mike to deploy a dev preview.
- Workflows that write to gh-pages must configure git identity:
  - `github-actions[bot]`
  - `41898282+github-actions[bot]@users.noreply.github.com`

## Release

- Keep version `0.1.0` before the first formal release.
- Before release, verify README badges, pyproject metadata, CHANGELOG, and tag version alignment.
