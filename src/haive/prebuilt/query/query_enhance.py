# src/haive/prebuilt/simple/query_enhancer.py
"""Agent Name: QueryEnhancer
Description: Enriches a query by adding relevant context, assumptions, or metadata.
Useful for boosting reasoning or LLM effectiveness.
"""

from haive.agents.simple.factory import create_simple_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """
You are a semantic enhancer.
Given a query, enrich it by adding relevant implicit information, assumptions, and metadata to make it more complete and self-contained.
"""

query_enhancer_prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("user", "Query: {query}")]
)


class EnhancedQuery(BaseModel):
    enriched_query: str = Field(
        ...,
        description="The enriched version of the query with added implicit information or assumptions.",
    )


query_enhancer_config = AugLLMConfig(
    name="query_enhancer",
    llm_config=AzureLLMConfig(),
    prompt_template=query_enhancer_prompt,
    structured_output_model=EnhancedQuery,
)

query_enhancer = create_simple_agent(
    engine=query_enhancer_config, name="query_enhancer"
)
