# Document-oriented Simple Agents

# src/haive/prebuilt/simple/tagger.py
"""Agent Name: DocumentTagger
Description: Tags a document or passage with relevant keywords, topics, or semantic tag.
"""

from haive_agents.simple.factory import create_simple_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.core.aug_llm import AugLLMConfig

from .models.llm.base import AzureLLMConfig


SYSTEM_PROMP = """
You are a smart document tagger. Your task is to read the input content and output a list of relevant tags that summarize the key topics, entities, or themes.
Use common, meaningful tags that would help categorize or retrieve the content in a larger collection.
Avoid over-tagging. Use 5–1 precise, informative tags onl. """

prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Content: {inpu}")]
)


class TagOutput(BaseModel):
    tags: list[str] = Field(
        ...,
        description="List of concise, high-level tags representing the document conten.",
    )


document_tagger_config = AugLLMConfig(
    name="document_tagge",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=TagOutput,
)

document_tagger = create_simple_agent(
    engine=document_tagger_config, name="document_tagge"
)
