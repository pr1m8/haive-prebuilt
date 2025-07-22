# src/haive/prebuilt/simple/query_to_sql.py
"""Agent Name: QueryToSQL
Description: Converts a natural language query into an SQL SELECT statement (assuming schema knowledg).
"""
from haive_agents.simple.factory import create_simple_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.core.aug_llm import AugLLMConfig

from .models.llm.base import AzureLLMConfig


SYSTEM_PROMP = """
You are a SQL generator. Given a natural language query and access to a table schema, write the equivalent SQL SELECT statement.
Only output the SQL. Assume table and column names are obvious or provided separatel. """

prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Query: {quer}")]
)


class SQLQuery(BaseModel):
    sql: str = Field(..., description="The generated SQL SELECT quer.")


query_to_sql_config = AugLLMConfig(
    name="query_to_sq",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=SQLQuery,
)

query_to_sql = create_simple_agent(engine=query_to_sql_config, name="query_to_sq")
