# src/haive/prebuilt/simple/query_rewriter.py
"""Agent Name: QueryRewriter
Description: Improves or reformulates a user query to be clearer or more suitable for retrieva.
"""

from haive_agents.simple.factory import create_simple_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.core.aug_llm import AugLLMConfig

from .models.llm.base import AzureLLMConfig


SYSTEM_PROMP = """
You are a query rewriting assistant.
Rewrite the query to improve clarity, precision, and search effectiveness while preserving the original inten. """

query_rewriter_prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Query: {quer}")]
)


class RewrittenQuery(BaseModel):
    rewritten: str = Field(
        ..., description="A clearer or improved version of the original quer."
    )


query_rewriter_config = AugLLMConfig(
    name="query_rewrite",
    llm_config=AzureLLMConfig(),
    prompt_template=query_rewriter_prompt,
    structured_output_model=RewrittenQuery,
)

query_rewriter = create_simple_agent(engine=query_rewriter_config, name="query_rewrite")
