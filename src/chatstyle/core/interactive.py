from __future__ import annotations

from dataclasses import dataclass
import os

import click


AUTO_PROMPT_ENV_VAR = "CHATARCH_AUTO_PROMPT"
_FALSE_ENV_VALUES = frozenset({"0", "false", "no", "off"})


def auto_prompt_enabled() -> bool:
    """Return whether automatic prompts are enabled for the current process."""

    value = os.getenv(AUTO_PROMPT_ENV_VAR)
    if value is None:
        return True
    return value.strip().lower() not in _FALSE_ENV_VALUES


@dataclass
class InteractiveResolution:
    interactive: bool | None
    can_prompt: bool
    force_interactive: bool
    need_prompt: bool


def is_interactive_available() -> bool:
    return os.isatty(0) and os.isatty(1)


def normalize_interactive(interactive: bool | None) -> bool | None:
    ctx = click.get_current_context(silent=True)
    if ctx:
        try:
            source = ctx.get_parameter_source("interactive")
            if source == click.core.ParameterSource.DEFAULT:
                return None
        except Exception:
            pass
    return interactive


def resolve_interactive_mode(
    interactive: bool | None,
    *,
    auto_prompt_condition: bool,
    respect_auto_prompt_env: bool = False,
) -> InteractiveResolution:
    interactive = normalize_interactive(interactive)
    can_prompt = is_interactive_available()
    force_interactive = interactive is True
    automatic_prompt_allowed = (
        auto_prompt_enabled() if respect_auto_prompt_env else True
    )
    need_prompt = force_interactive or (
        interactive is None
        and auto_prompt_condition
        and automatic_prompt_allowed
        and can_prompt
    )
    return InteractiveResolution(
        interactive=interactive,
        can_prompt=can_prompt,
        force_interactive=force_interactive,
        need_prompt=need_prompt,
    )
