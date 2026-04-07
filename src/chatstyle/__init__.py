"""chatstyle reusable CLI helpers."""

from .errors import abort_if_force_without_tty, abort_if_missing_without_tty
from .interactive import (
    InteractiveResolution,
    is_interactive_available,
    resolve_interactive_mode,
)
from .mask import mask_secret

__all__ = [
    "InteractiveResolution",
    "abort_if_force_without_tty",
    "abort_if_missing_without_tty",
    "is_interactive_available",
    "mask_secret",
    "resolve_interactive_mode",
    "__version__",
]

__version__ = "0.1.0"
