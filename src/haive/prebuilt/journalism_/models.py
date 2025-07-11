"""Models for the Journalism AI Assistant.

This module defines all Pydantic models used by the journalism assistant
for structured outputs, validation, and data handling throughout the
fact-checking, analysis, and review workflows.

Example:
    >>> from journalism_assistant.models import FactCheckStatement, ArticleSummary
    >>> fact_check = FactCheckStatement(
    ...     statement="The economy grew by 3%",
    ...     status="confirmed",
    ...     explanation="Verified by official statistics"
    ... )

Note:
    All models use Pydantic v2 with comprehensive field descriptions
    for documentation and validation.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, PrivateAttr, field_validator, model_validator
from pydantic.types import confloat, conint


class FactCheckStatement(BaseModel):
    """Individual fact-check result for a single statement.

    Represents the verification status of a claim or statement
    extracted from an article.

    Attributes:
        statement: The original claim being fact-checked
        status: Verification status (confirmed/refuted/unverifiable/vague)
        explanation: Detailed explanation of the verification result
        suggested_keywords: Keywords for further research if needed
        confidence: Confidence score in the fact-check result
        sources: Supporting sources used for verification
    """

    statement: str = Field(
        description="The original statement or claim being fact-checked", min_length=10
    )

    status: Literal["confirmed", "refuted", "unverifiable", "vague"] = Field(
        description="Verification status of the statement"
    )

    explanation: str = Field(
        description="Detailed explanation of findings or reason for status",
        min_length=20,
    )

    suggested_keywords: List[str] = Field(
        description="Keywords for further research if verification is incomplete",
        default_factory=list,
        max_items=5,
    )

    confidence: confloat(ge=0.0, le=1.0) = Field(
        description="Confidence score in the fact-check result", default=0.8
    )

    sources: List[Dict[str, str]] = Field(
        description="Supporting sources used for verification", default_factory=list
    )

    @field_validator("suggested_keywords")
    @classmethod
    def validate_keywords(cls, v: List[str]) -> List[str]:
        """Ensure keywords are unique and non-empty."""
        return list(set(k.strip() for k in v if k.strip()))


class FactCheckResult(BaseModel):
    """Complete fact-checking results for an article.

    Contains all fact-check statements and overall statistics
    about the verification process.

    Attributes:
        statements: List of individual fact-check results
        total_claims: Total number of claims analyzed
        confirmed_count: Number of confirmed claims
        refuted_count: Number of refuted claims
        unverifiable_count: Number of unverifiable claims
        vague_count: Number of vague claims
        overall_credibility: Overall credibility score
    """

    statements: List[FactCheckStatement] = Field(
        description="List of individual fact-check results"
    )

    total_claims: int = Field(description="Total number of claims analyzed", ge=0)

    confirmed_count: int = Field(
        description="Number of confirmed claims", ge=0, default=0
    )

    refuted_count: int = Field(description="Number of refuted claims", ge=0, default=0)

    unverifiable_count: int = Field(
        description="Number of unverifiable claims", ge=0, default=0
    )

    vague_count: int = Field(description="Number of vague claims", ge=0, default=0)

    overall_credibility: confloat(ge=0.0, le=1.0) = Field(
        description="Overall credibility score of the article", default=0.0
    )

    @model_validator(mode="after")
    def calculate_statistics(self) -> "FactCheckResult":
        """Calculate statistics from statements."""
        if self.statements:
            self.total_claims = len(self.statements)
            self.confirmed_count = sum(
                1 for s in self.statements if s.status == "confirmed"
            )
            self.refuted_count = sum(
                1 for s in self.statements if s.status == "refuted"
            )
            self.unverifiable_count = sum(
                1 for s in self.statements if s.status == "unverifiable"
            )
            self.vague_count = sum(1 for s in self.statements if s.status == "vague")

            # Calculate overall credibility
            if self.total_claims > 0:
                credibility_score = (
                    self.confirmed_count * 1.0 + self.unverifiable_count * 0.5
                ) / self.total_claims
                self.overall_credibility = round(credibility_score, 2)

        return self


class ArticleSummary(BaseModel):
    """Structured summary of an article.

    Provides a comprehensive summary focusing on key events,
    people, and statistics.

    Attributes:
        main_points: List of main points from the article
        key_people: Important people mentioned
        key_statistics: Important numbers and data
        word_count: Original article word count
        summary_text: Complete summary in paragraph form
    """

    main_points: List[str] = Field(
        description="Main points and events from the article", min_items=3, max_items=7
    )

    key_people: List[str] = Field(
        description="Important people mentioned in the article", default_factory=list
    )

    key_statistics: List[str] = Field(
        description="Important statistics, numbers, or data points",
        default_factory=list,
    )

    word_count: int = Field(description="Word count of the original article", ge=0)

    summary_text: str = Field(
        description="Complete summary in paragraph form (150-200 words)",
        min_length=100,
        max_length=300,
    )


class ToneAnalysis(BaseModel):
    """Analysis of article tone and sentiment.

    Evaluates the overall tone, sentiment, and potential biases
    present in the article.

    Attributes:
        overall_tone: Primary tone of the article
        sentiment_score: Sentiment score (-1 to 1)
        tone_examples: Specific examples supporting the analysis
        detected_biases: List of potential biases found
        objectivity_score: Score for journalistic objectivity
    """

    overall_tone: Literal[
        "neutral", "positive", "negative", "critical", "opinionated", "balanced"
    ] = Field(description="Primary tone of the article")

    sentiment_score: confloat(ge=-1.0, le=1.0) = Field(
        description="Sentiment score where -1 is negative, 0 is neutral, 1 is positive"
    )

    tone_examples: List[Dict[str, str]] = Field(
        description="Specific examples from text supporting the tone analysis",
        min_items=1,
        max_items=5,
    )

    detected_biases: List[str] = Field(
        description="List of potential biases detected", default_factory=list
    )

    objectivity_score: confloat(ge=0.0, le=1.0) = Field(
        description="Score for journalistic objectivity (0=biased, 1=objective)",
        default=0.5,
    )


class ExtractedQuote(BaseModel):
    """Individual quote extracted from an article.

    Represents a direct quote with attribution and context.

    Attributes:
        quote_text: The exact quoted text
        speaker: Person who said the quote
        context: Context or situation of the quote
        position: Position/title of the speaker if mentioned
        significance: Why this quote is important
    """

    quote_text: str = Field(description="The exact quoted text", min_length=10)

    speaker: str = Field(description="Person who said the quote")

    context: str = Field(
        description="Context in which the quote was said", min_length=10
    )

    position: Optional[str] = Field(
        description="Position or title of the speaker", default=None
    )

    significance: Optional[str] = Field(
        description="Why this quote is significant to the article", default=None
    )


class QuoteExtractionResult(BaseModel):
    """Complete quote extraction results.

    Contains all extracted quotes with metadata about
    the extraction process.

    Attributes:
        quotes: List of extracted quotes
        total_quotes: Total number of quotes found
        unique_speakers: Number of unique speakers
        has_attribution: Whether all quotes have proper attribution
    """

    quotes: List[ExtractedQuote] = Field(description="List of extracted quotes")

    total_quotes: int = Field(description="Total number of quotes found", ge=0)

    unique_speakers: int = Field(description="Number of unique speakers quoted", ge=0)

    has_attribution: bool = Field(
        description="Whether all quotes have proper attribution", default=True
    )

    @model_validator(mode="after")
    def calculate_quote_stats(self) -> "QuoteExtractionResult":
        """Calculate statistics from quotes."""
        self.total_quotes = len(self.quotes)

        if self.quotes:
            speakers = set(q.speaker for q in self.quotes)
            self.unique_speakers = len(speakers)
            self.has_attribution = all(
                q.speaker and q.speaker.lower() != "unknown" for q in self.quotes
            )

        return self


class GrammarIssue(BaseModel):
    """Individual grammar or style issue.

    Represents a specific grammar, spelling, or style problem
    found in the text.

    Attributes:
        issue_type: Type of issue found
        text: The problematic text
        suggestion: Suggested correction
        severity: Severity level of the issue
        location: Approximate location in the text
    """

    issue_type: Literal["grammar", "spelling", "punctuation", "style", "clarity"] = (
        Field(description="Type of issue found")
    )

    text: str = Field(description="The problematic text snippet")

    suggestion: str = Field(description="Suggested correction or improvement")

    severity: Literal["minor", "moderate", "major"] = Field(
        description="Severity level of the issue", default="moderate"
    )

    location: Optional[str] = Field(
        description="Approximate location in the text", default=None
    )


class BiasIndicator(BaseModel):
    """Potential bias indicator in the text.

    Represents language or framing that may indicate bias.

    Attributes:
        bias_type: Type of bias detected
        example_text: Text showing the bias
        explanation: Why this indicates bias
        severity: How severe the bias is
        suggestion: How to make it more neutral
    """

    bias_type: Literal[
        "political",
        "cultural",
        "gender",
        "racial",
        "economic",
        "confirmation",
        "selection",
        "framing",
    ] = Field(description="Type of bias detected")

    example_text: str = Field(description="Text excerpt showing the bias")

    explanation: str = Field(
        description="Explanation of why this indicates bias", min_length=20
    )

    severity: Literal["subtle", "moderate", "strong"] = Field(
        description="Severity of the bias", default="moderate"
    )

    suggestion: Optional[str] = Field(
        description="Suggestion for more neutral language", default=None
    )


class GrammarBiasReview(BaseModel):
    """Complete grammar and bias review results.

    Comprehensive review covering grammar issues and potential biases.

    Attributes:
        grammar_issues: List of grammar/style issues found
        bias_indicators: List of potential biases detected
        overall_quality_score: Overall writing quality score
        readability_score: Readability score
        bias_score: Overall bias score
        recommendations: General recommendations for improvement
    """

    grammar_issues: List[GrammarIssue] = Field(
        description="List of grammar and style issues", default_factory=list
    )

    bias_indicators: List[BiasIndicator] = Field(
        description="List of potential bias indicators", default_factory=list
    )

    overall_quality_score: confloat(ge=0.0, le=1.0) = Field(
        description="Overall writing quality score", default=0.7
    )

    readability_score: confloat(ge=0.0, le=1.0) = Field(
        description="Readability score (0=poor, 1=excellent)", default=0.7
    )

    bias_score: confloat(ge=0.0, le=1.0) = Field(
        description="Bias score (0=heavily biased, 1=neutral)", default=0.7
    )

    recommendations: List[str] = Field(
        description="General recommendations for improvement",
        default_factory=list,
        max_items=5,
    )


class JournalismAction(BaseModel):
    """User action request for journalism tasks.

    Represents what actions the user wants to perform
    on the article.

    Attributes:
        actions: List of requested actions
        priority: Priority level for the request
    """

    actions: List[
        Literal[
            "summarization",
            "fact-checking",
            "tone-analysis",
            "quote-extraction",
            "grammar-and-bias-review",
            "full-report",
            "no-action-required",
            "invalid",
        ]
    ] = Field(description="List of actions to perform")

    priority: Literal["low", "medium", "high"] = Field(
        description="Priority level for the request", default="medium"
    )


class SearchResult(BaseModel):
    """Web search result for fact-checking.

    Represents a single search result used for verification.

    Attributes:
        title: Title of the search result
        url: URL of the source
        snippet: Brief excerpt from the page
        relevance_score: How relevant this result is
        credibility_score: Source credibility score
    """

    title: str = Field(description="Title of the search result")
    url: str = Field(description="URL of the source")
    snippet: str = Field(description="Brief excerpt from the page")
    relevance_score: confloat(ge=0.0, le=1.0) = Field(
        description="Relevance to the fact being checked", default=0.5
    )
    credibility_score: Optional[confloat(ge=0.0, le=1.0)] = Field(
        description="Credibility score of the source", default=None
    )


class ArticleChunk(BaseModel):
    """Chunk of article text for processing.

    Represents a portion of the article for processing
    within token limits.

    Attributes:
        chunk_id: Unique identifier for the chunk
        text: The actual text content
        start_position: Starting character position
        end_position: Ending character position
        word_count: Number of words in chunk
    """

    chunk_id: int = Field(description="Unique identifier for the chunk", ge=0)
    text: str = Field(description="The chunk text content", min_length=1)
    start_position: int = Field(description="Starting character position", ge=0)
    end_position: int = Field(description="Ending character position", gt=0)
    word_count: int = Field(description="Number of words in the chunk", gt=0)

    @model_validator(mode="after")
    def validate_positions(self) -> "ArticleChunk":
        """Ensure end position is after start position."""
        if self.end_position <= self.start_position:
            raise ValueError("End position must be after start position")
        return self


class ComprehensiveReport(BaseModel):
    """Complete journalism analysis report.

    Combines all analysis results into a comprehensive report.

    Attributes:
        article_title: Title of the analyzed article
        analysis_timestamp: When the analysis was performed
        summary: Article summary
        fact_check_results: Fact-checking results
        tone_analysis: Tone and sentiment analysis
        quotes: Extracted quotes
        grammar_bias_review: Grammar and bias review
        overall_assessment: Overall article assessment
        recommendations: Recommendations for the article
    """

    article_title: Optional[str] = Field(
        description="Title of the analyzed article", default="Untitled Article"
    )

    analysis_timestamp: datetime = Field(
        description="When the analysis was performed", default_factory=datetime.now
    )

    summary: Optional[ArticleSummary] = Field(
        description="Article summary", default=None
    )

    fact_check_results: Optional[FactCheckResult] = Field(
        description="Fact-checking results", default=None
    )

    tone_analysis: Optional[ToneAnalysis] = Field(
        description="Tone and sentiment analysis", default=None
    )

    quotes: Optional[QuoteExtractionResult] = Field(
        description="Extracted quotes", default=None
    )

    grammar_bias_review: Optional[GrammarBiasReview] = Field(
        description="Grammar and bias review", default=None
    )

    overall_assessment: str = Field(
        description="Overall assessment of the article", default=""
    )

    recommendations: List[str] = Field(
        description="Key recommendations for improving the article",
        default_factory=list,
    )

    # Private attributes
    _processing_time: float = PrivateAttr(default=0.0)

    def to_markdown(self) -> str:
        """Convert report to markdown format.

        Returns:
            str: Formatted markdown report
        """
        md_parts = [
            f"# Journalism Analysis Report",
            f"**Article:** {self.article_title}",
            f"**Analysis Date:** {self.analysis_timestamp.strftime('%Y-%m-%d %H:%M')}",
            "\n---\n",
        ]

        if self.summary:
            md_parts.append("## Summary")
            md_parts.append(self.summary.summary_text)
            md_parts.append(f"\n*Original word count: {self.summary.word_count}*\n")

        if self.fact_check_results:
            md_parts.append("## Fact-Check Results")
            md_parts.append(
                f"**Overall Credibility:** {self.fact_check_results.overall_credibility:.0%}"
            )
            md_parts.append(f"- Confirmed: {self.fact_check_results.confirmed_count}")
            md_parts.append(f"- Refuted: {self.fact_check_results.refuted_count}")
            md_parts.append(
                f"- Unverifiable: {self.fact_check_results.unverifiable_count}"
            )
            md_parts.append(f"- Vague: {self.fact_check_results.vague_count}\n")

        if self.tone_analysis:
            md_parts.append("## Tone Analysis")
            md_parts.append(f"**Overall Tone:** {self.tone_analysis.overall_tone}")
            md_parts.append(
                f"**Objectivity Score:** {self.tone_analysis.objectivity_score:.0%}"
            )
            if self.tone_analysis.detected_biases:
                md_parts.append("**Detected Biases:**")
                for bias in self.tone_analysis.detected_biases:
                    md_parts.append(f"- {bias}")
            md_parts.append("")

        if self.quotes and self.quotes.quotes:
            md_parts.append("## Key Quotes")
            md_parts.append(
                f"*Found {self.quotes.total_quotes} quotes from {self.quotes.unique_speakers} speakers*\n"
            )
            for quote in self.quotes.quotes[:5]:  # Top 5 quotes
                md_parts.append(f'> "{quote.quote_text}"')
                md_parts.append(f"> — {quote.speaker}")
                md_parts.append("")

        if self.overall_assessment:
            md_parts.append("## Overall Assessment")
            md_parts.append(self.overall_assessment)

        if self.recommendations:
            md_parts.append("\n## Recommendations")
            for i, rec in enumerate(self.recommendations, 1):
                md_parts.append(f"{i}. {rec}")

        return "\n".join(md_parts)


# Export all models
__all__ = [
    "FactCheckStatement",
    "FactCheckResult",
    "ArticleSummary",
    "ToneAnalysis",
    "ExtractedQuote",
    "QuoteExtractionResult",
    "GrammarIssue",
    "BiasIndicator",
    "GrammarBiasReview",
    "JournalismAction",
    "SearchResult",
    "ArticleChunk",
    "ComprehensiveReport",
]
