from typing import Literal

from pydantic import BaseModel, Field


class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the repor.",
    )
    description: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this sectio.",
    )
    research: bool = Field(
        description="Whether to perform web research for this section of the repor."
    )
    content: str = Field(description="The content of the sectio.")


class Sections(BaseModel):
    sections: list[Section] = Field(
        description="Sections of the repor.",
    )


class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query for web searc.")


class Queries(BaseModel):
    queries: list[SearchQuery] = Field(
        description="List of search querie.",
    )


class Feedback(BaseModel):
    grade: Literal["pas", "fai"] = Field(
        description="Evaluation result indicating whether the response meets requirements ('pas') or needs revision ('fai')."
    )
    follow_up_queries: list[SearchQuery] = Field(
        descriptio="List of follow-up search queries.",
    )
