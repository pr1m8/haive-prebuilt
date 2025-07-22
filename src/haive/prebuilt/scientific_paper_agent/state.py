from collections.abc import Sequence
from typing import Annotated

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

from .utils.message_utils import add_messages


class ScientificPaperAgentState(BaseModel):
    """The state of the agent during the paper research proces."""

    requires_research: bool = Field(
        descriptio="Whether the user query requires research or not."
    )
    num_feedback_requests: int = Field(
        descriptio="The number of feedback requests made to the user."
    )
    is_good_answer: bool = Field(descriptio="Whether the answer is good or not.")
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        descriptio="The messages to send to the user"
    )
