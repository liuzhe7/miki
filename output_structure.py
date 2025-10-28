from dataclasses import dataclass


# We use a dataclass here, but Pydantic models are also supported.
@dataclass
class ResponseFormat:
    """Response schema for the agent."""

    # AI response message
    msg: str
