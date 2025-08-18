# ============================================================================
# FINANCIAL PROJECTION AGENT
# ============================================================================

from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.azure import AzureLLMConfig
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

# TODO: This needs to be properly imported or defined
tavily_search_tool = None  # This should be imported from the tools module

FINANCIAL_PROJECTION_SYSTEM_PROMPT = """You are a financial analyst specializing in startup financial projections. Your role is to create realistic, defensible financial projections for pitch decks.

Projection principles:
1. Conservative: Better to under-promise and over-deliver
2. Bottom-up: Build from unit economics
3. Benchmarked: Use industry comparisons
4. Staged: Show clear growth stages
5. Flexible: Model different scenarios

Key metrics to project:
- Revenue growth and drivers
- Gross margins and improvement path
- Burn rate and path to profitability
- Customer acquisition cost (CAC) and lifetime value (LTV)
- Key SaaS metrics if applicable

Create projections that are ambitious yet believable."""

financial_projection_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=FINANCIAL_PROJECTION_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Create financial projections for:.

Company: {company_name}
Business Model: {business_model}
Pricing: {pricing_info}
Market Size: {market_size}
Current Metrics: {current_metrics}

Create 3-year financial projections.""",
        ),
    ]
)


class FinancialProjectionRequest(BaseModel):
    """Request for financial projections."""

    company_name: str
    business_model: str
    pricing_info: Dict[str, Any]
    market_size: float
    current_metrics: Optional[Dict[str, Any]] = None


class FinancialProjectionResponse(BaseModel):
    """Financial projection response."""

    revenue_projections: List[Dict[str, Any]]
    expense_projections: List[Dict[str, Any]]
    key_metrics: Dict[str, List[float]]
    assumptions: List[str]
    charts_data: List[Dict[str, Any]]


financial_projection_aug_llm = AugLLMConfig(
    name="financial_projection_agent",
    prompt_template=financial_projection_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.3),
    tools=[tavily_search_tool],  # For industry benchmarks
    structured_output_model=FinancialProjectionResponse,
    system_message=FINANCIAL_PROJECTION_SYSTEM_PROMPT,
)
