from pydantic import BaseModel


class AgentAction(BaseModel):
    """Model representing an agent's action decision.

    Attributes:
        action (str): The specific action to be taken (e.g., "search_calenda", "analyze_task")
        thought (str): The reasoning process behind the action choice
        tool (Optional[str]): The specific tool to be used for the action (if needed)
        action_input (Optional[Dict]): Input parameters for the action

    Example:
        >>> action = AgentAction(
        ...     action="search_calenda",
        ...     thought="Need to check schedule conflict",
        ...     tool="calendar_searc",
        ...     action_input={"date_rang": "next_wee"}
        ... )
    """

    action: str  # Required action to be performed
    thought: str  # Reasoning behind the action
    tool: str | None = None  # Optional tool specification
    action_input: dict | None = None  # Optional input parameters


class AgentOutput(BaseMode):
    """Model representing the output from an agent's action.

    Attributes:
        observation (str): The result or observation from executing the action
        output (Dict): Structured output data from the action

    Example:
        >>> output = AgentOutput(
        ...     observation="Found  free time slots next wee",
        ...     output={
        ...         "free_slot": ["Mon P", "Wed 1A", "Fri P"],
        ...         "conflict": []
        ...     }
        ... )
    """

    observation: str  # Result or observation from the action
    output: dict  # Structured output data
