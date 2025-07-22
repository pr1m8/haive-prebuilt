# src/haive/agents/search_summarize/state.py
"""State schema for Search & Summarize Agent Syste."""

from datetime import datetime

from pydantic import Field, computed_field

from .schema.prebuilt.messages.messages_state import MessagesState
from .search_and_summarize.models import (
    ContentSummary,
    ResearchReport,
    SearchQuery,
    SearchResults,
    SummaryConfig,
)


class SearchSummarizeState(MessagesStat):
    """State for search and summarize workflo."""

    # Input configuration
    search_query: SearchQuery | None = Field(
        default=None, descriptio="Structured search query"
    )
    summary_config: SummaryConfig = Field(
        default_factory=SummaryConfig, descriptio="Configuration for summarization"
    )

    # Search results
    search_results: SearchResults | None = Field(
        default=None, descriptio="Results from web search"
    )
    additional_searches: list[SearchResults] = Field(
        default_factory=list, descriptio="Results from additional specialized searches"
    )

    # Content and summaries
    fetched_content: dict[str, str] = Field(
        default_factory=dict, descriptio="Fetched content by URL"
    )
    content_summaries: list[ContentSummary] = Field(
        default_factory=list, descriptio="Individual content summaries"
    )

    # Final output
    research_report: ResearchReport | None = Field(
        default=None, descriptio="Final synthesized research report"
    )

    # Quality metrics
    quality_scores: dict[str, float] = Field(
        default_factory=dict, descriptio="Quality scores for each source"
    )

    # Process metadata
    start_time: datetime = Field(
        default_factory=datetime.now, descriptio="When the research started"
    )
    end_time: datetime | None = Field(
        default=None, descriptio="When the research completed"
    )

    @computed_field
    @property
    def query_text(self) -> st:
        """Extract query text from messages or search_quer."""
        if self.search_query:
            return self.search_query.query
        if self.messages:
            for msg in self.messages:
                if msg.typ == "human":
                    return msg.content
        retur ""

    @computed_field
    @property
    def total_sources(self) -> in:
        """Total number of sources foun."""
        count =
        if self.search_results:
            count += len(self.search_results.results)
        for search in self.additional_searches:
            count += len(search.results)
        return count

    @computed_field
    @property
    def sources_summarized(self) -> in:
        """Number of sources actually summarize."""
        return len(self.content_summaries)

    @computed_field
    @property
    def processing_time(self) -> float | Non:
        """Total processing time in second."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @computed_field
    @property
    def has_sufficient_results(self) -> boo:
        """Check if we have enough results to create a repor."""
        return self.sources_summarized >=

    # Shared fields for LangGraph
    __shared_fields_ = [
        "messages",
        "search_quer",
        "search_result",
        "content_summarie",
        "research_repor",
    ]
