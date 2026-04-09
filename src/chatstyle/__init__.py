"""chatstyle reusable CLI helpers."""

from .click import add_interactive_option
from .errors import abort_if_force_without_tty, abort_if_missing_without_tty
from .interactive import (
    InteractiveResolution,
    is_interactive_available,
    normalize_interactive,
    resolve_interactive_mode,
)
from .mask import mask_secret
from .prompt import ask_confirm, ask_path, ask_select, ask_text
from .resolve import resolve_command_inputs
from .schema import CommandConstraint, CommandField, CommandSchema

__all__ = [
    "CommandConstraint",
    "CommandField",
    "CommandSchema",
    "InteractiveResolution",
    "add_interactive_option",
    "abort_if_force_without_tty",
    "abort_if_missing_without_tty",
    "ask_confirm",
    "ask_path",
    "ask_select",
    "ask_text",
    "is_interactive_available",
    "mask_secret",
    "normalize_interactive",
    "resolve_command_inputs",
    "resolve_interactive_mode",
    "__version__",
]

__version__ = "0.1.0"
