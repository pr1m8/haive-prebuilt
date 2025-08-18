# Additional simple agents

# src/haive/prebuilt/simple/query_intent_classifier.py
"""Agent Name: QueryIntentClassifier.
Description: Classifies the intent behind a query, such as definition, comparison, fact-checking, opinion, etc.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

SYSTEM_PROMPT = """
You are a query intent classifier.
Determine the user's intent from the query and output it as a descriptive label (e.g. fact-checking, comparison, explanation, definition, opinion, hypothetical).
Also give a confidence score.
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("user", "Query: {query}")]
)


class QueryIntent(BaseModel):
    intent: str = Field(..., description="The classified intent behind the query.")
    confidence: float = Field(..., description="The confidence score for the intent.")


query_intent_classifier_config = AugLLMConfig(
    name="query_intent_classifier",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=QueryIntent,
)
