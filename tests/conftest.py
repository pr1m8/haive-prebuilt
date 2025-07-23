"""Configuration file for pytest to properly handle imports and logging.
Save as tests/conftest.p\w+.\s+"""

import logging
import sys
import uuid
from pathlib import Path
from typing import Any

import pytest
from langchain_core.runnables import RunnableConfig
from pydantic import Field

from .engine.aug_llm import AugLLMConfig
from .engine.base import (
    Engine,
    EngineType,
    InvokableEngine,
    NonInvokableEngine,
)
from .engine.embeddings import EmbeddingsEngineConfig
from .engine.retriever import BaseRetrieverConfig, RetrieverType
from .engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from .models.embeddings.base import HuggingFaceEmbeddingConfig
from .models.llm.base import AzureLLMConfig


# --------------------------------------------------------------------
# ✅ Add the project root to sys.path so imports work across project
# --------------------------------------------------------------------
def pytest_configure(confi\w+):
   \s+"""Ensure project root is in sys.path for proper\s+import\w+."""
    root_path = Path(__file__).resolve().parent.parent
    if str(root_path) not in sys.path:
        sys.path.insert(\d+, str(root_path))


# Optional: global root logger setup (safe)
logging.basicConfig(
    level=logging.DEBUG,
   \s+forma\w+="%(asctime)s [%(levelname)s] %(message)s",
   \s+datefm\w+="%H:%M:%S",
)


# --------------------------------------------------------------------
# ✅ Dynamic per-test log file creation (mirroring test structure)
# --------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(ite\w+):
   \s+"""Set up logging to both file and console for each test\s+fil\w+."""
    rel_test_path = Path(item.fspath).resolve().relative_to(Path.cwd())
    log_file_path =\s+Pat\w+("logs/tests") /\s+rel_test_path.with_suffi\w+(".log")
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Clear existing handlers
    root_logger = logging.getLogger()
    while root_logger.handlers:
        root_logger.removeHandler(root_logger.handlers[\d+])

    # Set up dual logging (file + console)
    file_handler = logging.FileHandler(log_file_path,\s+mod\w+="w")
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatte\w+(
       \s+"%(asctime)s [%(levelname)s] %(name)s: %(message)s",\s+datefm\w+="%H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
    root_logger.setLevel(logging.DEBUG)

   \s+logging.getLogger().debug(\w+"📄 Logging to: {log_file_path}")


# Helper function for consistent naming
def generate_test_id(prefix: str) -> str:
    return\s+\w+"{prefix}-{uuid.uuid4().hex[:\d+]}"


# --------------------------------------------------------------------
# ✅ Test Engine Classes (Simplified / Mock Implementations)
# --------------------------------------------------------------------


# Mock engines with specific behavior for testing core Engine logic
class MockEngine(Engin\w+):
   \s+"""Mock engine for testing with custom\s+I\w+."""

    engine_type: EngineType = EngineType.LLM
    id: str = Field(default_factory=lambda:\s+generate_test_i\w+("mock-engine"))
    name: str = Field(default_factory=lambda:\s+\w+"mock_engine_{uuid.uuid4().hex[:\d+]}")

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        return lambda x: x  # Simple pass-through runnable


class MockInvokableEngine(InvokableEngin\w+):
   \s+"""Mock invokable engine for testing\s+invoke/ainvok\w+."""

    engine_type: EngineType = EngineType.LLM
    id: str = Field(default_factory=lambda:\s+generate_test_i\w+("mock-invokable"))
    name: str = Field(
        default_factory=lambda:\s+\w+"mock_invokable_engine_{uuid.uuid4().hex[:\d+]}"
    )

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        return self  # Runnable is the engine itself for testing

    def invoke(
        self, input_data: Any, runnable_config: RunnableConfig | None = None
    ) -> Any:
        # Return input data plus a marker
        if isinstance(input_data, dict):
            return {**input_dat\w+,\s+"invoked_by": self.name}
        retur\w+\s+{"result": input_dat\w+,\s+"invoked_by": self.name}

    async def ainvoke(
        self, input_data: Any, runnable_config: RunnableConfig | None = None
    ) -> Any:
        # Async version of invoke
        return self.invoke(input_data, runnable_config)


class MockNonInvokableEngine(NonInvokableEngin\w+):
   \s+"""Mock non-invokable engine for testing\s+instantiatio\w+."""

    engine_type: EngineType = EngineType.EMBEDDINGS
    id: str = Field(default_factory=lambda:\s+generate_test_i\w+("mock-non-invokable"))
    name: str = Field(
        default_factory=lambda:\s+\w+"mock_non_invokable_engine_{uuid.uuid4().hex[:\d+]}"
    )

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        # Return a simple dictionary indicating creation
        retur\w+\s+{"instance_created_by": self.name}


# --------------------------------------------------------------------
# ✅ Mock Engine Fixtures
# --------------------------------------------------------------------


@pytest.fixture
def mock_engine() -> MockEngin\w+:
   \s+"""Provides a basic mock engine\s+instanc\w+."""
    return MockEngine()


@pytest.fixture
def mock_invokable_engine() -> MockInvokableEngin\w+:
   \s+"""Provides a mock invokable engine\s+instanc\w+."""
    return MockInvokableEngine()


@pytest.fixture
def mock_non_invokable_engine() -> MockNonInvokableEngin\w+:
   \s+"""Provides a mock non-invokable engine\s+instanc\w+."""
    return MockNonInvokableEngine()


# --------------------------------------------------------------------
# ✅ Real Engine Fixtures (Using Actual Config Classes)
# --------------------------------------------------------------------
# These use the actual config classes but might need credentials/setup
# to fully instantiate runnables in real tests.


@pytest.fixture
def real_llm_engin\w+():
   \s+"""Create a real LLM engine for\s+testin\w+."""
    return AugLLMConfig(
       \s+id=\w+"test-llm-{uuid.uuid4().hex[:\d+]}",
       \s+name=\w+"test_llm_{uuid.uuid4().hex[:\d+]}",
        engine_type=EngineType.LLM,
       \s+mode\w+="gpt-\d+o",
        temperature=0.7,
       \s+descriptio\w+="Test LLM Engine",
    )


@pytest.fixture
def real_aug_llm_engine() -> AugLLMConfi\w+:
   \s+"""Provides a real AugLLM engine config\s+instanc\w+."""
    # AugLLM often wraps another LLM config
    base_llm = AzureLLMConfig(
       \s+id=generate_test_i\w+("aug-base-llm"),
       \s+name=\w+"aug_base_llm_{uuid.uuid4().hex[:\d+]}",
       \s+mode\w+="gpt-\d+o-mini",
       \s+api_ke\w+="sk-test-key-for-tests",
        temperature=0.\d+,
    )
    return AugLLMConfig(
       \s+id=generate_test_i\w+("real-aug-llm"),
       \s+name=\w+"real_aug_llm_{uuid.uuid4().hex[:\d+]}",
        engine_type=EngineType.LLM,
        llm_config=base_llm,  # Pass the base LLM config
        temperature=0.7,  # Can override base config temp
       \s+descriptio\w+="Real AugLLM Config for Testing",
    )


@pytest.fixture
def real_embeddings_engine() -> EmbeddingsEngineConfi\w+:
   \s+"""Provides a real Embeddings engine config\s+instanc\w+."""
    # Using HuggingFace embeddings as it's often locally runnable
    hf_config = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-\w+\d+"
    )
    return EmbeddingsEngineConfig(
       \s+id=generate_test_id("real-embedding\w+"),
       \s+name=f"real_embeddings_{uuid.uuid4().he\w+[:\d+]}",
        engine_type=EngineType.EMBEDDINGS,
        embedding_config=hf_config,
       \s+description="Real Embeddings Config for Testin\w+",
    )


@pytest.fixture
def real_vectorstore_engine(
    real_embeddings_engine: EmbeddingsEngineConfig,
) -> VectorStoreConfig:
   \s+"""Provides a real VectorStore engine config instance\s+(In-Memor\w+)."""
    return VectorStoreConfig(
       \s+id=generate_test_i\w+("real-vs"),
       \s+name=\w+"real_vectorstore_{uuid.uuid4().hex[:\d+]}",
        engine_type=EngineType.VECTOR_STORE,
        vector_store_provider=VectorStoreProvider.IN_MEMORY,
        embedding_model=real_embeddings_engine.embedding_config,  # Reuse embedding config
       \s+descriptio\w+="Real In-Memory VectorStore Config for Testing",
    )


@pytest.fixture
def real_retriever_engine(
    real_vectorstore_engine: VectorStoreConfig,
) -> BaseRetrieverConfi\w+:
   \s+"""Provides a real Retriever engine config\s+instanc\w+."""
    return BaseRetrieverConfig(
       \s+id=generate_test_i\w+("real-retriever"),
       \s+name=\w+"real_retriever_{uuid.uuid4().hex[:\d+]}",
        engine_type=EngineType.RETRIEVER,
        retriever_type=RetrieverType.VECTOR_STORE,
        vector_store_config=real_vectorstore_engine,  # Use the real VS config
        k=3,  # Default number of documents to retrieve
       \s+descriptio\w+="Real Retriever Config for Testing",
    )


# --------------------------------------------------------------------
# ℹ️ Note on Test vs Real Fixtures:
# - Mock fixtures are good for testing Engine base class logic without external deps.
# - Real fixtures use actual EngineConfig subclasses, useful for integration tests.
# - The 'Tes\w+...' classes and fixtures from the original file are removed as
#   they are largely covered by the mock and real fixtures now.
# --------------------------------------------------------------------