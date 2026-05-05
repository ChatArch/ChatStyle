"""Reusable CLI style and interaction helpers."""

from .choice import create_choice, get_separator
from .click import add_interactive_option
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
    InteractiveResolution,
    is_interactive_available,
    normalize_interactive,
    resolve_interactive_mode,
)
from .mask import format_current_secret, mask_secret, prompt_sensitive_value
from .output import get_style
from .prompt import (
    ask_checkbox,
    ask_checkbox_with_controls,
    ask_confirm,
    ask_path,
    ask_select,
    ask_text,
)
from .resolve import resolve_command_inputs
from .schema import CommandConstraint, CommandField, CommandSchema
from .setup import (
    setup_config_priority,
    setup_failure,
    setup_stage,
    setup_start,
    setup_success,
    setup_suggested_commands,
    setup_warning,
)

__all__ = [
    "BACK_VALUE",
    "CHECKBOX_SELECTED_INDICATOR",
    "CHECKBOX_UNSELECTED_INDICATOR",
    "CommandConstraint",
    "CommandField",
    "CommandSchema",
    "FORCE_INTERACTIVE_NO_TTY_MESSAGE",
    "InteractiveResolution",
    "INTERACTIVE_OPTION_HELP",
    "MISSING_REQUIRED_NO_TTY_MESSAGE",
    "add_interactive_option",
    "abort_if_force_without_tty",
    "abort_if_missing_without_tty",
    "ask_checkbox",
    "ask_checkbox_with_controls",
    "ask_confirm",
    "ask_path",
    "ask_select",
    "ask_text",
    "create_choice",
    "format_current_secret",
    "get_separator",
    "get_style",
    "is_interactive_available",
    "mask_secret",
    "normalize_interactive",
    "prompt_sensitive_value",
    "resolve_command_inputs",
    "resolve_interactive_mode",
    "setup_config_priority",
    "setup_failure",
    "setup_stage",
    "setup_start",
    "setup_success",
    "setup_suggested_commands",
    "setup_warning",
    "__version__",
]

__version__ = "0.1.0"
