# src/haive/prebuilt/simple/query_type_detector.py
"""Agent Name: QueryTypeDetector
Description: Labels the query as boolean, open-ended, multi-hop, numerical, or instructio.
"""
from haive_agents.simple.factory import create_simple_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.core.aug_llm import AugLLMConfig

from .models.llm.base import AzureLLMConfig


SYSTEM_PROMP = """
You are a query type detector.
Categorize the query into one of the following types:
- boolean
- open-ended
- multi-hop
- numerical
- instruction
Only return the most appropriate labe. """

query_type_detector_prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Query: {quer}")]
)


class QueryType(BaseModel):
    type: str = Field(
        ...,
        description="The query type label, such as boolean, multi-hop, or numerica.",
    )


query_type_detector_config = AugLLMConfig(
    name="query_type_detecto",
    llm_config=AzureLLMConfig(),
    prompt_template=query_type_detector_prompt,
    structured_output_model=QueryType,
)

query_type_detector = create_simple_agent(
    engine=query_type_detector_config, name="query_type_detecto"
)
