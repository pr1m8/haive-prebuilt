# haive/agents/perplexity/base/engines.py
"""
Engine configurations for the Perplexity multi-agent system.

This module defines all the engine configurations used by different agents,
including LLM configurations, tool configurations, and retrieval engines.
"""

from typing import Any, Dict, List, Optional, Type

from haive.agents.perplexity.base.prompts import PROMPT_REGISTRY
from haive.agents.perplexity.base.state import (
    Citation,
    ModelChoice,
    PerformanceMetrics,
    QueryAnalysis,
    QueryType,
    SearchMode,
    SearchResult,
)
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

# ============================================================================
# STRUCTURED OUTPUT MODELS
# ============================================================================


class QueryAnalysisOutput(BaseModel):
    """Output model for query analysis."""

    original_query: str
    query_type: QueryType
    complexity_score: float = Field(ge=0.0, le=1.0)
    requires_real_time: bool
    requires_reasoning: bool
    requires_tools: bool
    clarifying_questions: List[str] = Field(default_factory=list)
    decomposed_steps: List[str] = Field(default_factory=list)
    suggested_mode: SearchMode
    analysis_rationale: str


class SearchQueryOutput(BaseModel):
    """Output model for search query generation."""

    search_queries: List[Dict[str, str]]
    search_strategy: str


class DocumentScoringOutput(BaseModel):
    """Output model for document relevance scoring."""

    scored_results: List[Dict[str, Any]]
    summary: str


class GeneratedResponse(BaseModel):
    """Output model for response generation."""

    response: str
    confidence: float = Field(ge=0.0, le=1.0)
    missing_information: List[str] = Field(default_factory=list)
    conflicting_sources: List[Dict[str, Any]] = Field(default_factory=list)
    key_citations: List[Dict[str, Any]] = Field(default_factory=list)


class QualityCheckOutput(BaseModel):
    """Output model for quality assurance."""

    quality_score: float = Field(ge=0.0, le=1.0)
    issues_found: List[Dict[str, str]] = Field(default_factory=list)
    enhanced_response: str
    citations_verified: bool
    ready_for_delivery: bool


# ============================================================================
# TOOL CONFIGURATIONS
# ============================================================================


def create_tavily_search_tool() -> StructuredTool:
    """Create a Tavily search tool configuration."""
    from langchain_community.tools.tavily_search import TavilySearchResults

    return TavilySearchResults(
        name="web_search",
        description="Search the web for current information",
        max_results=10,
        include_answer=True,
        include_raw_content=True,
        include_images=False,
        search_depth="advanced",
    )


def create_web_loader_tool() -> StructuredTool:
    """Create a web page loader tool."""
    from langchain_community.document_loaders import WebBaseLoader

    def load_webpage(url: str) -> Dict[str, Any]:
        """Load and parse a webpage."""
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()
            return {
                "success": True,
                "content": documents[0].page_content if documents else "",
                "metadata": documents[0].metadata if documents else {},
                "error": None,
            }
        except Exception as e:
            return {"success": False, "content": "", "metadata": {}, "error": str(e)}

    return StructuredTool.from_function(
        func=load_webpage,
        name="load_webpage",
        description="Load and parse content from a webpage URL",
    )


def create_calculator_tool() -> StructuredTool:
    """Create a calculator tool for mathematical operations."""
    import numexpr

    def calculate(expression: str) -> Dict[str, Any]:
        """Safely evaluate mathematical expressions."""
        try:
            # Remove any potentially dangerous operations
            safe_expr = (
                expression.replace("__", "").replace("import", "").replace("eval", "")
            )
            result = numexpr.evaluate(safe_expr)
            return {
                "success": True,
                "result": float(result),
                "expression": expression,
                "error": None,
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "expression": expression,
                "error": str(e),
            }

    return StructuredTool.from_function(
        func=calculate,
        name="calculator",
        description="Perform mathematical calculations",
    )


def create_code_interpreter_tool() -> StructuredTool:
    """Create a Python code interpreter tool."""
    import os
    import subprocess
    import tempfile

    def execute_python(code: str) -> Dict[str, Any]:
        """Execute Python code in a sandboxed environment."""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Execute the code with timeout
            result = subprocess.run(
                ["python", temp_file],
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
            )

            # Clean up
            os.unlink(temp_file)

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": code,
                "error": None if result.returncode == 0 else result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Code execution timed out",
                "code": code,
                "error": "Timeout after 30 seconds",
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": "",
                "code": code,
                "error": str(e),
            }

    return StructuredTool.from_function(
        func=execute_python,
        name="python_interpreter",
        description="Execute Python code for data analysis and calculations",
    )


# ============================================================================
# LLM ENGINE CONFIGURATIONS
# ============================================================================


def create_query_analysis_engine() -> AugLLMConfig:
    """Create engine for query analysis."""
    return AugLLMConfig(
        name="query_analysis_engine",
        llm_config=AzureLLMConfig(
            model="gpt-4o",
            temperature=0.1,  # Low temperature for consistent classification
            max_tokens=500,
        ),
        prompt_template=PROMPT_REGISTRY["tool_orchestration"],
        structured_output_model=OrchestrationPlanOutput,
        structured_output_version="v2",
    )


# ============================================================================
# ENGINE FACTORY FUNCTIONS
# ============================================================================


def create_engine_set_for_mode(mode: SearchMode) -> Dict[str, AugLLMConfig]:
    """Create the appropriate set of engines for a search mode."""
    base_engines = {
        "query_analysis": create_query_analysis_engine(),
        "search_generation": create_search_generation_engine(),
        "document_scoring": create_document_scoring_engine(),
        "rag_generation": create_rag_generation_engine(),
        "quality_assurance": create_quality_assurance_engine(),
    }

    if mode == SearchMode.BASIC:
        return base_engines

    elif mode == SearchMode.PRO:
        pro_engines = base_engines.copy()
        pro_engines.update(
            {
                "planning": create_planning_engine(),
                "reasoning": create_reasoning_engine(),
            }
        )
        return pro_engines

    elif mode == SearchMode.DEEP_RESEARCH:
        research_engines = base_engines.copy()
        research_engines.update(
            {
                "research_planning": create_research_planning_engine(),
                "source_analysis": create_source_analysis_engine(),
                "synthesis": create_synthesis_engine(),
            }
        )
        return research_engines

    elif mode == SearchMode.LABS:
        labs_engines = base_engines.copy()
        labs_engines.update(
            {
                "project_analysis": create_project_analysis_engine(),
                "tool_orchestration": create_tool_orchestration_engine(),
            }
        )
        return labs_engines

    return base_engines


# ============================================================================
# TOOL REGISTRY
# ============================================================================

TOOL_REGISTRY = {
    "web_search": create_tavily_search_tool,
    "load_webpage": create_web_loader_tool,
    "calculator": create_calculator_tool,
    "python_interpreter": create_code_interpreter_tool,
}


def get_tools_for_mode(mode: SearchMode) -> List[StructuredTool]:
    """Get the appropriate tools for a search mode."""
    base_tools = [TOOL_REGISTRY["web_search"](), TOOL_REGISTRY["load_webpage"]()]

    if mode in [SearchMode.PRO, SearchMode.LABS]:
        base_tools.extend(
            [TOOL_REGISTRY["calculator"](), TOOL_REGISTRY["python_interpreter"]()]
        )

    return AugLLMConfig(
        name="query_analysis",
        structured_output_model=QueryAnalysisOutput,
        structured_output_version="v2",
        uses_messages_field=False,  # This engine doesn't use message history
    )


def create_search_generation_engine() -> AugLLMConfig:
    """Create engine for search query generation."""
    return AugLLMConfig(
        name="search_generation_engine",
        llm_config=AzureLLMConfig(
            model="gpt-4o-mini",  # Faster model for query generation
            temperature=0.7,  # Higher temperature for query diversity
            max_tokens=300,
        ),
        prompt_template=PROMPT_REGISTRY["search_generation"],
        structured_output_model=SearchQueryOutput,
        structured_output_version="v2",
    )


def create_document_scoring_engine() -> AugLLMConfig:
    """Create engine for document relevance scoring."""
    return AugLLMConfig(
        name="document_scoring_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.1, max_tokens=1000),
        prompt_template=PROMPT_REGISTRY["relevance_scoring"],
        structured_output_model=DocumentScoringOutput,
        structured_output_version="v2",
    )


def create_rag_generation_engine(
    model: ModelChoice = ModelChoice.GPT_4O,
) -> AugLLMConfig:
    """Create engine for RAG-based response generation."""
    # Map model choice to actual model name
    model_mapping = {
        ModelChoice.SONAR_7B: "gpt-4o-mini",  # Simulating with faster model
        ModelChoice.CLAUDE_35_SONNET: "gpt-4o",  # Using GPT-4 as substitute
        ModelChoice.GPT_4O: "gpt-4o",
        ModelChoice.MIXTRAL_8X22B: "gpt-4o",  # Using GPT-4 as substitute
    }

    return AugLLMConfig(
        name="rag_generation_engine",
        llm_config=AzureLLMConfig(
            model=model_mapping.get(model, "gpt-4o"), temperature=0.3, max_tokens=2000
        ),
        prompt_template=PROMPT_REGISTRY["rag_generation"],
        structured_output_model=GeneratedResponse,
        structured_output_version="v2",
        uses_messages_field=True,  # This engine uses conversation history
    )


def create_quality_assurance_engine() -> AugLLMConfig:
    """Create engine for quality assurance."""
    return AugLLMConfig(
        name="quality_assurance_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.1, max_tokens=2000),
        prompt_template=PROMPT_REGISTRY["quality_assurance"],
        structured_output_model=QualityCheckOutput,
        structured_output_version="v2",
    )


# ============================================================================
# RETRIEVAL ENGINE CONFIGURATIONS
# ============================================================================


def create_vector_store_config(
    name: str = "perplexity_knowledge_base",
    provider: VectorStoreProvider = VectorStoreProvider.FAISS,
) -> VectorStoreConfig:
    """Create a vector store configuration."""
    return VectorStoreConfig(
        name=name,
        vector_store_provider=provider,
        embedding_model=HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-MiniLM-L6-v2"
        ),
        k=10,  # Default number of results
    )


def create_retriever_config(
    vector_store_config: VectorStoreConfig, search_type: str = "similarity", k: int = 5
) -> VectorStoreRetrieverConfig:
    """Create a retriever configuration."""
    return VectorStoreRetrieverConfig(
        name=f"{vector_store_config.name}_retriever",
        vector_store_config=vector_store_config,
        search_type=search_type,
        k=k,
        score_threshold=0.7,  # Minimum relevance score
    )


# ============================================================================
# PRO MODE ENGINE CONFIGURATIONS
# ============================================================================


def create_planning_engine() -> AugLLMConfig:
    """Create engine for multi-step planning."""
    from haive.agents.perplexity.pro.models import ExecutionPlanOutput

    return AugLLMConfig(
        name="planning_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.3, max_tokens=1500),
        prompt_template=PROMPT_REGISTRY["multi_step_planning"],
        structured_output_model=ExecutionPlanOutput,
        structured_output_version="v2",
    )


def create_reasoning_engine() -> AugLLMConfig:
    """Create engine for chain-of-thought reasoning."""
    from haive.agents.perplexity.pro.models import ReasoningOutput

    return AugLLMConfig(
        name="reasoning_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2, max_tokens=2000),
        prompt_template=PROMPT_REGISTRY["chain_of_thought"],
        structured_output_model=ReasoningOutput,
        structured_output_version="v2",
    )


# ============================================================================
# RESEARCH MODE ENGINE CONFIGURATIONS
# ============================================================================


def create_research_planning_engine() -> AugLLMConfig:
    """Create engine for research planning."""
    from haive.agents.perplexity.research.models import ResearchPlanOutput

    return AugLLMConfig(
        name="research_planning_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.4, max_tokens=2000),
        prompt_template=PROMPT_REGISTRY["research_strategy"],
        structured_output_model=ResearchPlanOutput,
        structured_output_version="v2",
    )


def create_source_analysis_engine() -> AugLLMConfig:
    """Create engine for source analysis."""
    from haive.agents.perplexity.research.models import SourceAnalysisOutput

    return AugLLMConfig(
        name="source_analysis_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.1, max_tokens=2000),
        prompt_template=PROMPT_REGISTRY["source_analysis"],
        structured_output_model=SourceAnalysisOutput,
        structured_output_version="v2",
    )


def create_synthesis_engine() -> AugLLMConfig:
    """Create engine for research synthesis."""
    from haive.agents.perplexity.research.models import SynthesisOutput

    return AugLLMConfig(
        name="synthesis_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.3, max_tokens=3000),
        prompt_template=PROMPT_REGISTRY["research_synthesis"],
        structured_output_model=SynthesisOutput,
        structured_output_version="v2",
    )


# ============================================================================
# LABS MODE ENGINE CONFIGURATIONS
# ============================================================================


def create_project_analysis_engine() -> AugLLMConfig:
    """Create engine for project analysis."""
    from haive.agents.perplexity.labs.models import ProjectAnalysisOutput

    return AugLLMConfig(
        name="project_analysis_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2, max_tokens=2000),
        prompt_template=PROMPT_REGISTRY["project_requirements"],
        structured_output_model=ProjectAnalysisOutput,
        structured_output_version="v2",
    )


def create_tool_orchestration_engine() -> AugLLMConfig:
    """Create engine for tool orchestration."""
    from haive.agents.perplexity.labs.models import OrchestrationPlanOutput

    return AugLLMConfig(
        name="tool_orchestration_engine",
        llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2, max_tokens=1500),
        prompt_template=PROMPT_TEMPLATE,
        structured_output_model=OrchestrationPlanOutput,
        structured_output_version="v2",
    )
