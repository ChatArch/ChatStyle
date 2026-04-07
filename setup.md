# Setup

Use this repository as the extraction target for reusable CLI-style code.

Suggested workflow:

1. Identify a generic helper in ChatTool.
2. Copy it here first.
3. Refine names and boundaries until it is reusable.
4. Verify downstream usage in a small consumer package.
5. Only after the flow is stable, consider decoupling ChatTool itself.
