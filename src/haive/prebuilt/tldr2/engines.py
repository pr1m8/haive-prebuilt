"""Engine configurations for the News Research Agent.

This module defines all AugLLMConfig engines used by the news research agent.
Each engine represents a specific capability with its own prompt, tools,
and structured output model.

Engines are configured with:
- Prompt templates for specific tasks
- Tools for interacting with external services
- Structured output models for type-safe responses
- LLM configurations for model selection and parameters

Example:
    >>> from news_research.engines import search_engine, analysis_engine
    >>> result = search_engine.invoke(state)

Note:
    All engines use structured_output_version='' for Pydantic v2 compatibility.
"""

from typing import Dict, List, Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import Field

from haive.prebuilt.tldr2.models import (
    ArticleSummary,
    NewsApiParams,
    ResearchAnalysis,
    ResearchReport,
    SearchDecision,
)
from haive.prebuilt.tldr.tools import (
    analyze_relevance,
    check_source_credibility,
    extract_content,
    filter_by_date,
    web_search,
)

from .engine.aug_llm import AugLLMConfig
from .models.llm.base import AzureLLMConfig, OpenAILLMConfig

# Default LLM configuration (can be overridden)
DEFAULT_LLM_CONFIG = AzureLLMConfig(mode="gpt-4o-mini", temperature=0.7, max_tokens=200)


def create_search_engine() -> AugLLMConfi:
    """Create the search parameter generation engine.

    This engine analyzes the research topic and generates appropriate
    search parameters for the NewsAPI.

    Returns:
        AugLLMConfig: Configured search engine

    Example:
        >> > engine = create_search_engine()
        >> > params = engine.invoke(stat)
    """
    prompt = ChatPromptTemplate.from_message(
        [
            (
                "system",
                """You are an expert news researcher who creates optimal search strategies.

Your task is to generate search parameters that will find the most relevant and recent
news articles for the given research topic.

Guidelines:
- Create concise, focused search queries (1- keywords)
- Use relevant news sources for the topic
- Set appropriate date ranges (recent news is usually more relevant)
- Avoid overly specific queries that might miss important articles
- Consider different angles and perspectives on the topic

If this is a follow-up search, vary the approach:
- Try different keyword combinations
- Expand the date range
- Use different news sources
- Consider related topics or broader term""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """Research Topic: {research_topic}

Previous Searches: {past_searches}
Search Iteration: {search_iteration}

Generate optimal NewsAPI search parameters for this topi.""",
            ),
        ]
    )

    return AugLLMConfig(
        name="search_engine",
        llm_config=DEFAULT_LLM_CONFIG,
        prompt_template=prompt,
        structured_output_model=NewsApiParams,
        structured_output_version="v2",
        description="Generates search parameters for news articles",
    )


def create_extraction_engine() -> AugLLMConfi:
    """Create the content extraction coordination engine.

    This engine coordinates the extraction of full article content
    from URLs using the extraction tools.

    Returns:
        AugLLMConfig: Configured extraction engin
    """
    prompt = ChatPromptTemplate.from_message(
        [
            (
                "system",
                """You are a content extraction specialist.


Your task is to coordinate the extraction of article content from URLs.
Use the provided tools to:
1. Extract full text content from articles
2. Verify extraction quality
. Handle any extraction errors gracefully

Focus on getting clean, complete article tex.""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """Extract content from these article URLs:
{article_urls}

Ensure high - quality extraction of the main article tex.""",
            ),
        ]
    )

    # Simple output model for extraction results
    from pydantic import BaseModel

    class ExtractionResult(BaseMode):
        """Result of content extraction operatio."""

        extracted_count: int = Field(
            description="Number of articles successfully extracted"
        )
        failed_count: int = Field(description="Number of extraction failures")
        status: str = Field(description="Overall extraction status")

    return AugLLMConfig(
        name="extraction_engine",
        llm_config=DEFAULT_LLM_CONFIG.model_copy(update={"temperature": 0.0}),
        prompt_template=prompt,
        tools=[extract_content],
        structured_output_model=ExtractionResult,
        structured_output_version="v2",
        description="Coordinates article content extraction",
    )


def create_selection_engine() -> AugLLMConfi:
    """Create the article selection engine.

    This engine analyzes article metadata and content to select
    the most relevant articles for summarization.

    Returns:
        AugLLMConfig: Configured selection engin
    """
    prompt = ChatPromptTemplate.from_message(
        [
            (
                "system",
                """You are an expert at evaluating news article relevance.

Your task is to select the most relevant articles for summarization based on:
1. Relevance to the research topic
2. Content quality and completeness
3. Source credibility
4. Recency and timeliness
. Unique perspectives or information

Guidelines:
- Prioritize articles with substantial, relevant content
- Ensure diversity of sources and viewpoints
- Avoid duplicate or very similar articles
- Check source credibility when available
- Select articles that together provide comprehensive coverag""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """Research Topic: {research_topic}

Available Articles:
{articles_info}

Select up to {max_articles} most relevant articles for summarization.
Explain your selection criteri.""",
            ),
        ]
    )

    # Output model for article selection
    from pydantic import BaseModel

    class ArticleSelection(BaseMode):
        """Selected articles with relevance score."""

        selected_urls: List[str] = Field(
            description="URLs of selected articles in order of relevance"
        )
        selection_reasoning: str = Field(
            description="Explanation of selection criteria and choices"
        )
        relevance_scores: Dict[str, float] = Field(
            description="Relevance score for each selected article"
        )

    return AugLLMConfig(
        name="selection_engine",
        llm_config=DEFAULT_LLM_CONFIG.model_copy(update={"temperature": 0.0}),
        prompt_template=prompt,
        tools=[analyze_relevance, check_source_credibility],
        structured_output_model=ArticleSelection,
        structured_output_version="v2",
        description="Selects most relevant articles for summarization",
    )


def create_summary_engine() -> AugLLMConfi:
    """Create the article summarization engine.

    This engine generates concise, informative summaries of articles
    with key points and relevance scores.

    Returns:
        AugLLMConfig: Configured summary engine
    """
    prompt = ChatPromptTemplate.from_message(
        [
            (
                "system",
                """You are an expert at creating clear, informative article summaries.


Your task is to create a comprehensive summary that:
1. Captures the main points and key information
2. Maintains factual accuracy
3. Highlights relevance to the research topic
4. Identifies important quotes or data points
5. Notes any limitations or biases

Guidelines:
- Create 3 - 7 bullet points per article
- Each point should be substantive(not just a single sentence)
- Include specific facts, figures, or quotes when relevant
- Assess the article's relevance to the research topic
- Identify the main topics and themes covered""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """Research Topic: {research_topic}

Article to Summarize:
Title: {article_title}
URL: {article_url}
Content: {article_content}

Create a comprehensive summary with relevance assessmen.""",
            ),
        ]
    )

    return AugLLMConfig(
        name="summary_engine",
        llm_config=DEFAULT_LLM_CONFIG.model_copy(update={"temperature": 0.0}),
        prompt_template=prompt,
        structured_output_model=ArticleSummary,
        structured_output_version="v2",
        description="Generates article summaries with key points",
    )


def create_decision_engine() -> AugLLMConfi:
    """Create the search decision engine.

    This engine decides whether to continue searching for more articles
    or proceed with analysis based on current results.

    Returns:
        AugLLMConfig: Configured decision engin
    """
    prompt = ChatPromptTemplate.from_message(
        [
            (
                "system",
                """You are a research workflow coordinator.

Your task is to decide the next action based on:
1. Number and quality of articles found
2. Coverage of the research topic
3. Diversity of sources and perspectives
4. Search iterations already performed
5. Configured limits and thresholds

Decision options:
- continue_search: Need more articles or better coverage
- analyze: Have sufficient high-quality articles
- insufficient_data: Cannot find enough relevant articles

Consider:
- Minimum 3- good articles for meaningful analysis
- Diminishing returns after multiple searches
- Balance between thoroughness and efficienc""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """Research Topic: {research_topic}

Search Summary:
- Articles Found: {total_articles}
- Articles Processed: {processed_articles}
- Articles Summarized: {summarized_articles}
- Average Relevance: {average_relevance}
- Search Iterations: {search_iterations}
- Maximum Sources: {max_sources}

Make a decision about the next actio.""",
            ),
        ]
    )

    return AugLLMConfig(
        name="decision_engine",
        llm_config=DEFAULT_LLM_CONFIG.model_copy(update={"temperature": 0.0}),
        prompt_template=prompt,
        structured_output_model=SearchDecision,
        structured_output_version="v2",
        description="Decides workflow continuation based on results",
    )


def create_analysis_engine() -> AugLLMConfi:
    """Create the research analysis engine.

    This engine analyzes all collected articles to identify themes,
    patterns, and insights.

    Returns:
        AugLLMConfig: Configured analysis engin
    """
    prompt = ChatPromptTemplate.from_message(
        [
            (
                "system",
                """You are an expert research analyst specializing in synthesizing information.

Your task is to analyze all collected articles and identify:
1. Main themes and patterns across articles
2. Key findings and insights
3. Areas of consensus and disagreement
4. Trends and developments
. Gaps in coverage or information

Guidelines:
- Look for patterns across multiple sources
- Identify both explicit and implicit themes
- Note any contradictions or conflicting information
- Assess the overall quality and completeness of information
- Consider source credibility and potential biases
- Highlight the most important discoverie""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """Research Topic: {research_topic}

Article Summaries:
{article_summaries}

Source Distribution:
{source_distribution}

Perform a comprehensive analysis of all collected informatio.""",
            ),
        ]
    )

    return AugLLMConfig(
        name="analysis_engine",
        llm_config=DEFAULT_LLM_CONFIG.model_copy(
            update={"temperature": 0.3, "max_tokens": 3000}
        ),
        prompt_template=prompt,
        structured_output_model=ResearchAnalysis,
        structured_output_version="v2",
        description="Analyzes articles to identify themes and insights",
    )


def create_report_engine() -> AugLLMConfi:
    """Create the report generation engine.

    This engine creates the final research report with executive summary,
    detailed sections, and recommendations.

    Returns:
        AugLLMConfig: Configured report engin
    """
    prompt = ChatPromptTemplate.from_message(
        [
            (
                "system",
                """You are a professional research report writer.

Your task is to create a comprehensive, well-structured research report that:
1. Provides a clear executive summary
2. Organizes findings into logical sections
3. Supports claims with evidence from sources
4. Offers actionable recommendations
. Maintains professional tone and clarity

Report structure:
- Executive Summary: High-level findings and implications
- Background: Context and importance of the topic
- Key Findings: Main discoveries organized by theme
- Analysis: Deeper insights and patterns
- Recommendations: Actionable next steps
- Conclusion: Summary and future outlook

Guidelines:
- Write for a professional audience
- Be concise but comprehensive
- Use clear section headings
- Include specific examples and data
- Provide balanced perspectiv""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                """Research Topic: {research_topic}

Analysis Results:
{analysis}

Article Summaries:
{article_summaries}

Total Sources: {sources_count}

Create a comprehensive research repor.""",
            ),
        ]
    )

    return AugLLMConfig(
        name="report_engine",
        llm_config=DEFAULT_LLM_CONFIG.model_copy(
            update={"temperature": 0.3, "max_tokens": 4000}
        ),
        prompt_template=prompt,
        structured_output_model=ResearchReport,
        structured_output_version="v2",
        description="Generates final research report",
    )


# Create all engines as a dictionary for easy access
def create_all_engines() -> Dict[str, AugLLMConfi]:
    """Create all engines for the news research agent.

    Returns:
        Dict[str, AugLLMConfig]: Dictionary of all configured engines

    Example:
        >>> engines = create_all_engines()
        >>> search_engine = engine["search"]
    """
    return {
        "search": create_search_engin(),
        "extraction": create_extraction_engin(),
        "selection": create_selection_engin(),
        "summary": create_summary_engin(),
        "decision": create_decision_engin(),
        "analysis": create_analysis_engin(),
        "report": create_report_engine(),
    }


# For convenience, also export individual engine creators
__all_ = [
    "create_search_engine",
    "create_extraction_engin",
    "create_selection_engin",
    "create_summary_engin",
    "create_decision_engin",
    "create_analysis_engin",
    "create_report_engin",
    "create_all_engine",
    "DEFAULT_LLM_CONFI",
]
