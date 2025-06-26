"""
Prompts and AugLLM configurations for startup ideation and pitch deck creation.

This module provides specialized AugLLM configurations for different agents
in the startup development pipeline, from ideation through pitch deck creation.
"""

from typing import Any, Dict, List, Optional, Type

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

# Import search tools
from haive.tools.tools.search_tools import (
    scrape_webpages,
    tavily_extract,
    tavily_qna,
    tavily_search_context,
    tavily_search_tool,
)
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

# Import your models
from haive.prebuilt.startup.models import (
    BusinessModelCanvas,
    CompetitorAnalysis,
    IdeaCategory,
    IdeaMetrics,
    MarketResearch,
    ProblemStatement,
    SolutionConcept,
    StartupIdea,
)
from haive.prebuilt.startup.pitch_deck_models import (
    PitchDeck,
    PitchDeckMetadata,
    Slide,
    SlideContent,
    SlideType,
)

ideation_aug_llm = AugLLMConfig(
    name="ideation_agent",
    prompt_template=ideation_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.8),
    tools=[tavily_search_tool, tavily_qna],
    structured_output_model=IdeaGenerationResponse,
    system_message=IDEATION_SYSTEM_PROMPT,
)


# ============================================================================
# PROBLEM RESEARCH AGENT
# ============================================================================

PROBLEM_RESEARCH_SYSTEM_PROMPT = """You are a problem research specialist focused on deeply understanding user problems and pain points. Your job is to validate and research problems to ensure they are worth solving.

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
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            "Research this problem in detail: {problem_description}\n\nFocus on: {research_focus}",
        ),
    ]
)


class ProblemResearchRequest(BaseModel):
    """Request for problem research."""

    problem_description: str = Field(
        ..., description="Description of the problem to research"
    )
    research_focus: List[str] = Field(
        default_factory=lambda: [
            "severity",
            "frequency",
            "affected_users",
            "current_solutions",
        ],
        description="Specific aspects to research",
    )


class ProblemResearchResponse(BaseModel):
    """Enhanced problem statement with research."""

    problem: ProblemStatement = Field(..., description="Detailed problem statement")
    evidence_summary: str = Field(..., description="Summary of evidence found")
    market_indicators: List[str] = Field(
        ..., description="Market indicators of the problem"
    )
    research_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in research findings"
    )


problem_research_aug_llm = AugLLMConfig(
    name="problem_research_agent",
    prompt_template=problem_research_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.3),
    tools=[tavily_search_tool, tavily_qna, tavily_search_context, scrape_webpages],
    structured_output_model=ProblemResearchResponse,
    system_message=PROBLEM_RESEARCH_SYSTEM_PROMPT,
)


# ============================================================================
# MARKET RESEARCH AGENT
# ============================================================================

MARKET_RESEARCH_SYSTEM_PROMPT = """You are a market research analyst specializing in startup market analysis. Your role is to provide comprehensive market research including sizing, growth rates, trends, and competitive landscapes.

Research methodology:
1. TAM/SAM/SOM Analysis: Calculate realistic market sizes
2. Growth Analysis: Find historical and projected growth rates
3. Trend Identification: Identify macro and micro trends
4. Customer Segmentation: Define and size customer segments
5. Competitive Analysis: Map the competitive landscape

Use search tools to find:
- Industry reports and market studies
- Growth statistics and projections
- Customer demographics and behavior
- Competitor information and market share
- Regulatory and market barriers

Always cite sources and provide confidence levels for estimates."""

market_research_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=MARKET_RESEARCH_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Conduct market research for: {idea_name}
    
Problem: {problem_description}
Solution: {solution_description}
Category: {category}

Focus on: {research_priorities}""",
        ),
    ]
)


class MarketResearchRequest(BaseModel):
    """Request for market research."""

    idea_name: str
    problem_description: str
    solution_description: str
    category: IdeaCategory
    research_priorities: List[str] = Field(
        default_factory=lambda: ["market_size", "growth_rate", "competition", "trends"]
    )


market_research_aug_llm = AugLLMConfig(
    name="market_research_agent",
    prompt_template=market_research_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.4),
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
5. Identify opportunities to differentiate

Research approach:
- Company websites and product information
- Customer reviews and feedback
- Funding and growth information
- Feature comparisons
- Market positioning

Provide actionable insights for competitive advantage."""

competitor_analysis_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=COMPETITOR_ANALYSIS_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Analyze competitors for: {startup_name}

Our solution: {solution_description}
Target market: {target_market}
Key features: {key_features}

Find and analyze top competitors.""",
        ),
    ]
)


class CompetitorResearchRequest(BaseModel):
    """Request for competitor analysis."""

    startup_name: str
    solution_description: str
    target_market: str
    key_features: List[str]


class CompetitorResearchResponse(BaseModel):
    """Response with competitor analyses."""

    competitors: List[CompetitorAnalysis] = Field(
        ..., description="Detailed competitor analyses"
    )
    market_positioning: str = Field(..., description="Recommended market positioning")
    differentiation_opportunities: List[str] = Field(
        ..., description="Ways to differentiate"
    )


competitor_analysis_aug_llm = AugLLMConfig(
    name="competitor_analysis_agent",
    prompt_template=competitor_analysis_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.3),
    tools=[tavily_search_tool, scrape_webpages, tavily_extract],
    structured_output_model=CompetitorResearchResponse,
    system_message=COMPETITOR_ANALYSIS_SYSTEM_PROMPT,
)


# ============================================================================
# BUSINESS MODEL AGENT
# ============================================================================

BUSINESS_MODEL_SYSTEM_PROMPT = """You are a business model strategist specializing in startup business model design. Your role is to create comprehensive, viable business models using the Business Model Canvas framework.

Design principles:
1. Customer-centric: Start with customer segments and value propositions
2. Revenue focus: Design sustainable revenue streams
3. Scalability: Ensure the model can scale efficiently
4. Defensibility: Include elements of competitive advantage
5. Metrics-driven: Define clear success metrics

Consider:
- Unit economics and profitability paths
- Customer acquisition strategies
- Operational requirements
- Partnership opportunities
- Cost optimization

Create business models that are both innovative and executable."""

business_model_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=BUSINESS_MODEL_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Design a business model for: {idea_name}

Solution: {solution_description}
Target customers: {target_customers}
Value proposition: {value_proposition}
Market size: {market_size}

Create a complete Business Model Canvas.""",
        ),
    ]
)


class BusinessModelRequest(BaseModel):
    """Request for business model design."""

    idea_name: str
    solution_description: str
    target_customers: List[str]
    value_proposition: str
    market_size: Optional[float] = None


business_model_aug_llm = AugLLMConfig(
    name="business_model_agent",
    prompt_template=business_model_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.5),
    tools=[tavily_search_tool],
    structured_output_model=BusinessModelCanvas,
    system_message=BUSINESS_MODEL_SYSTEM_PROMPT,
)


# ============================================================================
# IDEA SCORING AGENT
# ============================================================================

IDEA_SCORING_SYSTEM_PROMPT = """You are a venture analyst specializing in evaluating startup ideas. Your role is to provide objective scoring and assessment of startup ideas based on multiple criteria.

Evaluation framework:
1. Problem Severity: How painful and frequent is the problem?
2. Solution Uniqueness: How innovative and differentiated is the solution?
3. Market Opportunity: Size, growth, and accessibility of the market
4. Feasibility: Technical and operational feasibility
5. Scalability: Potential to grow efficiently
6. Founder Fit: Match between idea and team capabilities
7. Timing: Why is now the right time?

Provide honest, data-driven assessments with clear reasoning."""

idea_scoring_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=IDEA_SCORING_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Score this startup idea:

Name: {idea_name}
Problem: {problem}
Solution: {solution}
Market Research: {market_research}
Business Model: {business_model}
Competition: {competition}

Provide detailed scoring and analysis.""",
        ),
    ]
)


class IdeaScoringRequest(BaseModel):
    """Request for idea scoring."""

    idea_name: str
    problem: str
    solution: str
    market_research: Optional[Dict[str, Any]] = None
    business_model: Optional[Dict[str, Any]] = None
    competition: Optional[List[str]] = None


idea_scoring_aug_llm = AugLLMConfig(
    name="idea_scoring_agent",
    prompt_template=idea_scoring_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2),
    structured_output_model=IdeaMetrics,
    system_message=IDEA_SCORING_SYSTEM_PROMPT,
)


# ============================================================================
# PITCH DECK OUTLINE AGENT
# ============================================================================

PITCH_DECK_OUTLINE_SYSTEM_PROMPT = """You are a pitch deck specialist who has created hundreds of successful pitch decks for startups. Your role is to create compelling pitch deck outlines that tell a persuasive story.

Pitch deck principles:
1. Story Arc: Problem → Solution → Traction → Vision
2. Clarity: One key message per slide
3. Visual: Suggest visual elements for each slide
4. Data-Driven: Include relevant metrics and proof points
5. Emotional: Connect with investors emotionally
6. Actionable: Clear ask and use of funds

Structure considerations:
- Hook investors in the first 30 seconds
- Build credibility throughout
- Address objections preemptively
- End with a strong call to action

Create outlines that investors want to see through to the end."""

pitch_deck_outline_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=PITCH_DECK_OUTLINE_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Create a pitch deck outline for:

Company: {company_name}
Stage: {stage}
Industry: {industry}
Funding Sought: {funding_amount}

Startup Brief:
{startup_brief}

Create a compelling slide-by-slide outline.""",
        ),
    ]
)


class PitchDeckOutlineRequest(BaseModel):
    """Request for pitch deck outline."""

    company_name: str
    stage: str
    industry: str
    funding_amount: Optional[float] = None
    startup_brief: Dict[str, Any]


class SlideOutline(BaseModel):
    """Outline for a single slide."""

    slide_type: SlideType
    title: str
    headline: str
    key_points: List[str]
    visual_suggestions: List[str]
    speaker_notes: str


class PitchDeckOutlineResponse(BaseModel):
    """Complete pitch deck outline."""

    slides: List[SlideOutline]
    narrative_flow: str
    key_messages: List[str]
    design_recommendations: List[str]


pitch_deck_outline_aug_llm = AugLLMConfig(
    name="pitch_deck_outline_agent",
    prompt_template=pitch_deck_outline_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.6),
    structured_output_model=PitchDeckOutlineResponse,
    system_message=PITCH_DECK_OUTLINE_SYSTEM_PROMPT,
)


# ============================================================================
# SLIDE CONTENT AGENT
# ============================================================================

SLIDE_CONTENT_SYSTEM_PROMPT = """You are a master slide content creator specializing in pitch deck slides. Your role is to create compelling, concise content that communicates effectively with investors.

Content principles:
1. Concise: Every word must earn its place
2. Clear: No jargon, simple language
3. Compelling: Create emotional connection
4. Credible: Back claims with evidence
5. Visual: Write for visual medium

Slide types expertise:
- Problem: Make investors feel the pain
- Solution: Show the 'aha' moment  
- Market: Demonstrate massive opportunity
- Business Model: Show path to profitability
- Team: Build confidence in execution
- Ask: Be specific and justified

Write content that makes investors lean forward."""

slide_content_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=SLIDE_CONTENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Create content for this slide:

Slide Type: {slide_type}
Slide Title: {slide_title}
Key Points: {key_points}
Supporting Data: {supporting_data}
Target Message: {target_message}

Create complete slide content.""",
        ),
    ]
)


class SlideContentRequest(BaseModel):
    """Request for slide content creation."""

    slide_type: SlideType
    slide_title: str
    key_points: List[str]
    supporting_data: Optional[Dict[str, Any]] = None
    target_message: str


slide_content_aug_llm = AugLLMConfig(
    name="slide_content_agent",
    prompt_template=slide_content_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.5),
    structured_output_model=SlideContent,
    system_message=SLIDE_CONTENT_SYSTEM_PROMPT,
)


# ============================================================================
# FINANCIAL PROJECTION AGENT
# ============================================================================

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
            """Create financial projections for:

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


# ============================================================================
# PITCH DECK REVIEW AGENT
# ============================================================================

PITCH_DECK_REVIEW_SYSTEM_PROMPT = """You are a venture capitalist with 20 years of experience reviewing pitch decks. Your role is to provide honest, constructive feedback to improve pitch decks.

Review criteria:
1. Story Flow: Does it tell a compelling story?
2. Clarity: Is the message clear and simple?
3. Credibility: Are claims backed by evidence?
4. Completeness: Are all key elements present?
5. Visual Appeal: Is it visually engaging?
6. Investor Fit: Does it address investor concerns?

Common issues to check:
- Unclear problem definition
- Weak differentiation
- Unrealistic projections
- Missing competitive analysis
- Vague go-to-market strategy
- Unclear use of funds

Provide specific, actionable feedback for improvement."""

pitch_deck_review_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=PITCH_DECK_REVIEW_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Review this pitch deck:

{pitch_deck_content}

Provide comprehensive feedback and improvement suggestions.""",
        ),
    ]
)


class PitchDeckReviewRequest(BaseModel):
    """Request for pitch deck review."""

    pitch_deck_content: Dict[str, Any]


class PitchDeckFeedback(BaseModel):
    """Feedback for a pitch deck."""

    overall_score: float = Field(..., ge=0.0, le=10.0)
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[Dict[str, str]]  # slide -> suggestion
    missing_elements: List[str]
    investor_concerns: List[str]
    revised_narrative: Optional[str] = None


pitch_deck_review_aug_llm = AugLLMConfig(
    name="pitch_deck_review_agent",
    prompt_template=pitch_deck_review_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.4),
    structured_output_model=PitchDeckFeedback,
    system_message=PITCH_DECK_REVIEW_SYSTEM_PROMPT,
)


# ============================================================================
# INDUSTRY RESEARCH AGENT
# ============================================================================

INDUSTRY_RESEARCH_SYSTEM_PROMPT = """You are an industry research specialist focused on deep sector analysis for startups. Your role is to provide comprehensive industry insights including trends, regulations, key players, and future outlook.

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
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Research the industry for:

Industry: {industry}
Specific Focus: {focus_areas}
Geographic Scope: {geography}
Time Horizon: {time_horizon}

Provide comprehensive industry analysis.""",
        ),
    ]
)


class IndustryResearchRequest(BaseModel):
    """Request for industry research."""

    industry: str
    focus_areas: List[str] = Field(
        default_factory=lambda: [
            "trends",
            "competition",
            "regulations",
            "opportunities",
        ]
    )
    geography: str = Field(default="Global")
    time_horizon: str = Field(default="3-5 years")


class IndustryResearchResponse(BaseModel):
    """Industry research findings."""

    executive_summary: str
    key_trends: List[Dict[str, str]]
    major_players: List[Dict[str, Any]]
    regulations: List[Dict[str, str]]
    opportunities: List[str]
    threats: List[str]
    investment_landscape: Dict[str, Any]
    future_outlook: str


industry_research_aug_llm = AugLLMConfig(
    name="industry_research_agent",
    prompt_template=industry_research_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.4),
    tools=[tavily_search_tool, tavily_search_context, tavily_extract],
    structured_output_model=IndustryResearchResponse,
    system_message=INDUSTRY_RESEARCH_SYSTEM_PROMPT,
)


# ============================================================================
# VALIDATION AGENT
# ============================================================================

VALIDATION_SYSTEM_PROMPT = """You are a startup validation expert specializing in testing assumptions and validating startup ideas. Your role is to design and interpret validation experiments.

Validation methods:
1. Customer Interviews: Design interview guides and interpret results
2. Landing Pages: Test demand with signup pages
3. Surveys: Quantitative validation at scale
4. Prototype Testing: User feedback on MVPs
5. Competitive Analysis: Validate through competitor success

Focus on:
- Testing riskiest assumptions first
- Getting quantitative and qualitative data
- Finding early adopters
- Measuring actual behavior, not just intent
- Iterating based on learnings

Help startups validate or invalidate ideas quickly and cheaply."""

validation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=VALIDATION_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Design validation strategy for:

Idea: {idea_name}
Key Assumptions: {assumptions}
Target Customers: {target_customers}
Resources Available: {resources}

Create validation plan and interpret any results.""",
        ),
    ]
)


class ValidationRequest(BaseModel):
    """Request for validation strategy."""

    idea_name: str
    assumptions: List[str]
    target_customers: List[str]
    resources: Dict[str, Any] = Field(default_factory=dict)


class ValidationStrategy(BaseModel):
    """Validation strategy and results."""

    validation_methods: List[Dict[str, Any]]
    experiment_designs: List[Dict[str, Any]]
    success_criteria: Dict[str, Any]
    timeline: str
    cost_estimate: Optional[float] = None
    risk_mitigation: List[str]


validation_aug_llm = AugLLMConfig(
    name="validation_agent",
    prompt_template=validation_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.5),
    tools=[tavily_search_tool],
    structured_output_model=ValidationStrategy,
    system_message=VALIDATION_SYSTEM_PROMPT,
)


# ============================================================================
# STORYTELLING AGENT
# ============================================================================

STORYTELLING_SYSTEM_PROMPT = """You are a master storyteller specializing in startup narratives. Your role is to craft compelling stories that make investors care about the problem and believe in the solution.

Storytelling principles:
1. Hero's Journey: Customer as hero, startup as guide
2. Emotional Connection: Make them feel the problem
3. Transformation: Show the better world you create
4. Authenticity: Use real stories and examples
5. Momentum: Build excitement throughout

Story elements:
- Hook: Grab attention immediately
- Conflict: The problem that must be solved
- Discovery: The 'aha' moment
- Solution: How you solve it uniquely
- Vision: The world you're building

Create narratives that inspire investment."""

storytelling_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=STORYTELLING_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", optional=True),
        (
            "human",
            """Create a compelling narrative for:

Company: {company_name}
Problem: {problem}
Solution: {solution}
Customer Stories: {customer_stories}
Vision: {vision}

Craft a story that resonates with investors.""",
        ),
    ]
)


class StorytellingRequest(BaseModel):
    """Request for storytelling."""

    company_name: str
    problem: str
    solution: str
    customer_stories: List[str] = Field(default_factory=list)
    vision: str


class StartupNarrative(BaseModel):
    """Compelling startup narrative."""

    hook: str
    problem_story: str
    solution_story: str
    customer_transformation: str
    vision_statement: str
    supporting_anecdotes: List[str]
    emotional_journey: List[str]
    call_to_action: str


storytelling_aug_llm = AugLLMConfig(
    name="storytelling_agent",
    prompt_template=storytelling_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.7),
    structured_output_model=StartupNarrative,
    system_message=STORYTELLING_SYSTEM_PROMPT,
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def create_ideation_chain():
    """Create a chain of agents for complete ideation process."""
    return {
        "ideation": ideation_aug_llm,
        "problem_research": problem_research_aug_llm,
        "market_research": market_research_aug_llm,
        "competitor_analysis": competitor_analysis_aug_llm,
        "business_model": business_model_aug_llm,
        "scoring": idea_scoring_aug_llm,
        "validation": validation_aug_llm,
    }


def create_pitch_deck_chain():
    """Create a chain of agents for pitch deck creation."""
    return {
        "outline": pitch_deck_outline_aug_llm,
        "content": slide_content_aug_llm,
        "financial": financial_projection_aug_llm,
        "storytelling": storytelling_aug_llm,
        "review": pitch_deck_review_aug_llm,
    }


def create_research_chain():
    """Create a chain of research-focused agents."""
    return {
        "industry": industry_research_aug_llm,
        "market": market_research_aug_llm,
        "competitor": competitor_analysis_aug_llm,
        "problem": problem_research_aug_llm,
    }


# Example of how to use these in a workflow
def example_ideation_workflow():
    """Example of using agents in an ideation workflow."""

    # Step 1: Generate ideas
    ideation_agent = ideation_aug_llm.create_runnable()
    ideas = ideation_agent.invoke(
        {"input": "Generate innovative fintech startup ideas for millennials"}
    )

    # Step 2: Research the most promising problem
    problem_agent = problem_research_aug_llm.create_runnable()
    problem_research = problem_agent.invoke(
        {
            "problem_description": ideas.ideas[0]["problem"],
            "research_focus": ["severity", "frequency", "market_size"],
        }
    )

    # Step 3: Market research
    market_agent = market_research_aug_llm.create_runnable()
    market_research = market_agent.invoke(
        {
            "idea_name": ideas.ideas[0]["name"],
            "problem_description": ideas.ideas[0]["problem"],
            "solution_description": ideas.ideas[0]["solution"],
            "category": "fintech",
        }
    )

    # Continue with other agents...
    return {
        "ideas": ideas,
        "problem_research": problem_research,
        "market_research": market_research,
    }
