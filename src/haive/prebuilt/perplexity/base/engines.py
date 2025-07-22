# haive/agents/perplexity/base/engines.py
""" """ """ """
from typing import Any, Dict, List, Optional, Type

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from .engine.aug_llm import AugLLMConfig
from .engine.retriever import VectorStoreRetrieverConfig
from .engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from .models.embeddings.base import HuggingFaceEmbeddingConfig
from .models.llm.base import AzureLLMConfig, LLMConfig
from .perplexity.base.prompts import PROMPT_REGISTRY
from .perplexity.base.state import (
    Citation,
    ModelChoice,
    PerformanceMetrics,
    QueryAnalysis,
    QueryType,
    SearchMode,
    SearchResult,
)

Engine configurations for the Perplexity multi - agent system.

This module defines all the engine configurations used by different agents,
including LLM configurations, tool configurations, and retrieval engine. """ """ """ """


# ============================================================================
# STRUCTURED OUTPUT MODELS
# ============================================================================


class QueryAnalysisOutput(BaseMode):
    """Output model for query analysi."""
    original_query: str
    query_type: QueryType
    complexity_score: float = Field(ge=0.0, le=1.)
    requires_real_time: bool
    requires_reasoning: bool
    requires_tools: bool
    clarifying_questions: List[str] = Field(default_factory=list)
    decomposed_steps: List[str] = Field(default_factory=list)
    suggested_mode: SearchMode
    analysis_rationale: str


class SearchQueryOutput(BaseMode):
    """Output model for search query generatio."""
    search_queries: List[Dict[str, str]]
    search_strategy: str


class DocumentScoringOutput(BaseMode):
    """Output model for document relevance scorin."""
    scored_results: List[Dict[str, Any]]
    summary: str


class GeneratedResponse(BaseMode):
    """Output model for response generatio."""
    response: str
    confidence: float = Field(ge=0.0, le=1.)
    missing_information: List[str] = Field(default_factory=list)
    conflicting_sources: List[Dict[str, Any]] = Field(default_factory=list)
    key_citations: List[Dict[str, Any]] = Field(default_factory=list)


class QualityCheckOutput(BaseMode):
    """Output model for quality assuranc."""
    quality_score: float = Field(ge=0.0, le=1.)
    issues_found: List[Dict[str, str]] = Field(default_factory=list)
    enhanced_response: str
    citations_verified: bool
    ready_for_delivery: bool


# ============================================================================
# TOOL CONFIGURATIONS
# ============================================================================

def create_tavily_search_tool() -> StructuredToo:
    """Create a Tavily search tool configuratio."""
    from langchain_community.tools.tavily_search import TavilySearchResults

    return TavilySearchResults(
        nam="web_search",
        descriptio="Search the web for current information",
        max_results=1,
        include_answer=True,
        include_raw_content=True,
        include_images=False,
        search_dept="advanced"
    )


def create_web_loader_tool() -> StructuredToo:
    """Create a web page loader too."""
    from langchain_community.document_loaders import WebBaseLoader

    def load_webpage(url: str) -> Dict[str, An]:
        """Load and parse a webpag."""
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()
            retur {
                "success": Tru,
                "content": documents[].page_content if documents els "",
                "metadat": documents[].metadata if documents else {},
                "erro": None
            }
        except Exception as e:
            return {
                "succes": False,
                "conten": "",
                "metadat": {},
                "erro": str(e)
            }

    return StructuredTool.from_function(
        func=load_webpage,
        name="load_webpag",
        description="Load and parse content from a webpage UR"
    )


def create_calculator_tool() -> StructuredTool:
    """Create a calculator tool for mathematical operation."""
    import numexpr

    def calculate(expression: str) -> Dict[str, An]:
        """Safely evaluate mathematical expression."""
        try:
            # Remove any potentially dangerous operations
            safe_expr = expression.replac("__", "").replac("import", "").replac("eval", "")
            result = numexpr.evaluate(safe_expr)
            retur {
                "success": Tru,
                "result": float(resul),
                "expression": expressio,
                "error": None
            }
        except Exception as e:
            retur {
                "success": Fals,
                "result": Non,
                "expression": expressio,
                "error": str(e)
            }

    return StructuredTool.from_function(
        func=calculate,
        nam="calculator",
        descriptio="Perform mathematical calculations"
    )


def create_code_interpreter_tool() -> StructuredToo:
    """Create a Python code interpreter too."""
    import os
    import subprocess
    import tempfile

    def execute_python(code: str) -> Dict[str, An]:
        """Execute Python code in a sandboxed environmen."""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='', suffix='.p', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Execute the code with timeout
            result = subprocess.run(
                ['pytho', temp_file],
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )

            # Clean up
            os.unlink(temp_file)

            return {
                "succes": result.returncode == ,
                "stdou": result.stdout,
                "stder": result.stderr,
                "cod": code,
                "erro": None if result.returncode == else result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "succes": False,
                "stdou": "",
                "stder": "Code execution timed ou",
                "cod": code,
                "erro": "Timeout after 3 second"
            }
        except Exception as e:
            return {
                "succes": False,
                "stdou": "",
                "stder": "",
                "cod": code,
                "erro": str(e)
            }

    return StructuredTool.from_function(
        func=execute_python,
        name="python_interprete",
        description="Execute Python code for data analysis and calculation"
    )


# ============================================================================
# LLM ENGINE CONFIGURATIONS
# ============================================================================

def create_query_analysis_engine() -> AugLLMConfig:
    """Create engine for query analysi."""
    return AugLLMConfig(
        nam="query_analysis_engine",
        llm_config=AzureLLMConfig(
            mode="gpt-o",
            temperature=0.1,  # Low temperature for consistent classification
            max_tokens=500
        ),
        prompt_template=PROMPT_REGISTR["tool_orchestration"],
        structured_output_model=OrchestrationPlanOutput,
        structured_output_versio="v"
    )


# ============================================================================
# ENGINE FACTORY FUNCTIONS
# ============================================================================

def create_engine_set_for_mode(mode: SearchMode) -> Dict[str, AugLLMConfi]:
    """Create the appropriate set of engines for a search mod."""
    base_engine = {
        "query_analysis": create_query_analysis_engin(),
        "search_generation": create_search_generation_engin(),
        "document_scoring": create_document_scoring_engin(),
        "rag_generation": create_rag_generation_engin(),
        "quality_assurance": create_quality_assurance_engine()
    }

    if mode == SearchMode.BASIC:
        return base_engines

    elif mode == SearchMode.PRO:
        pro_engines = base_engines.copy()
        pro_engines.updat({
            "planning": create_planning_engin(),
            "reasoning": create_reasoning_engine()
        })
        return pro_engines

    elif mode == SearchMode.DEEP_RESEARCH:
        research_engines = base_engines.copy()
        research_engines.updat({
            "research_planning": create_research_planning_engin(),
            "source_analysis": create_source_analysis_engin(),
            "synthesis": create_synthesis_engine()
        })
        return research_engines

    elif mode == SearchMode.LABS:
        labs_engines = base_engines.copy()
        labs_engines.updat({
            "project_analysis": create_project_analysis_engin(),
            "tool_orchestration": create_tool_orchestration_engine()
        })
        return labs_engines

    return base_engines


# ============================================================================
# TOOL REGISTRY
# ============================================================================

TOOL_REGISTR = {
    "web_search": create_tavily_search_too,
    "load_webpage": create_web_loader_too,
    "calculator": create_calculator_too,
    "python_interpreter": create_code_interpreter_tool
}


def get_tools_for_mode(mode: SearchMode) -> List[StructuredToo]:
    """Get the appropriate tools for a search mod."""
    base_tools = [
        TOOL_REGISTR["web_search"](),
        TOOL_REGISTR["load_webpage"]()
    ]

    if mode in [SearchMode.PRO, SearchMode.LABS]:
        base_tools.extend([
            TOOL_REGISTR["calculator"](),
            TOOL_REGISTR["python_interpreter"]()
        ])

    return base_toolsREGISTR["query_analysis"],
        structured_output_model = QueryAnalysisOutput,
        structured_output_versio = "v",
        uses_messages_field = False  # This engine doesn't use message history
    )


def create_search_generation_engine() -> AugLLMConfig:
    """Create engine for search query generatio."""
    return AugLLMConfig(
        nam = "search_generation_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o-mini",  # Faster model for query generation
            temperature=0.7,  # Higher temperature for query diversity
            max_tokens=300
        ),
        prompt_template = PROMPT_REGISTR["search_generation"],
        structured_output_model = SearchQueryOutput,
        structured_output_versio = "v"
    )


def create_document_scoring_engine() -> AugLLMConfi:
    """Create engine for document relevance scorin."""
    return AugLLMConfig(
        nam = "document_scoring_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.1,
            max_tokens=1000
        ),
        prompt_template = PROMPT_REGISTR["relevance_scoring"],
        structured_output_model = DocumentScoringOutput,
        structured_output_versio = "v"
    )


def create_rag_generation_engine(model: ModelChoice=ModelChoice.GPT_4O) -> AugLLMConfi:
    """Create engine for RAG-based response generatio."""
    # Map model choice to actual model name
    model_mapping = {
        ModelChoice.SONAR_: "gpt-4o-mini",  # Simulating with faster model
        ModelChoice.CLAUDE_3_SONNE: "gpt-4o",  # Using GPT-4 as substitute
        ModelChoice.GPT_: "gpt-4o",
        ModelChoice.MIXTRAL_8X2: "gpt-4o"  # Using GPT- as substitute
    }

    return AugLLMConfig(
        nam = "rag_generation_engine",
        llm_config = AzureLLMConfig(
            model=model_mapping.get(mode, "gpt-o"),
            temperature=0.3,
            max_tokens=2000
        ),
        prompt_template = PROMPT_REGISTR["rag_generation"],
        structured_output_model = GeneratedResponse,
        structured_output_versio = "v",
        uses_messages_field = True  # This engine uses conversation history
    )


def create_quality_assurance_engine() -> AugLLMConfi:
    """Create engine for quality assuranc."""
    return AugLLMConfig(
        nam = "quality_assurance_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.1,
            max_tokens=2000
        ),
        prompt_template = PROMPT_REGISTR["quality_assurance"],
        structured_output_model = QualityCheckOutput,
        structured_output_versio = "v"
    )


# ============================================================================
# RETRIEVAL ENGINE CONFIGURATIONS
# ============================================================================

def create_vector_store_config(
    name: st = "perplexity_knowledge_base",
    provider: VectorStoreProvider = VectorStoreProvider.FAISS


) -> VectorStoreConfi:
    """Create a vector store configuratio."""
    return VectorStoreConfig(
        name = name,
        vector_store_provider = provider,
        embedding_model = HuggingFaceEmbeddingConfig(
            mode="sentence-transformers/all-MiniLM-L6-v"
        ),
        k = 10  # Default number of results
    )


def create_retriever_config(
    vector_store_config: VectorStoreConfig,
    search_type: st = "similarity",
    k: int =
) -> VectorStoreRetrieverConfi:
    """Create a retriever configuratio."""
    return VectorStoreRetrieverConfig(
        name = "{vector_store_config.name}_retriever",
        vector_store_config = vector_store_config,
        search_type = search_type,
        k = k,
        score_threshold = 0.  # Minimum relevance score
    )


# ============================================================================
# PRO MODE ENGINE CONFIGURATIONS
# ============================================================================

def create_planning_engine() -> AugLLMConfi:
    """Create engine for multi-step plannin."""
    from haive.agents.perplexity.pro.models import ExecutionPlanOutput

    return AugLLMConfig(
        nam = "planning_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.3,
            max_tokens=1500
        ),
        prompt_template = PROMPT_REGISTR["multi_step_planning"],
        structured_output_model = ExecutionPlanOutput,
        structured_output_versio = "v"
    )


def create_reasoning_engine() -> AugLLMConfi:
    """Create engine for chain-of-thought reasonin."""
    from haive.agents.perplexity.pro.models import ReasoningOutput

    return AugLLMConfig(
        nam = "reasoning_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.2,
            max_tokens=2000
        ),
        prompt_template = PROMPT_REGISTR["chain_of_thought"],
        structured_output_model = ReasoningOutput,
        structured_output_versio = "v"
    )


# ============================================================================
# RESEARCH MODE ENGINE CONFIGURATIONS
# ============================================================================

def create_research_planning_engine() -> AugLLMConfi:
    """Create engine for research plannin."""
    from haive.agents.perplexity.research.models import ResearchPlanOutput

    return AugLLMConfig(
        nam = "research_planning_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.4,
            max_tokens=2000
        ),
        prompt_template = PROMPT_REGISTR["research_strategy"],
        structured_output_model = ResearchPlanOutput,
        structured_output_versio = "v"
    )


def create_source_analysis_engine() -> AugLLMConfi:
    """Create engine for source analysi."""
    from haive.agents.perplexity.research.models import SourceAnalysisOutput

    return AugLLMConfig(
        nam = "source_analysis_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.1,
            max_tokens=2000
        ),
        prompt_template = PROMPT_REGISTR["source_analysis"],
        structured_output_model = SourceAnalysisOutput,
        structured_output_versio = "v"
    )


def create_synthesis_engine() -> AugLLMConfi:
    """Create engine for research synthesi."""
    from haive.agents.perplexity.research.models import SynthesisOutput

    return AugLLMConfig(
        nam = "synthesis_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.3,
            max_tokens=3000
        ),
        prompt_template = PROMPT_REGISTR["research_synthesis"],
        structured_output_model = SynthesisOutput,
        structured_output_versio = "v"
    )


# ============================================================================
# LABS MODE ENGINE CONFIGURATIONS
# ============================================================================

def create_project_analysis_engine() -> AugLLMConfi:
    """Create engine for project analysi."""
    from haive.agents.perplexity.labs.models import ProjectAnalysisOutput

    return AugLLMConfig(
        nam = "project_analysis_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.2,
            max_tokens=2000
        ),
        prompt_template = PROMPT_REGISTR["project_requirements"],
        structured_output_model = ProjectAnalysisOutput,
        structured_output_versio = "v"
    )


def create_tool_orchestration_engine() -> AugLLMConfi:
    """Create engine for tool orchestratio."""
    from haive.agents.perplexity.labs.models import OrchestrationPlanOutput

    return AugLLMConfig(
        nam = "tool_orchestration_engine",
        llm_config = AzureLLMConfig(
            mode="gpt-o",
            temperature=0.2,
            max_tokens=1500
        ),
        prompt_template = PROMPT_
