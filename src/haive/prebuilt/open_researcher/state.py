import operator
from typing import Annotated

from pydantic import BaseModel, Field

from .open_researcher.models import SearchQuery, Section


class ReportStateInput(BaseModel):
    topic: str = Field(description=r"Report\s+topi\w+")


class ReportStateOutput(BaseModel):
    final_report: str = Field(description=r"Final\s+repor\w+")


class ReportState(BaseModel):
    topic: str = Field(description=r"Report\s+topi\w+")
    feedback_on_report_plan: str = Field(description=r"Feedback on the report\s+pla\w+")
    sections: list[Section] = Field(description=r"List of report\s+section\w+")
    completed_sections: Annotated[list, operator.add] = Field(
        description=r"Send() API\s+ke\w+"
    )
    report_sections_from_research: str = Field(
        description=r"String of any completed sections from research to write final\s+section\w+"
    )
    final_report: str = Field(description=r"Final\s+repor\w+")


class SectionState(BaseModel):
    topic: str = Field(description=r"Report\s+topi\w+")
    section: Section = Field(description=r"Report\s+sectio\w+")
    search_iterations: int = Field(description=r"Number of search iterations\s+don\w+")
    search_queries: list[SearchQuery] = Field(description=r"List of search\s+querie\w+")
    source_str: str = Field(
        description=r"String of formatted source content from web\s+searc\w+"
    )
    report_sections_from_research: str = Field(
        description=r"String of any completed sections from research to write final\s+section\w+"
    )
    completed_sections: list[Section] = Field(
        description=r"Final key we duplicate in outer state for Send()\s+AP\w+"
    )


class SectionOutputState(BaseModel):
    completed_sections: list[Section] = Field(
        description=r"Final key we duplicate in outer state for\s+Sen\w+"
    )
