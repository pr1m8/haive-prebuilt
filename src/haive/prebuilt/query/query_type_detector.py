# src/haive/prebuilt/simple/query_type_detector.py
"""Agent Name: QueryTypeDetector.
Description: Labels the query as boolean, open-ended, multi-hop, numerical, or instruction.
"""

from haive.agents.simple.factory import create_simple_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """
You are a query type detector.
Categorize the query into one of the following types:
- boolean
- open-ended
- multi-hop
- numerical
- instruction
Only return the most appropriate label.
"""

query_type_detector_prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("user", "Query: {query}")]
)


class QueryType(BaseModel):
    type: str = Field(
        ...,
        description="The query type label, such as boolean, multi-hop, or numerical.",
    )


query_type_detector_config = AugLLMConfig(
    name="query_type_detector",
    llm_config=AzureLLMConfig(),
    prompt_template=query_type_detector_prompt,
    structured_output_model=QueryType,
)

query_type_detector = create_simple_agent(
    engine=query_type_detector_config, name="query_type_detector"
)
