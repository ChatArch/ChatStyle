from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class InteractiveResolution:
    interactive: bool | None
    can_prompt: bool
    force_interactive: bool
    need_prompt: bool


def is_interactive_available() -> bool:
    return os.isatty(0) and os.isatty(1)


def resolve_interactive_mode(
    interactive: bool | None,
    *,
    auto_prompt_condition: bool,
) -> InteractiveResolution:
    can_prompt = is_interactive_available()
    force_interactive = interactive is True
    need_prompt = force_interactive or (
        interactive is None and auto_prompt_condition and can_prompt
    )
    return InteractiveResolution(
        interactive=interactive,
        can_prompt=can_prompt,
        force_interactive=force_interactive,
        need_prompt=need_prompt,
    )
