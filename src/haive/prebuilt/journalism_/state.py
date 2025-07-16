"""State schema for the Journalism AI Assistant.

This module defines the state schema that manages the workflow data
for journalism analysis tasks including fact-checking, summarization,
tone analysis, quote extraction, and grammar/bias review.

The state extends MessagesState to maintain conversation history
while tracking all analysis operations and results.

Example:
    >>> from journalism_assistant.state import JournalismState
    >>> state = JournalismState(
    ...     article_text="Article content here...",
    ...     requested_actions=["summarization", "fact-checking"]
    ... )

Note:
    Computed properties use safe access patterns to avoid
    initialization errors with Pydantic v2.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from haive-prebuilt.src.haive.prebuilt.journalism_.models import (
    ArticleChunk,
    ArticleSummary,
    ComprehensiveReport,
    FactCheckResult,
    GrammarBiasReview,
    JournalismAction,
    QuoteExtractionResult,
    SearchResult,
    ToneAnalysis,
)
from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from pydantic import Field, PrivateAttr, computed_field


class JournalismState(MessagesState):
    """State schema for journalism analysis workflow.

    Manages all data throughout the journalism assistant workflow,
    tracking article processing, analysis results, and user interactions.

    Attributes:
        article_text: Full text of the article to analyze
        article_title: Title of the article (if available)
        article_url: Source URL of the article (if available)
        article_author: Author of the article (if available)
        publication_date: When the article was published

        requested_actions: Actions requested by the user
        current_action: Action currently being processed
        chunks: Article text split into manageable chunks

        summary_result: Result of summarization
        fact_check_result: Result of fact-checking
        tone_analysis_result: Result of tone analysis
        quote_extraction_result: Result of quote extraction
        grammar_bias_result: Result of grammar/bias review

        search_results: Web search results for fact-checking
        processing_errors: Any errors encountered during processing

        final_report: Comprehensive report combining all analyses

    Computed Properties:
        total_chunks: Number of text chunks created
        actions_completed: List of completed actions
        actions_pending: List of pending actions
        has_errors: Whether any errors occurred
        is_complete: Whether all requested actions are complete
        overall_credibility: Overall credibility score
        processing_progress: Progress percentage
    """

    # Article information
    article_text: str = Field(description="Full text of the article to analyze")

    article_title: Optional[str] = Field(
        description="Title of the article", default=None
    )

    article_url: Optional[str] = Field(
        description="Source URL of the article", default=None
    )

    article_author: Optional[str] = Field(
        description="Author of the article", default=None
    )

    publication_date: Optional[datetime] = Field(
        description="Publication date of the article", default=None
    )

    # Workflow control
    requested_actions: List[str] = Field(
        description="List of actions requested by the user", default_factory=list
    )

    current_action: Optional[str] = Field(
        description="Action currently being processed", default=None
    )

    chunks: List[ArticleChunk] = Field(
        description="Article text split into manageable chunks", default_factory=list
    )

    # Analysis results
    summary_result: Optional[ArticleSummary] = Field(
        description="Result of article summarization", default=None
    )

    fact_check_result: Optional[FactCheckResult] = Field(
        description="Result of fact-checking analysis", default=None
    )

    tone_analysis_result: Optional[ToneAnalysis] = Field(
        description="Result of tone and sentiment analysis", default=None
    )

    quote_extraction_result: Optional[QuoteExtractionResult] = Field(
        description="Result of quote extraction", default=None
    )

    grammar_bias_result: Optional[GrammarBiasReview] = Field(
        description="Result of grammar and bias review", default=None
    )

    # Supporting data
    search_results: List[SearchResult] = Field(
        description="Web search results used for fact-checking", default_factory=list
    )

    processing_errors: List[Dict[str, Any]] = Field(
        description="Errors encountered during processing", default_factory=list
    )

    # Final output
    final_report: Optional[ComprehensiveReport] = Field(
        description="Comprehensive report combining all analyses", default=None
    )

    # Private attributes
    _start_time: datetime = PrivateAttr(default_factory=datetime.now)
    _completed_actions: Set[str] = PrivateAttr(default_factory=set)

    # Computed properties
    @computed_field
    @property
    def total_chunks(self) -> int:
        """Total number of text chunks created."""
        chunks = getattr(self, "chunks", [])
        return len(chunks) if chunks else 0

    @computed_field
    @property
    def actions_completed(self) -> List[str]:
        """List of completed actions."""
        completed = []

        if getattr(self, "summary_result", None) is not None:
            completed.append("summarization")
        if getattr(self, "fact_check_result", None) is not None:
            completed.append("fact-checking")
        if getattr(self, "tone_analysis_result", None) is not None:
            completed.append("tone-analysis")
        if getattr(self, "quote_extraction_result", None) is not None:
            completed.append("quote-extraction")
        if getattr(self, "grammar_bias_result", None) is not None:
            completed.append("grammar-and-bias-review")

        return completed

    @computed_field
    @property
    def actions_pending(self) -> List[str]:
        """List of pending actions."""
        requested = getattr(self, "requested_actions", [])
        completed = set(self.actions_completed)
        return [action for action in requested if action not in completed]

    @computed_field
    @property
    def has_errors(self) -> bool:
        """Whether any errors occurred during processing."""
        errors = getattr(self, "processing_errors", [])
        return len(errors) > 0

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Whether all requested actions are complete."""
        pending = self.actions_pending
        return len(pending) == 0 and len(self.actions_completed) > 0

    @computed_field
    @property
    def overall_credibility(self) -> Optional[float]:
        """Overall credibility score from fact-checking."""
        fact_check = getattr(self, "fact_check_result", None)
        if fact_check and hasattr(fact_check, "overall_credibility"):
            return fact_check.overall_credibility
        return None

    @computed_field
    @property
    def processing_progress(self) -> float:
        """Processing progress as a percentage."""
        requested = getattr(self, "requested_actions", [])
        if not requested:
            return 0.0

        completed = len(self.actions_completed)
        total = len(requested)
        return round((completed / total) * 100, 1)

    # Helper methods
    def add_chunk(self, chunk: ArticleChunk) -> None:
        """Add a text chunk to the state.

        Args:
            chunk: ArticleChunk to add
        """
        self.chunks.append(chunk)

    def add_search_result(self, result: SearchResult) -> None:
        """Add a search result for fact-checking.

        Args:
            result: SearchResult to add
        """
        self.search_results.append(result)

    def add_error(
        self, action: str, error: str, details: Optional[Dict] = None
    ) -> None:
        """Record an error that occurred during processing.

        Args:
            action: Action being performed when error occurred
            error: Error message
            details: Additional error details
        """
        error_entry = {
            "action": action,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
        }
        self.processing_errors.append(error_entry)

    def set_current_action(self, action: str) -> None:
        """Set the current action being processed.

        Args:
            action: Name of the action
        """
        self.current_action = action

    def complete_action(self, action: str) -> None:
        """Mark an action as completed.

        Args:
            action: Name of the completed action
        """
        self._completed_actions.add(action)
        if self.current_action == action:
            self.current_action = None

    def create_chunks(
        self, chunk_size: int = 100000, overlap: int = 1000
    ) -> List[ArticleChunk]:
        """Create chunks from the article text.

        Args:
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks

        Returns:
            List of ArticleChunk objects
        """
        text = self.article_text
        chunks = []
        chunk_id = 0
        start = 0

        while start < len(text):
            # Calculate end position
            end = min(start + chunk_size, len(text))

            # Try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings
                for sep in [". ", "! ", "? ", "\n\n", "\n"]:
                    last_sep = text.rfind(sep, start, end)
                    if last_sep > start + chunk_size // 2:
                        end = last_sep + len(sep)
                        break

            # Extract chunk text
            chunk_text = text[start:end]
            word_count = len(chunk_text.split())

            # Create chunk object
            chunk = ArticleChunk(
                chunk_id=chunk_id,
                text=chunk_text,
                start_position=start,
                end_position=end,
                word_count=word_count,
            )
            chunks.append(chunk)

            # Update for next iteration
            chunk_id += 1
            start = max(start + 1, end - overlap)

        self.chunks = chunks
        return chunks

    def get_chunk_texts(self) -> List[str]:
        """Get just the text content of all chunks.

        Returns:
            List of chunk text strings
        """
        return [chunk.text for chunk in self.chunks]

    def generate_final_report(self) -> ComprehensiveReport:
        """Generate a comprehensive report from all analysis results.

        Returns:
            ComprehensiveReport combining all analyses
        """
        # Calculate overall assessment
        assessments = []

        if self.overall_credibility is not None:
            if self.overall_credibility >= 0.8:
                assessments.append(
                    "The article demonstrates high credibility with mostly confirmed claims."
                )
            elif self.overall_credibility >= 0.6:
                assessments.append(
                    "The article shows moderate credibility with a mix of confirmed and unverifiable claims."
                )
            else:
                assessments.append(
                    "The article has credibility concerns with multiple refuted or vague claims."
                )

        if self.tone_analysis_result:
            if self.tone_analysis_result.objectivity_score >= 0.8:
                assessments.append("The writing maintains strong objectivity.")
            elif self.tone_analysis_result.objectivity_score <= 0.4:
                assessments.append("The writing shows significant bias.")

        overall_assessment = (
            " ".join(assessments) if assessments else "Analysis complete."
        )

        # Generate recommendations
        recommendations = []

        if self.fact_check_result and self.fact_check_result.refuted_count > 0:
            recommendations.append(
                "Review and correct factual inaccuracies identified in the fact-check."
            )

        if self.tone_analysis_result and self.tone_analysis_result.detected_biases:
            recommendations.append("Address potential biases to improve objectivity.")

        if (
            self.grammar_bias_result
            and len(self.grammar_bias_result.grammar_issues) > 5
        ):
            recommendations.append("Proofread for grammar and style improvements.")

        if (
            self.quote_extraction_result
            and not self.quote_extraction_result.has_attribution
        ):
            recommendations.append("Ensure all quotes have proper attribution.")

        # Create report
        report = ComprehensiveReport(
            article_title=self.article_title,
            summary=self.summary_result,
            fact_check_results=self.fact_check_result,
            tone_analysis=self.tone_analysis_result,
            quotes=self.quote_extraction_result,
            grammar_bias_review=self.grammar_bias_result,
            overall_assessment=overall_assessment,
            recommendations=recommendations,
        )

        self.final_report = report
        return report

    def get_processing_summary(self) -> Dict[str, Any]:
        """Get a summary of the processing status.

        Returns:
            Dictionary with processing statistics
        """
        return {
            "article_title": self.article_title or "Untitled",
            "word_count": len(self.article_text.split()),
            "chunks_created": self.total_chunks,
            "actions_requested": self.requested_actions,
            "actions_completed": self.actions_completed,
            "actions_pending": self.actions_pending,
            "progress": f"{self.processing_progress}%",
            "has_errors": self.has_errors,
            "error_count": len(self.processing_errors),
            "is_complete": self.is_complete,
            "overall_credibility": self.overall_credibility,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        use_enum_values = True
