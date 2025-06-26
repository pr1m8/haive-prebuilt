# haive/agents/perplexity/base/state.py
"""
Base state schemas for the Perplexity multi-agent system.

This module defines the core state schemas that are shared across all Perplexity
agents, including search results, citations, and performance metrics.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from haive.core.schema.prebuilt.messages_state import MessagesState
from langchain_core.documents import Document
from pydantic import BaseModel, Field

# ============================================================================
# ENUMS
# ============================================================================


class QueryType(str, Enum):
    """Types of queries that can be processed."""

    SIMPLE_FACTUAL = "simple_factual"
    COMPLEX_REASONING = "complex_reasoning"
    MULTI_STEP = "multi_step"
    RESEARCH = "research"
    PROJECT = "project"
    CONVERSATIONAL = "conversational"
    CODE_RELATED = "code_related"
    MATHEMATICAL = "mathematical"
    REAL_TIME = "real_time"


class SearchMode(str, Enum):
    """Search execution modes."""

    BASIC = "basic"
    PRO = "pro"
    DEEP_RESEARCH = "deep_research"
    LABS = "labs"


class SourceTrustLevel(str, Enum):
    """Trust levels for information sources."""

    VERIFIED = "verified"
    TRUSTED = "trusted"
    STANDARD = "standard"
    UNVERIFIED = "unverified"


class ModelChoice(str, Enum):
    """Available model choices for different tasks."""

    SONAR_7B = "sonar-7b"  # Fast factual QA
    CLAUDE_35_SONNET = "claude-3.5-sonnet"  # Analytical reasoning
    GPT_4O = "gpt-4o"  # Creative synthesis
    MIXTRAL_8X22B = "mixtral-8x22b"  # Multi-perspective analysis


# ============================================================================
# BASE MODELS
# ============================================================================


class Citation(BaseModel):
    """Represents a citation for a piece of information."""

    source_id: str = Field(description="Unique identifier for the source")
    title: str = Field(description="Title of the source")
    url: Optional[str] = Field(default=None, description="URL of the source")
    snippet: str = Field(description="Relevant excerpt from the source")
    relevance_score: float = Field(description="Relevance score (0-1)")
    trust_level: SourceTrustLevel = Field(
        default=SourceTrustLevel.STANDARD, description="Trust level of the source"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When this citation was retrieved"
    )
    sentence_indices: List[int] = Field(
        default_factory=list, description="Indices of sentences that support the claim"
    )


class SearchResult(BaseModel):
    """Represents a search result from web search or retrieval."""

    query: str = Field(description="The search query used")
    documents: List[Document] = Field(
        default_factory=list, description="Retrieved documents"
    )
    raw_results: List[Dict[str, Any]] = Field(
        default_factory=list, description="Raw search results from the search provider"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the search"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When this search was performed"
    )
    search_type: str = Field(
        default="web", description="Type of search performed (web, vector, hybrid)"
    )


class PerformanceMetrics(BaseModel):
    """Tracks performance metrics for the system."""

    start_time: datetime = Field(
        default_factory=datetime.now, description="When processing started"
    )
    end_time: Optional[datetime] = Field(
        default=None, description="When processing completed"
    )
    total_searches: int = Field(default=0, description="Number of searches performed")
    documents_processed: int = Field(
        default=0, description="Number of documents processed"
    )
    tokens_used: int = Field(default=0, description="Total tokens consumed")
    model_calls: Dict[str, int] = Field(
        default_factory=dict, description="Number of calls to each model"
    )
    latency_ms: Optional[float] = Field(
        default=None, description="Total processing time in milliseconds"
    )

    def calculate_latency(self) -> Optional[float]:
        """Calculate latency if start and end times are available."""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.latency_ms = delta.total_seconds() * 1000
            return self.latency_ms
        return None


class QueryAnalysis(BaseModel):
    """Results of query analysis."""

    original_query: str = Field(description="The original user query")
    query_type: QueryType = Field(description="Classified query type")
    complexity_score: float = Field(
        description="Complexity score (0-1)", ge=0.0, le=1.0
    )
    requires_real_time: bool = Field(
        default=False, description="Whether real-time information is needed"
    )
    requires_reasoning: bool = Field(
        default=False, description="Whether multi-step reasoning is needed"
    )
    requires_tools: bool = Field(
        default=False, description="Whether tools (code, calculations) are needed"
    )
    clarifying_questions: List[str] = Field(
        default_factory=list, description="Potential clarifying questions"
    )
    decomposed_steps: List[str] = Field(
        default_factory=list, description="Decomposed steps for complex queries"
    )
    suggested_mode: SearchMode = Field(
        default=SearchMode.BASIC, description="Suggested search mode based on analysis"
    )


# ============================================================================
# BASE STATE SCHEMA
# ============================================================================


class PerplexityBaseState(MessagesState):
    """
    Base state schema for all Perplexity agents.

    This state extends MessagesState to provide conversation management
    while adding Perplexity-specific fields for search, retrieval, and
    quality assurance.
    """

    # Query information
    query: str = Field(description="The user's query")
    query_analysis: Optional[QueryAnalysis] = Field(
        default=None, description="Analysis of the query"
    )

    # Search and retrieval
    search_results: List[SearchResult] = Field(
        default_factory=list, description="All search results"
    )
    current_search_query: Optional[str] = Field(
        default=None, description="Current search query being processed"
    )
    search_iteration: int = Field(
        default=0, description="Current search iteration number"
    )

    # Citations and sources
    citations: List[Citation] = Field(
        default_factory=list, description="All citations collected"
    )
    verified_facts: List[Dict[str, Any]] = Field(
        default_factory=list, description="Facts that have been verified"
    )

    # Response generation
    draft_response: Optional[str] = Field(
        default=None, description="Draft response before quality checks"
    )
    final_response: Optional[str] = Field(
        default=None, description="Final response with citations"
    )

    # Metadata and control
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    performance_metrics: PerformanceMetrics = Field(
        default_factory=PerformanceMetrics, description="Performance tracking"
    )
    search_mode: SearchMode = Field(
        default=SearchMode.BASIC, description="Current search mode"
    )
    max_iterations: int = Field(
        default=5, description="Maximum search iterations allowed"
    )
    confidence_threshold: float = Field(
        default=0.7, description="Minimum confidence for accepting results"
    )

    # Control flags
    should_continue_searching: bool = Field(
        default=True, description="Whether to continue searching"
    )
    needs_clarification: bool = Field(
        default=False, description="Whether clarification is needed from user"
    )

    def add_search_result(self, result: SearchResult) -> None:
        """Add a search result to the state."""
        self.search_results.append(result)
        self.search_iteration += 1
        self.performance_metrics.total_searches += 1
        self.performance_metrics.documents_processed += len(result.documents)

    def add_citation(self, citation: Citation) -> None:
        """Add a citation, avoiding duplicates."""
        if not any(c.source_id == citation.source_id for c in self.citations):
            self.citations.append(citation)

    def get_high_confidence_citations(self) -> List[Citation]:
        """Get citations above the confidence threshold."""
        return [
            c for c in self.citations if c.relevance_score >= self.confidence_threshold
        ]

    def should_continue(self) -> bool:
        """Determine if searching should continue."""
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


class BasicSearchState(PerplexityBaseState):
    """State for basic search mode."""

    # No additional fields needed for basic search
    pass


class ProSearchState(PerplexityBaseState):
    """State for Pro search mode with enhanced reasoning."""

    # Multi-step planning
    execution_plan: List[Dict[str, Any]] = Field(
        default_factory=list, description="Step-by-step execution plan"
    )
    current_step: int = Field(
        default=0, description="Current step in the execution plan"
    )

    # Reasoning traces
    reasoning_traces: List[str] = Field(
        default_factory=list, description="Chain-of-thought reasoning traces"
    )

    # Model selection
    selected_model: Optional[ModelChoice] = Field(
        default=None, description="Selected model for current task"
    )
    model_selection_rationale: Optional[str] = Field(
        default=None, description="Why this model was selected"
    )

    # Code execution
    code_snippets: List[Dict[str, Any]] = Field(
        default_factory=list, description="Code snippets to execute"
    )
    code_results: List[Dict[str, Any]] = Field(
        default_factory=list, description="Results from code execution"
    )

    # Enhanced search
    follow_up_queries: List[str] = Field(
        default_factory=list, description="Generated follow-up queries"
    )
    cross_references: List[Dict[str, Any]] = Field(
        default_factory=list, description="Cross-referenced information"
    )


class ResearchState(PerplexityBaseState):
    """State for deep research mode."""

    # Research planning
    research_topic: str = Field(description="Main research topic")
    subtopics: List[str] = Field(
        default_factory=list, description="Identified subtopics"
    )
    research_roadmap: List[Dict[str, Any]] = Field(
        default_factory=list, description="Research execution roadmap"
    )

    # Source management
    source_coverage: Dict[str, List[str]] = Field(
        default_factory=dict, description="Coverage of sources by topic"
    )
    contradictions: List[Dict[str, Any]] = Field(
        default_factory=list, description="Identified contradictions between sources"
    )
    patterns: List[Dict[str, Any]] = Field(
        default_factory=list, description="Identified patterns across sources"
    )

    # Report generation
    report_outline: Optional[Dict[str, Any]] = Field(
        default=None, description="Structured report outline"
    )
    report_sections: Dict[str, str] = Field(
        default_factory=dict, description="Generated report sections"
    )
    visual_elements: List[Dict[str, Any]] = Field(
        default_factory=list, description="Charts, graphs, or other visuals"
    )

    # Research metrics
    source_diversity_score: float = Field(
        default=0.0, description="Diversity of sources (0-1)"
    )
    coverage_completeness: float = Field(
        default=0.0, description="Completeness of topic coverage (0-1)"
    )


class LabsState(PerplexityBaseState):
    """State for Labs mode with project-based workflows."""

    # Project analysis
    project_type: str = Field(description="Type of project")
    project_requirements: List[str] = Field(
        default_factory=list, description="Identified project requirements"
    )
    deliverables: List[Dict[str, Any]] = Field(
        default_factory=list, description="Expected deliverables"
    )

    # Tool orchestration
    required_tools: List[str] = Field(
        default_factory=list, description="Tools required for the project"
    )
    tool_execution_log: List[Dict[str, Any]] = Field(
        default_factory=list, description="Log of tool executions"
    )

    # Asset generation
    generated_assets: Dict[str, Any] = Field(
        default_factory=dict, description="Generated project assets"
    )
    asset_dependencies: Dict[str, List[str]] = Field(
        default_factory=dict, description="Dependencies between assets"
    )

    # Integration and deployment
    integration_status: Dict[str, bool] = Field(
        default_factory=dict, description="Integration status of components"
    )
    deployment_ready: bool = Field(
        default=False, description="Whether project is ready for deployment"
    )

    # Project metadata
    estimated_completion_time: Optional[float] = Field(
        default=None, description="Estimated time to complete in minutes"
    )
    actual_completion_time: Optional[float] = Field(
        default=None, description="Actual completion time in minutes"
    )
