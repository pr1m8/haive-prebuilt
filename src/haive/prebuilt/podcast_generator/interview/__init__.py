"""Interview - TODO: Add brief description

TODO: Add detailed description of module functionality


Key Components:
    * Classes: InterviewState


Example:
    Basic usage::

        from haive.interview import InterviewState

        instance = InterviewState()
        # TODO: Complete example


"""

# https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/generate_podcast_agent_langgraph.ipynb

import operator
from typing import Annotated

from haive.core.schema.prebuilt.messages_state import MessagesState


class InterviewState(MessagesState):
    topic: str  # Topic of the podcast
    max_num_turns: int  # Number turns of conversation
    context: Annotated[list, operator.add]  # Source docs
    section: str  # section transcript
    sections: list  # Final key we duplicate in outer state for Send() API
