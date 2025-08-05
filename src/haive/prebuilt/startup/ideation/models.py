"""Startup idea models for the Haive framework.

This module provides comprehensive data models for brainstorming, researching,
and evaluating startup ideas using AI agents. These models integrate with the
pitch deck models to create a complete startup development pipeline.

The models support:
- Idea generation and brainstorming
- Market research and validation
- Competitive analysis
- Problem-solution fit assessment
- Business model exploration
- Risk and opportunity analysis
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Literal, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    field_validator,
    model_validator,
)

TResearch = TypeVar("TResearch", bound=BaseModel)
TValidation = TypeVar("TValidation", bound=BaseModel)


class IdeaCategory(str, Enum):
    """Categories of startup ideas."""

    B2B_SAAS = "b2b_saas"
    B2C_APP = "b2c_app"
    MARKETPLACE = "marketplace"
    FINTECH = "fintech"
    HEALTHTECH = "healthtech"
    EDTECH = "edtech"
    DEEPTECH = "deeptech"
    HARDWARE = "hardware"
    ECOMMERCE = "ecommerce"
    SOCIAL = "social"
    ENTERTAINMENT = "entertainment"
    SUSTAINABILITY = "sustainability"
    AI_ML = "ai_ml"
    BLOCKCHAIN = "blockchain"
    BIOTECH = "biotech"
    OTHER = "other"


class IdeaStage(str, Enum):
    """Stage of idea development."""

    RAW_CONCEPT = "raw_concept"
    RESEARCHED = "researched"
    VALIDATED = "validated"
    PROTOTYPED = "prototyped"
    MVP_READY = "mvp_ready"
    LAUNCHED = "launched"


class MarketSize(str, Enum):
    """Market size categories."""

    NICHE = "niche"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    MASSIVE = "massive"


class RiskLevel(str, Enum):
    """Risk level assessment."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ValidationMethod(str, Enum):
    """Methods for validating ideas."""

    CUSTOMER_INTERVIEWS = "customer_interviews"
    SURVEYS = "surveys"
    LANDING_PAGE = "landing_page"
    PROTOTYPE_TESTING = "prototype_testing"
    PILOT_PROGRAM = "pilot_program"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    EXPERT_CONSULTATION = "expert_consultation"
    MARKET_RESEARCH = "market_research"


class ProblemStatement(BaseModel):
    """Defines a problem that the startup idea aims to solve.

    This is the foundation of any good startup idea - a clear problem definition.
    """

    model_config = ConfigDict(extra="forbid")
    problem_id: str = Field(..., description="Unique problem identifier")
    description: str = Field(..., description="Clear description of the problem")
    affected_users: list[str] = Field(..., description="Who experiences this problem")
    frequency: Literal["daily", "weekly", "monthly", "occasionally", "rarely"] = Field(
        ...
    )
    severity: Literal["critical", "high", "medium", "low"] = Field(...)
    current_solutions: list[str] = Field(
        default_factory=list, description="How people currently solve this"
    )
    pain_points: list[str] = Field(..., description="Specific pain points")
    emotional_impact: str | None = Field(
        None, description="How users feel about this problem"
    )
    financial_impact: str | None = Field(None, description="Cost of the problem")
    evidence: list[str] = Field(
        default_factory=list, description="Evidence this problem exists"
    )
    quotes: list[str] = Field(
        default_factory=list, description="Real user quotes about the problem"
    )
    research_sources: list[str] = Field(
        default_factory=list, description="Sources validating the problem"
    )
    validation_score: float = Field(
        0.0, ge=0.0, le=1.0, description="How well validated the problem is"
    )

    @property
    def problem_score(self) -> float:
        """Calculate a score for how good this problem is to solve."""
        severity_scores = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
        frequency_scores = {
            "daily": 1.0,
            "weekly": 0.8,
            "monthly": 0.6,
            "occasionally": 0.4,
            "rarely": 0.2,
        }
        severity_score = severity_scores.get(self.severity, 0.5)
        frequency_score = frequency_scores.get(self.frequency, 0.5)
        evidence_score = min(len(self.evidence) / 5, 1.0)
        return severity_score * 0.4 + frequency_score * 0.3 + evidence_score * 0.3


class SolutionConcept(BaseModel):
    """Defines a solution concept for a problem.

    This represents how the startup plans to solve the identified problem.
    """

    model_config = ConfigDict(extra="forbid")
    solution_id: str = Field(..., description="Unique solution identifier")
    name: str = Field(..., description="Name of the solution")
    description: str = Field(..., description="Clear description of the solution")
    key_features: list[str] = Field(..., description="Main features of the solution")
    value_proposition: str = Field(..., description="Core value proposition")
    unique_aspects: list[str] = Field(..., description="What makes this unique")
    technical_feasibility: float = Field(
        0.5, ge=0.0, le=1.0, description="Technical feasibility score"
    )
    implementation_complexity: RiskLevel = Field(RiskLevel.MEDIUM)
    required_technologies: list[str] = Field(default_factory=list)
    user_journey: list[str] = Field(
        default_factory=list, description="Key steps in user journey"
    )
    wow_factor: str | None = Field(None, description="What will make users say 'wow'")

    @field_validator("key_features")
    @classmethod
    def validate_features(cls, v):
        """Ensure we have at least 3 key features."""
        if len(v) < 3:
            raise ValueError("Solution should have at least 3 key features")
        return v


class MarketResearch(BaseModel):
    """Market research data for a startup idea.

    Contains comprehensive market analysis and research findings.
    """

    model_config = ConfigDict(extra="forbid")
    total_addressable_market: float | None = Field(None, description="TAM in USD")
    serviceable_addressable_market: float | None = Field(None, description="SAM in USD")
    serviceable_obtainable_market: float | None = Field(None, description="SOM in USD")
    market_size_category: MarketSize = Field(MarketSize.MEDIUM)
    growth_rate: float | None = Field(None, ge=0.0, description="Annual growth rate")
    market_trends: list[str] = Field(
        default_factory=list, description="Key market trends"
    )
    market_drivers: list[str] = Field(
        default_factory=list, description="What's driving market growth"
    )
    market_barriers: list[str] = Field(
        default_factory=list, description="Barriers to market entry"
    )
    primary_customers: list[dict[str, Any]] = Field(
        default_factory=list, description="Primary customer segments"
    )
    secondary_customers: list[dict[str, Any]] = Field(
        default_factory=list, description="Secondary segments"
    )
    early_adopters: list[str] = Field(
        default_factory=list, description="Early adopter characteristics"
    )
    direct_competitors: list[dict[str, Any]] = Field(default_factory=list)
    indirect_competitors: list[dict[str, Any]] = Field(default_factory=list)
    market_gaps: list[str] = Field(
        default_factory=list, description="Identified market gaps"
    )
    research_date: datetime = Field(default_factory=datetime.now)
    data_sources: list[str] = Field(default_factory=list)
    confidence_level: float = Field(0.5, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_market_sizes(self):
        """Ensure market sizes are logical."""
        if all([self.total_addressable_market, self.serviceable_addressable_market]):
            if self.serviceable_addressable_market > self.total_addressable_market:
                raise ValueError("SAM cannot be larger than TAM")
        if all(
            [self.serviceable_addressable_market, self.serviceable_obtainable_market]
        ):
            if self.serviceable_obtainable_market > self.serviceable_addressable_market:
                raise ValueError("SOM cannot be larger than SAM")
        return self


class CompetitorAnalysis(BaseModel):
    """Analysis of a specific competitor.

    Detailed competitive intelligence for strategic planning.
    """

    model_config = ConfigDict(extra="forbid")
    competitor_name: str = Field(..., description="Competitor name")
    website: str | None = Field(None, description="Competitor website")
    description: str = Field(..., description="What they do")
    founded_year: int | None = Field(None)
    funding_raised: float | None = Field(None, description="Total funding in USD")
    estimated_revenue: float | None = Field(None, description="Annual revenue in USD")
    employee_count: str | None = Field(None, description="Employee range")
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    market_share: float | None = Field(None, ge=0.0, le=1.0)
    customer_satisfaction: float | None = Field(None, ge=0.0, le=5.0)
    key_features: list[str] = Field(default_factory=list)
    pricing_model: str | None = Field(None)
    target_customers: list[str] = Field(default_factory=list)
    unique_selling_points: list[str] = Field(default_factory=list)
    recent_developments: list[str] = Field(default_factory=list)
    potential_threats: list[str] = Field(default_factory=list)
    opportunities_to_differentiate: list[str] = Field(default_factory=list)


class BusinessModelCanvas(BaseModel):
    """Business model canvas for startup ideas.

    Based on the standard Business Model Canvas framework.
    """

    model_config = ConfigDict(extra="forbid")
    value_propositions: list[str] = Field(..., description="Core value propositions")
    customer_segments: list[str] = Field(..., description="Target customer segments")
    channels: list[str] = Field(..., description="Distribution channels")
    customer_relationships: list[str] = Field(
        ..., description="How we maintain relationships"
    )
    revenue_streams: list[str] = Field(..., description="How we make money")
    key_resources: list[str] = Field(..., description="Essential resources needed")
    key_activities: list[str] = Field(..., description="Critical activities")
    key_partnerships: list[str] = Field(..., description="Important partners")
    cost_structure: list[str] = Field(..., description="Major cost categories")
    unfair_advantage: str | None = Field(
        None, description="Sustainable competitive advantage"
    )
    metrics: list[str] = Field(default_factory=list, description="Key metrics to track")

    @field_validator("value_propositions", "customer_segments", "revenue_streams")
    @classmethod
    def validate_required_lists(cls, v, info):
        """Ensure critical lists are not empty."""
        if not v:
            raise ValueError(f"{info.field_name} cannot be empty")
        return v


class RiskAssessment(BaseModel):
    """Risk assessment for a startup idea.

    Comprehensive risk analysis across multiple dimensions.
    """

    model_config = ConfigDict(extra="forbid")
    market_risk: RiskLevel = Field(
        ..., description="Risk of market not accepting solution"
    )
    technical_risk: RiskLevel = Field(..., description="Risk of technical challenges")
    financial_risk: RiskLevel = Field(..., description="Risk of running out of money")
    competitive_risk: RiskLevel = Field(..., description="Risk from competition")
    regulatory_risk: RiskLevel = Field(..., description="Risk from regulations")
    team_risk: RiskLevel = Field(..., description="Risk from team limitations")
    identified_risks: list[dict[str, Any]] = Field(
        default_factory=list, description="Specific risks with mitigation strategies"
    )
    overall_risk_level: RiskLevel = Field(...)
    risk_mitigation_strategies: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def calculate_overall_risk(self):
        """Calculate overall risk from individual components."""
        risk_values = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.VERY_HIGH: 4,
        }
        risks = [
            self.market_risk,
            self.technical_risk,
            self.financial_risk,
            self.competitive_risk,
            self.regulatory_risk,
            self.team_risk,
        ]
        avg_risk = sum((risk_values[r] for r in risks)) / len(risks)
        if avg_risk <= 1.5:
            self.overall_risk_level = RiskLevel.LOW
        elif avg_risk <= 2.5:
            self.overall_risk_level = RiskLevel.MEDIUM
        elif avg_risk <= 3.5:
            self.overall_risk_level = RiskLevel.HIGH
        else:
            self.overall_risk_level = RiskLevel.VERY_HIGH
        return self


class ValidationResult(BaseModel):
    """Results from idea validation activities.

    Tracks validation efforts and findings.
    """

    model_config = ConfigDict(extra="forbid")
    validation_id: str = Field(..., description="Unique validation identifier")
    method: ValidationMethod = Field(..., description="Validation method used")
    date_conducted: datetime = Field(default_factory=datetime.now)
    summary: str = Field(..., description="Summary of findings")
    key_insights: list[str] = Field(..., description="Key insights gained")
    supporting_data: dict[str, Any] = Field(default_factory=dict)
    sample_size: int | None = Field(
        None, description="Number of participants/data points"
    )
    response_rate: float | None = Field(None, ge=0.0, le=1.0)
    confidence_score: float = Field(0.5, ge=0.0, le=1.0)
    validates_hypothesis: bool | None = Field(None)
    pivot_recommendations: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)


class IdeaMetrics(BaseModel):
    """Metrics for evaluating startup ideas.

    Comprehensive scoring across multiple dimensions.
    """

    model_config = ConfigDict(extra="forbid")
    problem_severity: float = Field(..., ge=0.0, le=10.0)
    solution_uniqueness: float = Field(..., ge=0.0, le=10.0)
    market_opportunity: float = Field(..., ge=0.0, le=10.0)
    feasibility: float = Field(..., ge=0.0, le=10.0)
    scalability: float = Field(..., ge=0.0, le=10.0)
    founder_fit: float = Field(5.0, ge=0.0, le=10.0)
    timing: float = Field(5.0, ge=0.0, le=10.0)
    resource_requirements: float = Field(5.0, ge=0.0, le=10.0)
    overall_score: float | None = Field(None, ge=0.0, le=10.0)
    investment_readiness: float | None = Field(None, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def calculate_scores(self):
        """Calculate overall scores."""
        weights = {
            "problem_severity": 0.2,
            "solution_uniqueness": 0.2,
            "market_opportunity": 0.25,
            "feasibility": 0.2,
            "scalability": 0.15,
        }
        self.overall_score = sum(
            (getattr(self, metric) * weight for metric, weight in weights.items())
        )
        if self.overall_score >= 7.5 and self.feasibility >= 7:
            self.investment_readiness = 0.9
        elif self.overall_score >= 6.5:
            self.investment_readiness = 0.7
        elif self.overall_score >= 5:
            self.investment_readiness = 0.5
        else:
            self.investment_readiness = 0.3
        return self


class IdeaBrainstorm(BaseModel):
    """A brainstorming session for generating startup ideas.

    Tracks the ideation process and generated concepts.
    """

    model_config = ConfigDict(extra="forbid")
    session_id: str = Field(..., description="Unique session identifier")
    session_date: datetime = Field(default_factory=datetime.now)
    focus_areas: list[str] = Field(
        default_factory=list, description="Areas to focus on"
    )
    constraints: list[str] = Field(
        default_factory=list, description="Constraints to consider"
    )
    inspiration_sources: list[str] = Field(
        default_factory=list, description="Sources of inspiration"
    )
    participating_agents: list[str] = Field(
        default_factory=list, description="Agent IDs involved"
    )
    raw_ideas: list[str] = Field(
        default_factory=list, description="All generated ideas"
    )
    refined_ideas: list["StartupIdea"] = Field(
        default_factory=list, description="Refined idea objects"
    )
    techniques_used: list[str] = Field(
        default_factory=list, description="Brainstorming techniques"
    )
    session_notes: str = Field(default="", description="Notes from the session")

    def add_raw_idea(self, idea: str, agent_id: str | None = None) -> None:
        """Add a raw idea to the session."""
        self.raw_ideas.append(idea)
        if agent_id and agent_id not in self.participating_agents:
            self.participating_agents.append(agent_id)


class StartupIdea(BaseModel):
    """Complete startup idea with all research and validation.

    This is the main model that brings together all components of a startup idea.
    """

    model_config = ConfigDict(extra="forbid")
    idea_id: str = Field(..., description="Unique idea identifier")
    name: str = Field(..., description="Startup/product name")
    tagline: str = Field(..., description="One-line description")
    category: IdeaCategory = Field(..., description="Primary category")
    stage: IdeaStage = Field(default=IdeaStage.RAW_CONCEPT)
    problem: ProblemStatement = Field(..., description="Problem being solved")
    solution: SolutionConcept = Field(..., description="Proposed solution")
    market_research: MarketResearch | None = None
    competitor_analyses: list[CompetitorAnalysis] = Field(default_factory=list)
    business_model: BusinessModelCanvas | None = None
    risk_assessment: RiskAssessment | None = None
    validation_results: list[ValidationResult] = Field(default_factory=list)
    metrics: IdeaMetrics | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    contributing_agents: list[str] = Field(
        default_factory=list, description="Agents that contributed"
    )
    research_sources: list[str] = Field(
        default_factory=list, description="External sources used"
    )
    _research_tasks_completed: set[str] = PrivateAttr(default_factory=set)
    _validation_status: dict[str, bool] = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def update_timestamp(self):
        """Update timestamp on changes."""
        self.updated_at = datetime.now()
        return self

    def add_research(self, research_type: str, data: Any) -> None:
        """Add research data to the idea."""
        if research_type == "market":
            self.market_research = data
        elif research_type == "competitor":
            self.competitor_analyses.append(data)
        elif research_type == "business_model":
            self.business_model = data
        elif research_type == "risk":
            self.risk_assessment = data
        self._research_tasks_completed.add(research_type)
        self.updated_at = datetime.now()

    def add_validation(self, validation: ValidationResult) -> None:
        """Add validation results."""
        self.validation_results.append(validation)
        self._validation_status[validation.method.value] = (
            validation.validates_hypothesis or False
        )
        if len(self.validation_results) >= 3 and self.stage == IdeaStage.RESEARCHED:
            self.stage = IdeaStage.VALIDATED

    def calculate_readiness(self) -> dict[str, Any]:
        """Calculate how ready this idea is for next steps."""
        readiness = {
            "research_completeness": len(self._research_tasks_completed) / 5,
            "validation_completeness": len(self.validation_results) / 3,
            "has_business_model": self.business_model is not None,
            "has_risk_assessment": self.risk_assessment is not None,
            "has_metrics": self.metrics is not None,
            "overall_score": self.metrics.overall_score if self.metrics else 0,
        }
        readiness["overall_readiness"] = sum(
            [
                readiness["research_completeness"] * 0.3,
                readiness["validation_completeness"] * 0.3,
                readiness["has_business_model"] * 0.2,
                readiness["has_risk_assessment"] * 0.1,
                readiness["has_metrics"] * 0.1,
            ]
        )
        return readiness

    def to_pitch_deck_brief(self) -> dict[str, Any]:
        """Convert idea to a brief for pitch deck generation.

        This creates a structured brief that can be used by pitch deck agents.
        """
        return {
            "company_name": self.name,
            "tagline": self.tagline,
            "problem": {
                "description": self.problem.description,
                "pain_points": self.problem.pain_points,
                "affected_users": self.problem.affected_users,
            },
            "solution": {
                "description": self.solution.description,
                "key_features": self.solution.key_features,
                "value_proposition": self.solution.value_proposition,
            },
            "market": {
                "size": (
                    self.market_research.total_addressable_market
                    if self.market_research
                    else None
                ),
                "growth_rate": (
                    self.market_research.growth_rate if self.market_research else None
                ),
                "trends": (
                    self.market_research.market_trends if self.market_research else []
                ),
            },
            "business_model": {
                "revenue_streams": (
                    self.business_model.revenue_streams if self.business_model else []
                ),
                "key_metrics": (
                    self.business_model.metrics if self.business_model else []
                ),
            },
            "competition": [
                {
                    "name": comp.competitor_name,
                    "strengths": comp.strengths,
                    "weaknesses": comp.weaknesses,
                }
                for comp in self.competitor_analyses[:3]
            ],
            "metrics": self.metrics.model_dump() if self.metrics else None,
        }

    def get_research_gaps(self) -> list[str]:
        """Identify what research is still needed."""
        gaps = []
        if not self.market_research:
            gaps.append("Market research and sizing")
        elif not self.market_research.total_addressable_market:
            gaps.append("Market size estimation")
        if not self.competitor_analyses:
            gaps.append("Competitor analysis")
        elif len(self.competitor_analyses) < 3:
            gaps.append("Additional competitor research")
        if not self.business_model:
            gaps.append("Business model development")
        if not self.risk_assessment:
            gaps.append("Risk assessment")
        if not self.validation_results:
            gaps.append("Idea validation")
        elif len(self.validation_results) < 2:
            gaps.append("Additional validation methods")
        return gaps


class IdeaPortfolio(BaseModel):
    """Portfolio of startup ideas being developed.

    Manages multiple ideas and tracks their progress.
    """

    model_config = ConfigDict(extra="forbid")
    portfolio_id: str = Field(..., description="Unique portfolio identifier")
    name: str = Field(..., description="Portfolio name")
    description: str = Field(default="", description="Portfolio description")
    ideas: list[StartupIdea] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    focus_categories: list[IdeaCategory] = Field(default_factory=list)
    target_market_size: MarketSize | None = None
    max_ideas: int = Field(default=10, ge=1, le=50)

    def add_idea(self, idea: StartupIdea) -> bool:
        """Add an idea to the portfolio."""
        if len(self.ideas) >= self.max_ideas:
            return False
        self.ideas.append(idea)
        self.updated_at = datetime.now()
        return True

    def get_top_ideas(self, n: int = 3) -> list[StartupIdea]:
        """Get top N ideas by score."""
        scored_ideas = [
            idea for idea in self.ideas if idea.metrics and idea.metrics.overall_score
        ]
        return sorted(
            scored_ideas, key=lambda x: x.metrics.overall_score, reverse=True
        )[:n]

    def get_ideas_by_stage(self, stage: IdeaStage) -> list[StartupIdea]:
        """Get all ideas at a specific stage."""
        return [idea for idea in self.ideas if idea.stage == stage]

    def get_portfolio_summary(self) -> dict[str, Any]:
        """Get summary statistics of the portfolio."""
        return {
            "total_ideas": len(self.ideas),
            "ideas_by_stage": {
                stage.value: len(self.get_ideas_by_stage(stage)) for stage in IdeaStage
            },
            "ideas_by_category": {
                cat.value: sum((1 for idea in self.ideas if idea.category == cat))
                for cat in IdeaCategory
            },
            "validated_ideas": len(
                [
                    idea
                    for idea in self.ideas
                    if idea.stage
                    in [IdeaStage.VALIDATED, IdeaStage.PROTOTYPED, IdeaStage.MVP_READY]
                ]
            ),
            "average_score": sum(
                (
                    idea.metrics.overall_score
                    for idea in self.ideas
                    if idea.metrics and idea.metrics.overall_score
                )
            )
            / max(len(self.ideas), 1),
        }


def create_problem_from_description(
    description: str, severity: str = "high"
) -> ProblemStatement:
    """Create a problem statement from a simple description."""
    return ProblemStatement(
        problem_id=str(uuid.uuid4()),
        description=description,
        affected_users=["To be determined"],
        frequency="daily",
        severity=severity,
        pain_points=["To be researched"],
    )


def create_basic_idea(
    name: str, problem: str, solution: str, category: IdeaCategory
) -> StartupIdea:
    """Create a basic startup idea from minimal information."""
    problem_statement = create_problem_from_description(problem)
    solution_concept = SolutionConcept(
        solution_id=str(uuid.uuid4()),
        name=name,
        description=solution,
        key_features=["Feature 1", "Feature 2", "Feature 3"],
        value_proposition="To be defined",
        unique_aspects=["To be determined"],
    )
    return StartupIdea(
        idea_id=str(uuid.uuid4()),
        name=name,
        tagline=f"{name} - {solution[:50]}",
        category=category,
        problem=problem_statement,
        solution=solution_concept,
    )


class IdeaGenerationRequest(BaseModel):
    """Request model for idea generation."""

    focus_area: str | None = Field(
        None, description="Specific area to focus on (e.g., 'healthcare', 'education')"
    )
    target_audience: str | None = Field(None, description="Target audience for ideas")
    constraints: list[str] = Field(
        default_factory=list, description="Any constraints to consider"
    )
    num_ideas: int = Field(default=5, description="Number of ideas to generate")
    inspiration_keywords: list[str] = Field(
        default_factory=list, description="Keywords for inspiration"
    )


class IdeaGenerationResponse(BaseModel):
    """Response model for idea generation."""

    ideas: list[dict[str, Any]] = Field(..., description="Generated startup ideas")
    rationale: str = Field(..., description="Reasoning behind the ideas")
    market_trends: list[str] = Field(
        ..., description="Relevant market trends identified"
    )
