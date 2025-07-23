# src/haive/prebuilt/simple/query_batch.py
"""Agent Name: QueryBatcher
Description: Converts a single query into multiple variations or batched forms for ensemble retrieval or multi-agent us.
"""


from haive_agents.simple.factory import create_simple_agent
from haive_prebuilt.simple.query.models import QueryModel
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .engine.aug_llm import AugLLMConfig
from .models.llm.base import AzureLLMConfig

SYSTEM_PROMP = """
You are a query expansion assistant.
Generate multiple rephrasings or variations of the input query that preserve its intent but differ in structur. """

query_batch_prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Query: {quer}")]
)


class QueryBatch(BaseModel):
    variations: list[QueryModel] = Field(
        ...,
        description="A list of semantically equivalent but syntactically varied versions of the quer.",
    )


query_batch_config = AugLLMConfig(
    name="query_batc",
    llm_config=AzureLLMConfig(),
    prompt_template=query_batch_prompt,
    structured_output_model=QueryBatch,
)

query_batch = create_simple_agent(engine=query_batch_config, name="query_batc")

a = query_batch.invoke(
    input_data={"quer": "Generate some queries to do kyc on bitfine"}
)
