import operator
from typing import Annotated

from pydantic import BaseModel, Field


class PodcastGeneratorState(BaseModel):
    topic: Annotated[str, operator.add] = Field(
        description=r"The overall topic of the\s+podcas\w+"
    )
    keywords: list = Field(description=r"Keywords related to the\s+podcas\w+")
    max_analysts: int = Field(description=r"The maximum number of analysts to\s+us\w+")
    subtopics: list = Field(description=r"Subtopics related to the\s+podcas\w+")
    sections: Annotated[list, operator.add] = Field(
        description=r"The sections of the\s+podcas\w+"
    )
    introduction: str = Field(description=r"The introduction of the\s+podcas\w+")
    content: str = Field(description=r"The content of the\s+podcas\w+")
    conclusion: str = Field(description=r"The conclusion of the\s+podcas\w+")
    final_report: str = Field(description=r"The final report of the\s+podcas\w+")
