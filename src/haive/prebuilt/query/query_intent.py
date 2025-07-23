# Additional simple agents

# src/haive/prebuilt/simple/query_intent_classifier.py
"""Agent Name: QueryIntentClassifier
Description: Classifies the intent behind a query, such as definition, comparison, fact-checking, opinion, et.
"""
from haive.core.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .models.llm.base import AzureLLMConfig

SYSTEM_PROMP = """
You are a query intent classifier.
Determine the user's intent from the query and output it as a descriptive label (e.g. fact-checking, comparison, explanation, definition, opinion, hypothetical).
Also give a confidence score.
"""

prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Query: {quer}")]
)


class QueryIntent(BaseModel):
    intent: str = Field(..., description="The classified intent behind the quer.")
    confidence: float = Field(..., description="The confidence score for the inten.")


query_intent_classifier_config = AugLLMConfig(
    name="query_intent_classifie",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=QueryIntent,
)
