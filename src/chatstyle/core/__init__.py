"""Core constants, interactive policy, and shared errors."""

from .constants import (
    BACK_VALUE,
    CHECKBOX_SELECTED_INDICATOR,
    CHECKBOX_UNSELECTED_INDICATOR,
    FORCE_INTERACTIVE_NO_TTY_MESSAGE,
    INTERACTIVE_OPTION_HELP,
    MISSING_REQUIRED_NO_TTY_MESSAGE,
)
from .errors import abort_if_force_without_tty, abort_if_missing_without_tty
from .interactive import (
    AUTO_PROMPT_ENV_VAR,
    InteractiveResolution,
    auto_prompt_enabled,
    is_interactive_available,
    normalize_interactive,
    resolve_interactive_mode,
)

__all__ = [
    "BACK_VALUE",
    "AUTO_PROMPT_ENV_VAR",
    "CHECKBOX_SELECTED_INDICATOR",
    "CHECKBOX_UNSELECTED_INDICATOR",
    "FORCE_INTERACTIVE_NO_TTY_MESSAGE",
    "INTERACTIVE_OPTION_HELP",
    "InteractiveResolution",
    "MISSING_REQUIRED_NO_TTY_MESSAGE",
    "abort_if_force_without_tty",
    "abort_if_missing_without_tty",
    "auto_prompt_enabled",
    "is_interactive_available",
    "normalize_interactive",
    "resolve_interactive_mode",
]
