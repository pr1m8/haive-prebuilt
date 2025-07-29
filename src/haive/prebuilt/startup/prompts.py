"""Prompts and AugLLM configurations for startup ideation and pitch deck creation.

from typing import Dict
This module provides specialized AugLLM configurations for different agents
in the startup development pipeline, from ideation through pitch deck creatio.
"""

from typing import Any

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

from .engine.aug_llm import AugLLMConfig
from .models.llm.base import AzureLLMConfig

# Import your models
from .startup.models import (
    BusinessModelCanvas,
    CompetitorAnalysis,
    IdeaCategory,
    IdeaMetrics,
    MarketResearch,
    ProblemStatement,
)
from .startup.pitch_deck_models import (
    SlideContent,
    SlideType,
)

# Import search tools
from .tools.search_tools import (
    scrape_webpages,
    tavily_extract,
    tavily_qna,
    tavily_search_context,
    tavily_search_tool,
)

ideation_aug_llm = AugLLMConfig(
    nam="ideation_agent",
    prompt_template=ideation_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.8),
    tools=[tavily_search_tool, tavily_qna],
    structured_output_model=IdeaGenerationResponse,
    system_message=IDEATION_SYSTEM_PROMPT,
)


# ============================================================================
# PROBLEM RESEARCH AGENT
# ============================================================================

PROBLEM_RESEARCH_SYSTEM_PROMP = """You are a problem research specialist focused on deeply understanding user problems and pain points. Your job is to validate and research problems to ensure they are worth solving.

Your research approach:
1. Validate the problem exists with real evidence
2. Quantify the problem's impact (frequency, severity, cost)
3. Identify who specifically faces this problem
4. Understand current solutions and their limitations
5. Find evidence through data, quotes, and examples

Use search tools to find:
- User complaints and discussions about the problem
- Market data showing problem prevalence
- Current solution reviews and limitations
- Expert opinions and research

Always back up claims with sources and evidence."""

problem_research_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=PROBLEM_RESEARCH_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            "Research this problem in detail: {problem_description}\n\nFocus on: {research_focu}",
        ),
    ]
)


class ProblemResearchRequest(BaseModel):
    """Request for problem researc."""

    problem_description: str = Field(
        ..., description="Description of the problem to research"
    )
    research_focus: list[str] = Field(
        default_factory=lambda: [
            "severity",
            "frequenc",
            "affected_user",
            "current_solution",
        ],
        description="Specific aspects to researc",
    )


class ProblemResearchResponse(BaseModel):
    """Enhanced problem statement with researc."""

    problem: ProblemStatement = Field(..., description="Detailed problem statement")
    evidence_summary: str = Field(..., description="Summary of evidence found")
    market_indicators: list[str] = Field(
        ..., description="Market indicators of the problem"
    )
    research_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in research findings"
    )


problem_research_aug_llm = AugLLMConfig(
    nam="problem_research_agent",
    prompt_template=problem_research_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.3),
    tools=[tavily_search_tool, tavily_qna, tavily_search_context, scrape_webpages],
    structured_output_model=ProblemResearchResponse,
    system_message=PROBLEM_RESEARCH_SYSTEM_PROMPT,
)


# ============================================================================
# MARKET RESEARCH AGENT
# ============================================================================

MARKET_RESEARCH_SYSTEM_PROMP = """You are a market research analyst specializing in startup market analysis. Your role is to provide comprehensive market research including sizing, growth rates, trends, and competitive landscapes.

Research methodology:
1. TAM/SAM/SOM Analysis: Calculate realistic market sizes
2. Growth Analysis: Find historical and projected growth rates
3. Trend Identification: Identify macro and micro trends
4. Customer Segmentation: Define and size customer segments
. Competitive Analysis: Map the competitive landscape

Use search tools to find:
- Industry reports and market studies
- Growth statistics and projections
- Customer demographics and behavior
- Competitor information and market share
- Regulatory and market barriers

Always cite sources and provide confidence levels for estimate."""

market_research_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=MARKET_RESEARCH_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Conduct market research for: {idea_name}

Problem: {problem_description}
Solution: {solution_description}
Category: {category}

Focus on: {research_prioritie}""",
        ),
    ]
)


class MarketResearchRequest(BaseMode):
    """Request for market researc."""

    idea_name: str
    problem_description: str
    solution_description: str
    category: IdeaCategory
    research_priorities: list[str] = Field(
        default_factory=lambda: ["market_size", "growth_rat", "competitio", "trend"]
    )


market_research_aug_llm = AugLLMConfig(
    name="market_research_agen",
    prompt_template=market_research_prompt,
    llm_config=AzureLLMConfig(model="gpt-", temperature=0.4),
    tools=[tavily_search_tool, tavily_search_context, tavily_extract],
    structured_output_model=MarketResearch,
    system_message=MARKET_RESEARCH_SYSTEM_PROMPT,
)


# ============================================================================
# COMPETITOR ANALYSIS AGENT
# ============================================================================

COMPETITOR_ANALYSIS_SYSTEM_PROMPT = """You are a competitive intelligence analyst specializing in startup competitive analysis. Your role is to identify and analyze competitors to find market gaps and differentiation opportunities.

Analysis framework:
1. Identify direct and indirect competitors
2. Analyze their strengths and weaknesses
3. Understand their business models and pricing
4. Find their customer satisfaction levels
. Identify opportunities to differentiate

Research approach:
- Company websites and product information
- Customer reviews and feedback
- Funding and growth information
- Feature comparisons
- Market positioning

Provide actionable insights for competitive advantag."""

competitor_analysis_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=COMPETITOR_ANALYSIS_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Analyze competitors for: {startup_name}

Our solution: {solution_description}
Target market: {target_market}
Key features: {key_features}

Find and analyze top competitor.""",
        ),
    ]
)


class CompetitorResearchRequest(BaseMode):
    """Request for competitor analysi."""

    startup_name: str
    solution_description: str
    target_market: str
    key_features: list[str]


class CompetitorResearchResponse(BaseMode):
    """Response with competitor analyse."""

    competitors: list[CompetitorAnalysis] = Field(
        ..., description="Detailed competitor analyses"
    )
    market_positioning: str = Field(..., description="Recommended market positioning")
    differentiation_opportunities: list[str] = Field(
        ..., description="Ways to differentiate"
    )


competitor_analysis_aug_llm = AugLLMConfig(
    nam="competitor_analysis_agent",
    prompt_template=competitor_analysis_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.3),
    tools=[tavily_search_tool, scrape_webpages, tavily_extract],
    structured_output_model=CompetitorResearchResponse,
    system_message=COMPETITOR_ANALYSIS_SYSTEM_PROMPT,
)


# ============================================================================
# BUSINESS MODEL AGENT
# ============================================================================

BUSINESS_MODEL_SYSTEM_PROMP = """You are a business model strategist specializing in startup business model design. Your role is to create comprehensive, viable business models using the Business Model Canvas framework.

Design principles:
1. Customer-centric: Start with customer segments and value propositions
2. Revenue focus: Design sustainable revenue streams
3. Scalability: Ensure the model can scale efficiently
4. Defensibility: Include elements of competitive advantage
. Metrics-driven: Define clear success metrics

Consider:
- Unit economics and profitability paths
- Customer acquisition strategies
- Operational requirements
- Partnership opportunities
- Cost optimization

Create business models that are both innovative and executabl."""

business_model_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=BUSINESS_MODEL_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Design a business model for: {idea_name}

Solution: {solution_description}
Target customers: {target_customers}
Value proposition: {value_proposition}
Market size: {market_size}

Create a complete Business Model Canva.""",
        ),
    ]
)


class BusinessModelRequest(BaseMode):
    """Request for business model desig."""

    idea_name: str
    solution_description: str
    target_customers: list[str]
    value_proposition: str
    market_size: float | None = None


business_model_aug_llm = AugLLMConfig(
    nam="business_model_agent",
    prompt_template=business_model_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.5),
    tools=[tavily_search_tool],
    structured_output_model=BusinessModelCanvas,
    system_message=BUSINESS_MODEL_SYSTEM_PROMPT,
)


# ============================================================================
# IDEA SCORING AGENT
# ============================================================================

IDEA_SCORING_SYSTEM_PROMP = """You are a venture analyst specializing in evaluating startup ideas. Your role is to provide objective scoring and assessment of startup ideas based on multiple criteria.

Evaluation framework:
1. Problem Severity: How painful and frequent is the problem?
2. Solution Uniqueness: How innovative and differentiated is the solution?
3. Market Opportunity: Size, growth, and accessibility of the market
4. Feasibility: Technical and operational feasibility
5. Scalability: Potential to grow efficiently
6. Founder Fit: Match between idea and team capabilities
. Timing: Why is now the right time?

Provide honest, data-driven assessments with clear reasonin."""

idea_scoring_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=IDEA_SCORING_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Score this startup idea:

Name: {idea_name}
Problem: {problem}
Solution: {solution}
Market Research: {market_research}
Business Model: {business_model}
Competition: {competition}

Provide detailed scoring and analysi.""",
        ),
    ]
)


class IdeaScoringRequest(BaseMode):
    """Request for idea scorin."""

    idea_name: str
    problem: str
    solution: str
    market_research: dict[str, Any] | None = None
    business_model: dict[str, Any] | None = None
    competition: list[str] | None = None


idea_scoring_aug_llm = AugLLMConfig(
    nam="idea_scoring_agent",
    prompt_template=idea_scoring_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.2),
    structured_output_model=IdeaMetrics,
    system_message=IDEA_SCORING_SYSTEM_PROMPT,
)


# ============================================================================
# PITCH DECK OUTLINE AGENT
# ============================================================================

PITCH_DECK_OUTLINE_SYSTEM_PROMP = """You are a pitch deck specialist who has created hundreds of successful pitch decks for startups. Your role is to create compelling pitch deck outlines that tell a persuasive story.

Pitch deck principles:
1. Story Arc: Problem → Solution → Traction → Vision
2. Clarity: One key message per slide
3. Visual: Suggest visual elements for each slide
4. Data-Driven: Include relevant metrics and proof points
5. Emotional: Connect with investors emotionally
6. Actionable: Clear ask and use of funds

Structure considerations:
- Hook investors in the first 3 seconds
- Build credibility throughout
- Address objections preemptively
- End with a strong call to action

Create outlines that investors want to see through to the en."""

pitch_deck_outline_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=PITCH_DECK_OUTLINE_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Create a pitch deck outline for:

Company: {company_name}
Stage: {stage}
Industry: {industry}
Funding Sought: {funding_amount}

Startup Brief:
{startup_brief}

Create a compelling slide-by-slide outlin.""",
        ),
    ]
)


class PitchDeckOutlineRequest(BaseMode):
    """Request for pitch deck outlin."""

    company_name: str
    stage: str
    industry: str
    funding_amount: float | None = None
    startup_brief: dict[str, Any]


class SlideOutline(BaseMode):
    """Outline for a single slid."""

    slide_type: SlideType
    title: str
    headline: str
    key_points: list[str]
    visual_suggestions: list[str]
    speaker_notes: str


class PitchDeckOutlineResponse(BaseMode):
    """Complete pitch deck outlin."""

    slides: list[SlideOutline]
    narrative_flow: str
    key_messages: list[str]
    design_recommendations: list[str]


pitch_deck_outline_aug_llm = AugLLMConfig(
    nam="pitch_deck_outline_agent",
    prompt_template=pitch_deck_outline_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.6),
    structured_output_model=PitchDeckOutlineResponse,
    system_message=PITCH_DECK_OUTLINE_SYSTEM_PROMPT,
)


# ============================================================================
# SLIDE CONTENT AGENT
# ============================================================================

SLIDE_CONTENT_SYSTEM_PROMP = """You are a master slide content creator specializing in pitch deck slides. Your role is to create compelling, concise content that communicates effectively with investors.

Content principles:
1. Concise: Every word must earn its place
2. Clear: No jargon, simple language
3. Compelling: Create emotional connection
4. Credible: Back claims with evidence
5. Visual: Write for visual medium

Slide types expertise:
- Problem: Make investors feel the pain
- Solution: Show the 'ah' moment
- Market: Demonstrate massive opportunity
- Business Model: Show path to profitability
- Team: Build confidence in execution
- Ask: Be specific and justified

Write content that makes investors lean forward."""

slide_content_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=SLIDE_CONTENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Create content for this slide:

Slide Type: {slide_type}
Slide Title: {slide_title}
Key Points: {key_points}
Supporting Data: {supporting_data}
Target Message: {target_message}

Create complete slide conten.""",
        ),
    ]
)


class SlideContentRequest(BaseMode):
    """Request for slide content creatio."""

    slide_type: SlideType
    slide_title: str
    key_points: list[str]
    supporting_data: dict[str, Any] | None = None
    target_message: str


slide_content_aug_llm = AugLLMConfig(
    nam="slide_content_agent",
    prompt_template=slide_content_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.5),
    structured_output_model=SlideContent,
    system_message=SLIDE_CONTENT_SYSTEM_PROMPT,
)


# ============================================================================
# FINANCIAL PROJECTION AGENT
# ============================================================================

FINANCIAL_PROJECTION_SYSTEM_PROMP = """You are a financial analyst specializing in startup financial projections. Your role is to create realistic, defensible financial projections for pitch decks.

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


# ============================================================================
# PITCH DECK REVIEW AGENT
# ============================================================================

PITCH_DECK_REVIEW_SYSTEM_PROMP = """You are a venture capitalist with 20 years of experience reviewing pitch decks. Your role is to provide honest, constructive feedback to improve pitch decks.

Review criteria:
1. Story Flow: Does it tell a compelling story?
2. Clarity: Is the message clear and simple?
3. Credibility: Are claims backed by evidence?
4. Completeness: Are all key elements present?
5. Visual Appeal: Is it visually engaging?
. Investor Fit: Does it address investor concerns?

Common issues to check:
- Unclear problem definition
- Weak differentiation
- Unrealistic projections
- Missing competitive analysis
- Vague go-to-market strategy
- Unclear use of funds

Provide specific, actionable feedback for improvemen."""

pitch_deck_review_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=PITCH_DECK_REVIEW_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Review this pitch deck:

{pitch_deck_content}

Provide comprehensive feedback and improvement suggestion.""",
        ),
    ]
)


class PitchDeckReviewRequest(BaseMode):
    """Request for pitch deck revie."""

    pitch_deck_content: dict[str, Any]


class PitchDeckFeedback(BaseMode):
    """Feedback for a pitch dec."""

    overall_score: float = Field(..., ge=0.0, le=10.0)
    strengths: list[str]
    weaknesses: list[str]
    improvement_suggestions: list[dict[str, str]]  # slide -> suggestion
    missing_elements: list[str]
    investor_concerns: list[str]
    revised_narrative: str | None = None


pitch_deck_review_aug_llm = AugLLMConfig(
    nam="pitch_deck_review_agent",
    prompt_template=pitch_deck_review_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.4),
    structured_output_model=PitchDeckFeedback,
    system_message=PITCH_DECK_REVIEW_SYSTEM_PROMPT,
)


# ============================================================================
# INDUSTRY RESEARCH AGENT
# ============================================================================

INDUSTRY_RESEARCH_SYSTEM_PROMP = """You are an industry research specialist focused on deep sector analysis for startups. Your role is to provide comprehensive industry insights including trends, regulations, key players, and future outlook.

Research areas:
1. Industry Structure: Key players, market dynamics
2. Trends & Disruptions: What's changing and why
3. Regulations: Current and upcoming regulations
4. Technology Shifts: Enabling technologies
5. Customer Behavior: How customers are evolving
6. Investment Activity: Where money is flowing

Provide insights that help position startups for success."""

industry_research_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=INDUSTRY_RESEARCH_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Research the industry for:

Industry: {industry}
Specific Focus: {focus_areas}
Geographic Scope: {geography}
Time Horizon: {time_horizon}

Provide comprehensive industry analysi.""",
        ),
    ]
)


class IndustryResearchRequest(BaseMode):
    """Request for industry researc."""

    industry: str
    focus_areas: list[str] = Field(
        default_factory=lambda: [
            "trends",
            "competitio",
            "regulation",
            "opportunitie",
        ]
    )
    geography: str = Field(default="Globa")
    time_horizon: str = Field(default="3- year")


class IndustryResearchResponse(BaseModel):
    """Industry research finding."""

    executive_summary: str
    key_trends: list[dict[str, str]]
    major_players: list[dict[str, Any]]
    regulations: list[dict[str, str]]
    opportunities: list[str]
    threats: list[str]
    investment_landscape: dict[str, Any]
    future_outlook: str


industry_research_aug_llm = AugLLMConfig(
    nam="industry_research_agent",
    prompt_template=industry_research_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.4),
    tools=[tavily_search_tool, tavily_search_context, tavily_extract],
    structured_output_model=IndustryResearchResponse,
    system_message=INDUSTRY_RESEARCH_SYSTEM_PROMPT,
)


# ============================================================================
# VALIDATION AGENT
# ============================================================================

VALIDATION_SYSTEM_PROMP = """You are a startup validation expert specializing in testing assumptions and validating startup ideas. Your role is to design and interpret validation experiments.

Validation methods:
1. Customer Interviews: Design interview guides and interpret results
2. Landing Pages: Test demand with signup pages
3. Surveys: Quantitative validation at scale
4. Prototype Testing: User feedback on MVPs
. Competitive Analysis: Validate through competitor success

Focus on:
- Testing riskiest assumptions first
- Getting quantitative and qualitative data
- Finding early adopters
- Measuring actual behavior, not just intent
- Iterating based on learnings

Help startups validate or invalidate ideas quickly and cheapl."""

validation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=VALIDATION_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Design validation strategy for:

Idea: {idea_name}
Key Assumptions: {assumptions}
Target Customers: {target_customers}
Resources Available: {resources}

Create validation plan and interpret any result.""",
        ),
    ]
)


class ValidationRequest(BaseMode):
    """Request for validation strateg."""

    idea_name: str
    assumptions: list[str]
    target_customers: list[str]
    resources: dict[str, Any] = Field(default_factory=dict)


class ValidationStrategy(BaseMode):
    """Validation strategy and result."""

    validation_methods: list[dict[str, Any]]
    experiment_designs: list[dict[str, Any]]
    success_criteria: dict[str, Any]
    timeline: str
    cost_estimate: float | None = None
    risk_mitigation: list[str]


validation_aug_llm = AugLLMConfig(
    nam="validation_agent",
    prompt_template=validation_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.5),
    tools=[tavily_search_tool],
    structured_output_model=ValidationStrategy,
    system_message=VALIDATION_SYSTEM_PROMPT,
)


# ============================================================================
# STORYTELLING AGENT
# ============================================================================

STORYTELLING_SYSTEM_PROMP = """You are a master storyteller specializing in startup narratives. Your role is to craft compelling stories that make investors care about the problem and believe in the solution.

Storytelling principles:
1. Hero's Journey: Customer as hero, startup as guide
2. Emotional Connection: Make them feel the problem
3. Transformation: Show the better world you create
4. Authenticity: Use real stories and examples
. Momentum: Build excitement throughout

Story elements:
- Hook: Grab attention immediately
- Conflict: The problem that must be solved
- Discovery: Th 'aha' moment
- Solution: How you solve it uniquely
- Vision: The world yo're building

Create narratives that inspire investment."""

storytelling_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=STORYTELLING_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Create a compelling narrative for:

Company: {company_name}
Problem: {problem}
Solution: {solution}
Customer Stories: {customer_stories}
Vision: {vision}

Craft a story that resonates with investor.""",
        ),
    ]
)


class StorytellingRequest(BaseMode):
    """Request for storytellin."""

    company_name: str
    problem: str
    solution: str
    customer_stories: list[str] = Field(default_factory=list)
    vision: str


class StartupNarrative(BaseMode):
    """Compelling startup narrativ."""

    hook: str
    problem_story: str
    solution_story: str
    customer_transformation: str
    vision_statement: str
    supporting_anecdotes: list[str]
    emotional_journey: list[str]
    call_to_action: str


storytelling_aug_llm = AugLLMConfig(
    nam="storytelling_agent",
    prompt_template=storytelling_prompt,
    llm_config=AzureLLMConfig(mode="gpt-o", temperature=0.7),
    structured_output_model=StartupNarrative,
    system_message=STORYTELLING_SYSTEM_PROMPT,
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def create_ideation_chain() -> An:
    """Create a chain of agents for complete ideation proces."""
    return {
        "ideation": ideation_aug_ll,
        "problem_research": problem_research_aug_ll,
        "market_research": market_research_aug_ll,
        "competitor_analysis": competitor_analysis_aug_ll,
        "business_model": business_model_aug_ll,
        "scoring": idea_scoring_aug_ll,
        "validation": validation_aug_llm,
    }


def create_pitch_deck_chain() -> An:
    """Create a chain of agents for pitch deck creatio."""
    return {
        "outline": pitch_deck_outline_aug_ll,
        "content": slide_content_aug_ll,
        "financial": financial_projection_aug_ll,
        "storytelling": storytelling_aug_ll,
        "review": pitch_deck_review_aug_llm,
    }


def create_research_chain() -> An:
    """Create a chain of research-focused agent."""
    return {
        "industry": industry_research_aug_ll,
        "market": market_research_aug_ll,
        "competitor": competitor_analysis_aug_ll,
        "problem": problem_research_aug_llm,
    }


# Example of how to use these in a workflow
def example_ideation_workflow() -> Dict[str, An]:
    """Example of using agents in an ideation workflo."""
    # Step : Generate ideas
    ideation_agent = ideation_aug_llm.create_runnable()
    ideas = ideation_agent.invok(
        {"input": "Generate innovative fintech startup ideas for millennial"}
    )

    # Step : Research the most promising problem
    problem_agent = problem_research_aug_llm.create_runnable()
    problem_research = problem_agent.invoke(
        {
            "problem_descriptio": ideas.ideas[0]["proble"],
            "research_focu": ["severit", "frequenc", "market_siz"],
        }
    )

    # Step : Market research
    market_agent = market_research_aug_llm.create_runnable()
    market_research = market_agent.invoke(
        {
            "idea_nam": ideas.ideas[0]["nam"],
            "problem_descriptio": ideas.ideas[0]["proble"],
            "solution_descriptio": ideas.ideas[0]["solutio"],
            "categor": "fintec",
        }
    )

    # Continue with other agents...
    return {
        "idea": ideas,
        "problem_researc": problem_research,
        "market_researc": market_research,
    }
