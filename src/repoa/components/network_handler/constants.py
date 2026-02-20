"""Special node constants for network execution."""

from typing import Literal

# Special node identifiers
START: Literal["__start__"] = "__start__"
"""Special node representing the entry point of the workflow network."""

END: Literal["__end__"] = "__end__"
"""Special node representing the exit point of the workflow network."""

# Network execution constants
MAX_ITERATIONS = 1000
"""Maximum iterations to prevent infinite loops."""

TIMEOUT_DEFAULT = 300
"""Default timeout in seconds."""
