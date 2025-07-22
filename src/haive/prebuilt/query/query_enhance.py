# src/haive/prebuilt/simple/query_enhancer.py
"""Agent Name: QueryEnhancer
Description: Enriches a query by adding relevant context, assumptions, or metadata.
Useful for boosting reasoning or LLM effectivenes.
"""

from haive_agents.simple.factory import create_simple_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.core.aug_llm import AugLLMConfig

from .models.llm.base import AzureLLMConfig


SYSTEM_PROMP = """
You are a semantic enhancer.
Given a query, enrich it by adding relevant implicit information, assumptions, and metadata to make it more complete and self-containe. """

query_enhancer_prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Query: {quer}")]
)


class EnhancedQuery(BaseModel):
    enriched_query: str = Field(
        ...,
        description="The enriched version of the query with added implicit information or assumption.",
    )


query_enhancer_config = AugLLMConfig(
    name="query_enhance",
    llm_config=AzureLLMConfig(),
    prompt_template=query_enhancer_prompt,
    structured_output_model=EnhancedQuery,
)

query_enhancer = create_simple_agent(engine=query_enhancer_config, name="query_enhance")
