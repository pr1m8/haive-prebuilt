"""Engine configurations for the Journalism AI Assistant.

This module defines all AugLLMConfig engines used by the journalism assistant
for various analysis tasks including summarization, fact-checking, tone analysis,
quote extraction, and grammar/bias review.

Each engine is configured with specific prompts, tools, and output models
to handle different aspects of journalism analysis.

Example:
    >>> from journalism_assistant.engines import create_summarization_engine
    >>> summary_engine = create_summarization_engine()
    >>> result = summary_engine.invoke(state)

Note:
    All engines use structured_output_version='v2' for Pydantic v2 compatibility.
"""

from typing import Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, OpenAILLMConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import Field

from .models import (
    ArticleSummary,
    ExtractedQuote,
    FactCheckResult,
    FactCheckStatement,
    GrammarBiasReview,
    JournalismAction,
    QuoteExtractionResult,
    ToneAnalysis,
)
from .tools import (
    analyze_source_diversity,
    calculate_readability_score,
    detect_bias_indicators,
    extract_quotes,
    extract_web_content,
    identify_key_claims,
    search_and_summarize,
    search_web,
)

# Default LLM configuration
DEFAULT_LLM_CONFIG = AzureLLMConfig(
    model="gpt-4o-mini",
    temperature=0.3,  # Lower temperature for more consistent analysis
    max_tokens=2000,
)


def create_action_identification_engine() -> AugLLMConfig:
    """Create engine for identifying user-requested actions.

    This engine analyzes user input to determine which journalism
    analysis actions should be performed.

    Returns:
        AugLLMConfig: Configured action identification engine
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an AI assistant that identifies journalism analysis actions from user requests.

Identify the user's intended actions and categorize them into:
- summarization: Create article summary
- fact-checking: Verify claims and statements
- tone-analysis: Analyze tone and sentiment
- quote-extraction: Extract quotes
- grammar-and-bias-review: Check grammar and bias
- full-report: All analyses combined
- no-action-required: No specific action needed
- invalid: Request outside scope

Guidelines:
1. If user asks for "everything" or "full analysis", select all individual actions
2. List only explicitly requested actions
3. Multiple specific actions can be selected
4. Be precise in interpretation""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """User request: {input_text}

Identify the journalism analysis actions requested.""",
            ),
        ]
    )

    return AugLLMConfig(
        name="action_identification",
        llm_config=DEFAULT_LLM_CONFIG.model_copy(update={"temperature": 0.1}),
        prompt_template=prompt,
        structured_output_model=JournalismAction,
        structured_output_version="v2",
        description="Identifies requested journalism analysis actions",
    )


def create_summarization_engine() -> AugLLMConfig:
    """Create engine for article summarization.

    This engine generates concise summaries focusing on main events,
    key people, and important statistics.

    Returns:
        AugLLMConfig: Configured summarization engine
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert journalism summarizer who creates clear, concise summaries.

Your task is to summarize articles by:
1. Identifying 3-7 main points or events
2. Highlighting key people mentioned
3. Extracting important statistics or data
4. Writing a cohesive summary paragraph (150-200 words)

Focus on:
- Factual accuracy
- Neutral, journalistic tone
- Clear and concise language
- Logical flow of information
- No personal opinions or interpretations""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """Article text to summarize:
{article_text}

Word count: {word_count}

Create a comprehensive summary following the guidelines.""",
            ),
        ]
    )

    return AugLLMConfig(
        name="summarization",
        llm_config=DEFAULT_LLM_CONFIG,
        prompt_template=prompt,
        description="Creates comprehensive article summaries",
    )
