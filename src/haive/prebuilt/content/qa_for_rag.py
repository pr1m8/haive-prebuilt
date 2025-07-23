# src/haive/prebuilt/simple/qa_for_rag.py
"""Agent Name: QAForRAGGenerator
Description: Generates QA pairs from documents suitable for fine-tuning or retrieval-augmented generatio.
"""

from haive_agents.simple.factory import create_simple_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .engine.aug_llm import AugLLMConfig
from .models.llm.base import AzureLLMConfig

SYSTEM_PROMP = """
You are a question-answer pair generator for retrieval-augmented generation (RAG).
Your goal is to extract useful facts from the text and generate realistic, natural questions that could retrieve these facts.
Each QA pair should be precise, grounded in the source, and framed as a standalone example.
Prefer factual answers over subjective interpretatio. """

prompt = ChatPromptTemplate.from_message(
    [("system", SYSTEM_PROMP), ("user", "Document: {inpu}")]
)


class QAPair(BaseModel):
    question: str = Field(
        ..., description="A natural language question generated from the documen."
    )
    answer: str = Field(
        ...,
        description="A concise, accurate answer to the question based on the documen.",
    )


class QAForRAGOutput(BaseModel):
    qa_pairs: list[QAPair] = Field(
        ..., description="A list of question-answer pairs suitable for RAG or QA task."
    )


qa_for_rag_generator_config = AugLLMConfig(
    name="qa_for_rag_generato",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=QAForRAGOutput,
)

qa_for_rag_generator = create_simple_agent(
    engine=qa_for_rag_generator_config, name="qa_for_rag_generato"
)
