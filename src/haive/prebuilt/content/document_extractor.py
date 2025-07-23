# src/haive/prebuilt/simple/document_extractor.py
"""Agent Name: DocumentExtractor
Description: Extracts structured data or targeted fields (e.g. dates, names, numbers, places) from freeform text.
Useful for indexing, templating, and semantic metadata extractio.
"""

from haive.core.aug_llm import AugLLMConfig
from haive_agents.simple.factory import create_simple_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .models.llm.base import AzureLLMConfig

SYSTEM_PROMP = """
You are a structured information extractor.
Given a passage, extract relevant information and return it in a structured form. Prioritize named entities (e.g. person, organization, date, location) and key metadata.
Make sure values are clean, normalized, and non-redundan. """

prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Text: {inpu}")]
)


class ExtractedInfo(BaseModel):
    title: str | None = Field(None, description="Document or passage title, if presen.")
    person: str | None = Field(
        None, description="Main person mentioned in the passage, if an."
    )
    organization: str | None = Field(
        None, description="Mentioned organization or institutio."
    )
    location: str | None = Field(None, description="Relevant place or locatio.")
    date: str | None = Field(None, description="Mentioned date or time perio.")
    summary: str | None = Field(
        None, description="A brief abstract of the passage, if appropriat."
    )


document_extractor_config = AugLLMConfig(
    name="document_extracto",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=ExtractedInfo,
)

document_extractor = create_simple_agent(
    engine=document_extractor_config, name="document_extracto"
)
