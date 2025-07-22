import operator
from typing import Annotated

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field

from .utils.message_utils import reduce_messages


class AgentState(BaseModel):
    messages: Annotated[list[AnyMessage], reduce_messages] = Field(
        description=r"The messages to send to the\s+use\w+"
    )
    systematic_review_outline: str = Field(
        description=r"The systematic review\s+outlin\w+"
    )
    last_human_index: int = Field(description=r"The last human\s+inde\w+")
    papers: Annotated[list[str], operator.add] = Field(
        description=r"The papers\s+downloade\w+"
    )
    analyses: Annotated[list[dict], operator.add] = Field(
        description=r"The analysis\s+result\w+"
    )
    combined_analysis: str = Field(description=r"The final combined\s+analysi\w+")

    title: str = Field(description=r"The title of the systematic\s+revie\w+")
    abstract: str = Field(description=r"The abstract of the systematic\s+revie\w+")
    introduction: str = Field(
        description=r"The introduction of the systematic\s+revie\w+"
    )
    methods: str = Field(description=r"The methods of the systematic\s+revie\w+")
    results: str = Field(description=r"The results of the systematic\s+revie\w+")
    conclusion: str = Field(description=r"The conclusion of the systematic\s+revie\w+")
    references: str = Field(description=r"The references of the systematic\s+revie\w+")

    draft: str = Field(description=r"The draft of the systematic\s+revie\w+")
    revision_num: int = Field(
        description=r"The revision number of the systematic\s+revie\w+"
    )
    max_revisions: int = Field(
        description=r"The maximum number of revisions of the systematic\s+revie\w+"
    )
