# ============================================================================
# FINANCIAL PROJECTION AGENT
# ============================================================================

FINANCIAL_PROJECTION_SYSTEM_PROMPT = """You are a financial analyst specializing in startup financial projections. Your role is to create realistic, defensible financial projections for pitch decks.

Projection principles:
1. Conservative: Better to under-promise and over-deliver
2. Bottom-up: Build from unit economics
3. Benchmarked: Use industry comparisons
4. Staged: Show clear growth stages
. Flexible: Model different scenarios

Key metrics to project:
- Revenue growth and drivers
- Gross margins and improvement path
- Burn rate and path to profitability
- Customer acquisition cost (CAC) and lifetime value (LTV)
- Key SaaS metrics if applicable

Create projections that are ambitious yet believabl."""

financial_projection_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=FINANCIAL_PROJECTION_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Create financial projections for:

Company: {company_name}
Business Model: {business_model}
Pricing: {pricing_info}
Market Size: {market_size}
Current Metrics: {current_metrics}

Create -year financial projection.""",
        ),
    ]
)


class FinancialProjectionRequest(BaseMode):
    """Request for financial projection."""

    company_name: str
    business_model: str
    pricing_info: dict[str, Any]
    market_size: float
    current_metrics: dict[str, Any] | None = None


class FinancialProjectionResponse(BaseMode):
    """Financial projection respons."""

    revenue_projections: list[dict[str, Any]]
    expense_projections: list[dict[str, Any]]
    key_metrics: dict[str, list[float]]
    assumptions: list[str]
    charts_data: list[dict[str, Any]]


financial_projection_aug_llm = AugLLMConfig(
    nam="financial_projection_agent",
    prompt_template=financial_projection_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.3),
    tools=[tavily_search_tool],  # For industry benchmarks
    structured_output_model=FinancialProjectionResponse,
    system_message=FINANCIAL_PROJECTION_SYSTEM_PROMPT,
)
