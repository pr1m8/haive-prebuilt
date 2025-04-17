# src/haive/prebuilt/simple/query_rewriter.py
"""
Agent Name: QueryRewriter
Description: Improves or reformulates a user query to be clearer or more suitable for retrieval.
"""

from langchain_core.prompts import ChatPromptTemplate
from haive_core.models.llm.base import AzureLLMConfig
from haive_core.aug_llm import AugLLMConfig
from haive_prebuilt.simple.query.models import QueryModel
from pydantic import BaseModel, Field
from haive_agents.simple.factory import create_simple_agent

SYSTEM_PROMPT = """
You are a query rewriting assistant.
Rewrite the query to improve clarity, precision, and search effectiveness while preserving the original intent.
"""

query_rewriter_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Query: {query}")
])

class RewrittenQuery(BaseModel):
    rewritten: str = Field(..., description="A clearer or improved version of the original query.")

query_rewriter_config = AugLLMConfig(
    name="query_rewriter",
    llm_config=AzureLLMConfig(),
    prompt_template=query_rewriter_prompt,
    structured_output_model=RewrittenQuery,
)

query_rewriter = create_simple_agent(
    engine=query_rewriter_config,
    name="query_rewriter"
)
