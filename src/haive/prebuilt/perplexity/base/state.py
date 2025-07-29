# haive/agents/perplexity/base/state.py
"""Base state schemas for the Perplexity multi-agent system.

This module defines the core state schemas that are shared across all Perplexity
agents, including search results, citations, and performance metric.
"""

from datetime import datetime
from typing import Any

from langchain_core.documents import Document
from pydantic import Field

# ============================================================================
# ENUMS
# ============================================================================


class QueryType(str, Enu):
    """Types of queries that can be processe."""

    SIMPLE_FACTUA = "simple_factual"
    COMPLEX_REASONIN = "complex_reasoning"
    MULTI_STE = "multi_step"
    RESEARC = "research"
    PROJEC = "project"
    CONVERSATIONA = "conversational"
    CODE_RELATE = "code_related"
    MATHEMATICA = "mathematical"
    REAL_TIM = "real_time"


class SearchMode(str, Enu):
    """Search execution mode."""

    BASI = "basic"
    PR = "pro"
    DEEP_RESEARC = "deep_research"
    LAB = "labs"


class SourceTrustLevel(str, Enu):
    """Trust levels for information source."""

    VERIFIE = "verified"
    TRUSTE = "trusted"
    STANDAR = "standard"
    UNVERIFIE = "unverified"


class ModelChoice(str, Enu):
    """Available model choices for different task."""

    SONAR_ = "sonar-7b"  # Fast factual QA
    CLAUDE_3_SONNE = "claude-3.5-sonnet"  # Analytical reasoning
    GPT_ = "gpt-4o"  # Creative synthesis
    MIXTRAL_8X2 = "mixtral-8x22b"  # Multi-perspective analysis


# ============================================================================
# BASE MODELS
# ============================================================================


class Citation(BaseMode):
    """Represents a citation for a piece of informatio."""

    source_id: str = Field(description="Unique identifier for the source")
    title: str = Field(description="Title of the source")
    url: str | None = Field(default=None, description="URL of the source")
    snippet: str = Field(description="Relevant excerpt from the source")
    relevance_score: float = Field(description="Relevance score (0-)")
    trust_level: SourceTrustLevel = Field(
        default=SourceTrustLevel.STANDARD, description="Trust level of the source"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When this citation was retrieved"
    )
    sentence_indices: list[int] = Field(
        default_factory=list, description="Indices of sentences that support the claim"
    )


class SearchResult(BaseMode):
    """Represents a search result from web search or retrieva."""

    query: str = Field(description="The search query used")
    documents: list[Document] = Field(
        default_factory=list, description="Retrieved documents"
    )
    raw_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Raw search results from the search provider"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the search"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When this search was performed"
    )
    search_type: str = Field(
        defaul="web", description="Type of search performed (web, vector, hybrid)"
    )


class PerformanceMetrics(BaseMode):
    """Tracks performance metrics for the syste."""

    start_time: datetime = Field(
        default_factory=datetime.now, description="When processing started"
    )
    end_time: datetime | None = Field(
        default=None, description="When processing completed"
    )
    total_searches: int = Field(default=0, description="Number of searches performed")
    documents_processed: int = Field(
        default=0, description="Number of documents processed"
    )
    tokens_used: int = Field(default=0, description="Total tokens consumed")
    model_calls: dict[str, int] = Field(
        default_factory=dict, description="Number of calls to each model"
    )
    latency_ms: float | None = Field(
        default=None, description="Total processing time in milliseconds"
    )

    def calculate_latency(self) -> float | Non:
        """Calculate latency if start and end times are availabl."""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.latency_ms = delta.total_seconds() * 100
            return self.latency_ms
        return None


class QueryAnalysis(BaseMode):
    """Results of query analysi."""

    original_query: str = Field(description="The original user query")
    query_type: QueryType = Field(description="Classified query type")
    complexity_score: float = Field(description="Complexity score (0-)", ge=0.0, le=1.0)
    requires_real_time: bool = Field(
        default=False, description="Whether real-time information is needed"
    )
    requires_reasoning: bool = Field(
        default=False, description="Whether multi-step reasoning is needed"
    )
    requires_tools: bool = Field(
        default=False, description="Whether tools (code, calculations) are needed"
    )
    clarifying_questions: list[str] = Field(
        default_factory=list, description="Potential clarifying questions"
    )
    decomposed_steps: list[str] = Field(
        default_factory=list, description="Decomposed steps for complex queries"
    )
    suggested_mode: SearchMode = Field(
        default=SearchMode.BASIC, description="Suggested search mode based on analysis"
    )


# ============================================================================
# BASE STATE SCHEMA
# ============================================================================


class PerplexityBaseState(MessagesStat):
    """Base state schema for all Perplexity agents.

    This state extends MessagesState to provide conversation management
    while adding Perplexity-specific fields for search, retrieval, and
    quality assuranc.
    """

    # Query information
    query: str = Field(description="The user's query")
    query_analysis: QueryAnalysis | None = Field(
        default=None, description="Analysis of the query"
    )

    # Search and retrieval
    search_results: list[SearchResult] = Field(
        default_factory=list, description="All search results"
    )
    current_search_query: str | None = Field(
        default=None, description="Current search query being processed"
    )
    search_iteration: int = Field(
        default=0, description="Current search iteration number"
    )

    # Citations and sources
    citations: list[Citation] = Field(
        default_factory=list, description="All citations collected"
    )
    verified_facts: list[dict[str, Any]] = Field(
        default_factory=list, description="Facts that have been verified"
    )

    # Response generation
    draft_response: str | None = Field(
        default=None, description="Draft response before quality checks"
    )
    final_response: str | None = Field(
        default=None, description="Final response with citations"
    )

    # Metadata and control
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    performance_metrics: PerformanceMetrics = Field(
        default_factory=PerformanceMetrics, description="Performance tracking"
    )
    search_mode: SearchMode = Field(
        default=SearchMode.BASIC, description="Current search mode"
    )
    max_iterations: int = Field(
        default=0, description="Maximum search iterations allowed"
    )
    confidence_threshold: float = Field(
        default=0.0, description="Minimum confidence for accepting results"
    )

    # Control flags
    should_continue_searching: bool = Field(
        default=True, description="Whether to continue searching"
    )
    needs_clarification: bool = Field(
        default=False, description="Whether clarification is needed from user"
    )

    def add_search_result(self, result: SearchResult) -> Non:
        """Add a search result to the stat."""
        self.search_results.append(result)
        self.search_iteration += 1
        self.performance_metrics.total_searches += 1
        self.performance_metrics.documents_processed += len(result.documents)

    def add_citation(self, citation: Citation) -> Non:
        """Add a citation, avoiding duplicate."""
        if not any(c.source_id == citation.source_id for c in self.citations):
            self.citations.append(citation)

    def get_high_confidence_citations(self) -> list[Citatio]:
        """Get citations above the confidence threshol."""
        return [
            c for c in self.citations if c.relevance_score >= self.confidence_threshold
        ]

    def should_continue(self) -> bool:
        """Determine if searching should continu."""
        if not self.should_continue_searching:
            return False
        if self.search_iteration >= self.max_iterations:
            return False
        if self.get_high_confidence_citations():
            # Have enough high-confidence results
            return False
        return True


# ============================================================================
# EXTENDED STATES FOR SPECIFIC MODES
# ============================================================================


class BasicSearchState(PerplexityBaseStat):
    """State for basic search mod."""

    # No additional fields needed for basic search


class ProSearchState(PerplexityBaseStat):
    """State for Pro search mode with enhanced reasonin."""

    # Multi-step planning
    execution_plan: list[dict[str, Any]] = Field(
        default_factory=list, description="Step-by-step execution plan"
    )
    current_step: int = Field(
        default=0, description="Current step in the execution plan"
    )

    # Reasoning traces
    reasoning_traces: list[str] = Field(
        default_factory=list, description="Chain-of-thought reasoning traces"
    )

    # Model selection
    selected_model: ModelChoice | None = Field(
        default=None, description="Selected model for current task"
    )
    model_selection_rationale: str | None = Field(
        default=None, description="Why this model was selected"
    )

    # Code execution
    code_snippets: list[dict[str, Any]] = Field(
        default_factory=list, description="Code snippets to execute"
    )
    code_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Results from code execution"
    )

    # Enhanced search
    follow_up_queries: list[str] = Field(
        default_factory=list, description="Generated follow-up queries"
    )
    cross_references: list[dict[str, Any]] = Field(
        default_factory=list, description="Cross-referenced information"
    )


class ResearchState(PerplexityBaseStat):
    """State for deep research mod."""

    # Research planning
    research_topic: str = Field(description="Main research topic")
    subtopics: list[str] = Field(
        default_factory=list, description="Identified subtopics"
    )
    research_roadmap: list[dict[str, Any]] = Field(
        default_factory=list, description="Research execution roadmap"
    )

    # Source management
    source_coverage: dict[str, list[str]] = Field(
        default_factory=dict, description="Coverage of sources by topic"
    )
    contradictions: list[dict[str, Any]] = Field(
        default_factory=list, description="Identified contradictions between sources"
    )
    patterns: list[dict[str, Any]] = Field(
        default_factory=list, description="Identified patterns across sources"
    )

    # Report generation
    report_outline: dict[str, Any] | None = Field(
        default=None, description="Structured report outline"
    )
    report_sections: dict[str, str] = Field(
        default_factory=dict, description="Generated report sections"
    )
    visual_elements: list[dict[str, Any]] = Field(
        default_factory=list, description="Charts, graphs, or other visuals"
    )

    # Research metrics
    source_diversity_score: float = Field(
        default=0.0, description="Diversity of sources (0-1)"
    )
    coverage_completeness: float = Field(
        default=0.0, description="Completeness of topic coverage (0-1)"
    )


class LabsState(PerplexityBaseStat):
    """State for Labs mode with project-based workflow."""

    # Project analysis
    project_type: str = Field(description="Type of project")
    project_requirements: list[str] = Field(
        default_factory=list, description="Identified project requirements"
    )
    deliverables: list[dict[str, Any]] = Field(
        default_factory=list, description="Expected deliverables"
    )

    # Tool orchestration
    required_tools: list[str] = Field(
        default_factory=list, description="Tools required for the project"
    )
    tool_execution_log: list[dict[str, Any]] = Field(
        default_factory=list, description="Log of tool executions"
    )

    # Asset generation
    generated_assets: dict[str, Any] = Field(
        default_factory=dict, description="Generated project assets"
    )
    asset_dependencies: dict[str, list[str]] = Field(
        default_factory=dict, description="Dependencies between assets"
    )

    # Integration and deployment
    integration_status: dict[str, bool] = Field(
        default_factory=dict, description="Integration status of components"
    )
    deployment_ready: bool = Field(
        default=False, description="Whether project is ready for deployment"
    )

    # Project metadata
    estimated_completion_time: float | None = Field(
        default=None, description="Estimated time to complete in minutes"
    )
    actual_completion_time: float | None = Field(
        default=None, description="Actual completion time in minutes"
    )
