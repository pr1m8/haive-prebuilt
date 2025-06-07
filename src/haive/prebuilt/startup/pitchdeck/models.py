"""
Pitch deck models for the Haive framework.

This module provides comprehensive data models for creating, managing, and generating
pitch decks using AI agents. The models are designed to be composable, serializable,
and extensible, following Haive's dynamic architecture principles.

The models support:
- Complete pitch deck structure with slides and sections
- Content generation tracking and versioning
- Agent collaboration metadata
- Validation and quality scoring
- Export to various formats
"""

from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    field_validator,
    model_validator,
)
from typing_extensions import Annotated

# Type variables for generic content
TContent = TypeVar("TContent", bound=BaseModel)
TMetrics = TypeVar("TMetrics", bound=BaseModel)


class SlideType(str, Enum):
    """Types of slides commonly found in pitch decks."""

    TITLE = "title"
    PROBLEM = "problem"
    SOLUTION = "solution"
    MARKET_SIZE = "market_size"
    BUSINESS_MODEL = "business_model"
    COMPETITION = "competition"
    COMPETITIVE_ADVANTAGE = "competitive_advantage"
    GO_TO_MARKET = "go_to_market"
    TEAM = "team"
    TRACTION = "traction"
    FINANCIALS = "financials"
    FUNDRAISING = "fundraising"
    ROADMAP = "roadmap"
    CALL_TO_ACTION = "call_to_action"
    APPENDIX = "appendix"
    CUSTOM = "custom"


class ContentStatus(str, Enum):
    """Status of content generation."""

    PENDING = "pending"
    GENERATING = "generating"
    GENERATED = "generated"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_NEEDED = "revision_needed"


class DesignStyle(str, Enum):
    """Visual design styles for the pitch deck."""

    MINIMAL = "minimal"
    MODERN = "modern"
    CORPORATE = "corporate"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    PLAYFUL = "playful"
    ELEGANT = "elegant"
    BOLD = "bold"


class ExportFormat(str, Enum):
    """Supported export formats for pitch decks."""

    PDF = "pdf"
    PPTX = "pptx"
    GOOGLE_SLIDES = "google_slides"
    HTML = "html"
    MARKDOWN = "markdown"
    KEYNOTE = "keynote"


class DataPoint(BaseModel):
    """
    Represents a single data point that can be used in slides.

    This is useful for financial data, metrics, market statistics, etc.
    """

    model_config = ConfigDict(extra="forbid")

    label: str = Field(..., description="Label for the data point")
    value: Union[float, int, str] = Field(..., description="The actual value")
    unit: Optional[str] = Field(
        None, description="Unit of measurement (e.g., '$', '%', 'users')"
    )
    source: Optional[str] = Field(None, description="Source of the data")
    confidence: float = Field(
        1.0, ge=0.0, le=1.0, description="Confidence in the data accuracy"
    )
    timestamp: Optional[datetime] = Field(
        None, description="When this data point was recorded"
    )

    @property
    def formatted_value(self) -> str:
        """Get formatted value with unit."""
        if isinstance(self.value, (int, float)) and self.unit:
            return (
                f"{self.unit}{self.value:,}"
                if self.unit == "$"
                else f"{self.value:,} {self.unit}"
            )
        return str(self.value)


class ChartData(BaseModel):
    """Data structure for charts and visualizations."""

    model_config = ConfigDict(extra="forbid")

    chart_type: Literal["bar", "line", "pie", "scatter", "area", "combo"] = Field(
        ..., description="Type of chart"
    )
    title: str = Field(..., description="Chart title")
    data_points: List[DataPoint] = Field(
        default_factory=list, description="Data points for the chart"
    )
    x_axis_label: Optional[str] = Field(None, description="X-axis label")
    y_axis_label: Optional[str] = Field(None, description="Y-axis label")
    colors: Optional[List[str]] = Field(None, description="Color scheme for the chart")

    @field_validator("data_points")
    @classmethod
    def validate_data_points(cls, v):
        """Ensure we have at least one data point."""
        if not v:
            raise ValueError("Chart must have at least one data point")
        return v


class SlideContent(BaseModel):
    """
    Base content for a slide with common fields.

    This can be extended for specific slide types with additional fields.
    """

    model_config = ConfigDict(extra="forbid")

    headline: str = Field(..., description="Main headline for the slide")
    subheadline: Optional[str] = Field(None, description="Supporting subheadline")
    body_text: Optional[str] = Field(None, description="Main body text content")
    bullet_points: List[str] = Field(
        default_factory=list, description="Bullet points for the slide"
    )
    call_to_action: Optional[str] = Field(None, description="Call to action text")
    speaker_notes: Optional[str] = Field(None, description="Notes for the presenter")

    # Visual elements
    images: List[str] = Field(
        default_factory=list, description="URLs or paths to images"
    )
    charts: List[ChartData] = Field(
        default_factory=list, description="Charts to display"
    )
    icons: List[str] = Field(
        default_factory=list, description="Icon identifiers to use"
    )

    @field_validator("headline")
    @classmethod
    def validate_headline(cls, v):
        """Ensure headline is not too long."""
        if len(v) > 100:
            raise ValueError("Headline should be concise (max 100 characters)")
        return v


class TeamMember(BaseModel):
    """Information about a team member."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Full name")
    role: str = Field(..., description="Role/title in the company")
    bio: str = Field(..., max_length=500, description="Short biography")
    expertise: List[str] = Field(default_factory=list, description="Areas of expertise")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    photo_url: Optional[str] = Field(None, description="Photo URL")
    key_achievements: List[str] = Field(
        default_factory=list, description="Notable achievements"
    )


class FinancialMetrics(BaseModel):
    """Financial metrics and projections."""

    model_config = ConfigDict(extra="forbid")

    revenue_current: Optional[DataPoint] = None
    revenue_projected: List[DataPoint] = Field(default_factory=list)
    burn_rate: Optional[DataPoint] = None
    runway_months: Optional[float] = None
    gross_margin: Optional[float] = Field(None, ge=0.0, le=1.0)
    customer_acquisition_cost: Optional[DataPoint] = None
    lifetime_value: Optional[DataPoint] = None

    @model_validator(mode="after")
    def validate_metrics(self):
        """Validate financial metrics relationships."""
        if self.customer_acquisition_cost and self.lifetime_value:
            cac_value = float(self.customer_acquisition_cost.value)
            ltv_value = float(self.lifetime_value.value)
            if cac_value > ltv_value:
                # Just a warning, not an error - might be early stage
                pass
        return self


class AgentMetadata(BaseModel):
    """
    Metadata about agent contributions to content generation.

    Tracks which agents contributed to what content for auditing and improvement.
    """

    model_config = ConfigDict(extra="forbid")

    agent_id: str = Field(
        ..., description="ID of the agent that generated/modified content"
    )
    agent_type: str = Field(
        ..., description="Type of agent (e.g., 'content_writer', 'data_analyst')"
    )
    action: str = Field(
        ..., description="Action performed (e.g., 'generated', 'revised', 'validated')"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When the action occurred"
    )
    confidence_score: float = Field(
        1.0, ge=0.0, le=1.0, description="Agent's confidence in its output"
    )
    reasoning: Optional[str] = Field(
        None, description="Agent's reasoning for decisions made"
    )
    tool_calls: List[str] = Field(
        default_factory=list, description="Tools used by the agent"
    )


class SlideRevision(BaseModel):
    """Tracks revisions to a slide."""

    model_config = ConfigDict(extra="forbid")

    revision_id: str = Field(..., description="Unique revision identifier")
    timestamp: datetime = Field(default_factory=datetime.now)
    previous_content: Optional[SlideContent] = None
    changes_made: List[str] = Field(
        default_factory=list, description="Description of changes"
    )
    agent_metadata: Optional[AgentMetadata] = None
    reason: Optional[str] = Field(None, description="Reason for revision")


class Slide(BaseModel, Generic[TContent]):
    """
    A single slide in the pitch deck.

    Generic over content type to allow specialized slide content while
    maintaining type safety.
    """

    model_config = ConfigDict(extra="forbid")

    slide_id: str = Field(..., description="Unique identifier for the slide")
    slide_type: SlideType = Field(..., description="Type of slide")
    order: int = Field(..., ge=0, description="Order in the deck (0-indexed)")
    title: str = Field(..., description="Slide title")

    # Content - generic to allow different content types
    content: TContent = Field(..., description="Slide content")

    # Status tracking
    status: ContentStatus = Field(default=ContentStatus.PENDING)
    quality_score: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Quality assessment score"
    )

    # Design elements
    layout: str = Field(default="standard", description="Layout template to use")
    color_scheme: Optional[Dict[str, str]] = Field(
        None, description="Custom color overrides"
    )
    animation_style: Optional[str] = Field(
        None, description="Animation/transition style"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    agent_metadata: List[AgentMetadata] = Field(default_factory=list)
    revisions: List[SlideRevision] = Field(default_factory=list)

    # Private attributes for runtime state
    _validation_errors: List[str] = PrivateAttr(default_factory=list)
    _generation_attempts: int = PrivateAttr(default=0)

    @model_validator(mode="after")
    def update_timestamp(self):
        """Update timestamp when model is modified."""
        self.updated_at = datetime.now()
        return self

    def add_agent_contribution(self, agent_metadata: AgentMetadata) -> None:
        """Track agent contribution to this slide."""
        self.agent_metadata.append(agent_metadata)
        self.updated_at = datetime.now()

    def validate_content(self) -> List[str]:
        """
        Validate slide content and return any issues.

        Override in subclasses for specific validation rules.
        """
        errors = []
        if not self.content.headline:
            errors.append("Slide must have a headline")
        if self.slide_type != SlideType.CUSTOM and not self.title:
            errors.append("Slide must have a title")

        self._validation_errors = errors
        return errors


class PitchDeckMetadata(BaseModel):
    """Metadata about the pitch deck."""

    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., description="Name of the company")
    tagline: Optional[str] = Field(None, description="Company tagline")
    industry: str = Field(..., description="Industry/sector")
    stage: Literal[
        "idea", "pre_seed", "seed", "series_a", "series_b", "series_c", "later"
    ] = Field(...)

    # Fundraising details
    funding_amount_sought: Optional[DataPoint] = None
    valuation: Optional[DataPoint] = None
    use_of_funds: List[Dict[str, Any]] = Field(default_factory=list)

    # Deck metadata
    version: str = Field(default="1.0.0")
    language: str = Field(default="en")
    confidential: bool = Field(default=True)

    # Target audience
    target_audience: List[str] = Field(
        default_factory=lambda: ["investors"], description="Who this deck is for"
    )

    # Design preferences
    design_style: DesignStyle = Field(default=DesignStyle.MODERN)
    brand_colors: Optional[Dict[str, str]] = Field(
        None, description="Brand color palette"
    )
    font_preferences: Optional[Dict[str, str]] = Field(
        None, description="Font preferences"
    )


class QualityMetrics(BaseModel):
    """Metrics for assessing pitch deck quality."""

    model_config = ConfigDict(extra="forbid")

    clarity_score: float = Field(
        ..., ge=0.0, le=1.0, description="How clear the message is"
    )
    completeness_score: float = Field(
        ..., ge=0.0, le=1.0, description="How complete the deck is"
    )
    visual_appeal_score: float = Field(
        ..., ge=0.0, le=1.0, description="Visual design quality"
    )
    data_credibility_score: float = Field(
        ..., ge=0.0, le=1.0, description="Credibility of data/claims"
    )
    storytelling_score: float = Field(
        ..., ge=0.0, le=1.0, description="Narrative flow quality"
    )

    @property
    def overall_score(self) -> float:
        """Calculate overall quality score."""
        scores = [
            self.clarity_score,
            self.completeness_score,
            self.visual_appeal_score,
            self.data_credibility_score,
            self.storytelling_score,
        ]
        return sum(scores) / len(scores)

    def get_improvement_areas(self) -> List[str]:
        """Identify areas needing improvement."""
        areas = []
        if self.clarity_score < 0.7:
            areas.append("Message clarity needs improvement")
        if self.completeness_score < 0.8:
            areas.append("Deck is missing important sections")
        if self.visual_appeal_score < 0.6:
            areas.append("Visual design could be enhanced")
        if self.data_credibility_score < 0.7:
            areas.append("Data sources and credibility need strengthening")
        if self.storytelling_score < 0.7:
            areas.append("Narrative flow could be improved")
        return areas


class PitchDeck(BaseModel):
    """
    Complete pitch deck model.

    This is the main model that contains all slides and orchestrates
    the pitch deck creation process.
    """

    model_config = ConfigDict(extra="forbid")

    deck_id: str = Field(..., description="Unique identifier for the pitch deck")
    metadata: PitchDeckMetadata = Field(..., description="Deck metadata")

    # Slides - using Union to support different content types
    slides: List[Slide[SlideContent]] = Field(default_factory=list)

    # Status and quality
    status: ContentStatus = Field(default=ContentStatus.PENDING)
    quality_metrics: Optional[QualityMetrics] = None

    # Generation tracking
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    generation_config: Dict[str, Any] = Field(default_factory=dict)

    # Agent collaboration
    agent_contributions: List[AgentMetadata] = Field(default_factory=list)

    # Private attributes
    _slide_index: Dict[str, int] = PrivateAttr(default_factory=dict)
    _generation_stats: Dict[str, Any] = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def validate_deck(self):
        """Validate deck structure and update indices."""
        # Update slide index
        self._slide_index = {slide.slide_id: i for i, slide in enumerate(self.slides)}

        # Check for required slides
        slide_types = {slide.slide_type for slide in self.slides}
        required_types = {SlideType.TITLE, SlideType.PROBLEM, SlideType.SOLUTION}

        missing = required_types - slide_types
        if missing and self.status != ContentStatus.PENDING:
            # Just a warning during generation
            pass

        return self

    def add_slide(
        self, slide: Slide[SlideContent], position: Optional[int] = None
    ) -> None:
        """Add a slide to the deck."""
        if position is None:
            self.slides.append(slide)
        else:
            self.slides.insert(position, slide)

        # Update order
        for i, s in enumerate(self.slides):
            s.order = i

        self.updated_at = datetime.now()
        self._slide_index[slide.slide_id] = position or len(self.slides) - 1

    def get_slide_by_type(self, slide_type: SlideType) -> Optional[Slide[SlideContent]]:
        """Get the first slide of a given type."""
        for slide in self.slides:
            if slide.slide_type == slide_type:
                return slide
        return None

    def get_slides_by_status(self, status: ContentStatus) -> List[Slide[SlideContent]]:
        """Get all slides with a specific status."""
        return [slide for slide in self.slides if slide.status == status]

    def calculate_completion_percentage(self) -> float:
        """Calculate how complete the deck is."""
        if not self.slides:
            return 0.0

        completed = sum(
            1 for slide in self.slides if slide.status == ContentStatus.APPROVED
        )
        return (completed / len(self.slides)) * 100

    def get_next_slide_to_generate(self) -> Optional[Slide[SlideContent]]:
        """Get the next slide that needs generation."""
        for slide in self.slides:
            if slide.status in [ContentStatus.PENDING, ContentStatus.REVISION_NEEDED]:
                return slide
        return None

    def export_config(self, format: ExportFormat) -> Dict[str, Any]:
        """
        Generate export configuration for the specified format.

        Returns configuration that can be used by export agents.
        """
        config = {
            "format": format.value,
            "deck_id": self.deck_id,
            "company_name": self.metadata.company_name,
            "design_style": self.metadata.design_style.value,
            "include_speaker_notes": True,
            "include_appendix": any(
                s.slide_type == SlideType.APPENDIX for s in self.slides
            ),
        }

        if format == ExportFormat.PDF:
            config["page_size"] = "16:9"
            config["include_animations"] = False
        elif format == ExportFormat.PPTX:
            config["template"] = "modern"
            config["include_animations"] = True

        return config

    def to_review_format(self) -> Dict[str, Any]:
        """
        Convert deck to a format suitable for review.

        Returns a simplified version for review agents or humans.
        """
        return {
            "deck_id": self.deck_id,
            "company": self.metadata.company_name,
            "stage": self.metadata.stage,
            "total_slides": len(self.slides),
            "completion": f"{self.calculate_completion_percentage():.1f}%",
            "slides": [
                {
                    "order": slide.order,
                    "type": slide.slide_type.value,
                    "title": slide.title,
                    "headline": slide.content.headline,
                    "status": slide.status.value,
                    "quality_score": slide.quality_score,
                }
                for slide in self.slides
            ],
            "quality_metrics": (
                self.quality_metrics.model_dump() if self.quality_metrics else None
            ),
        }


class PitchDeckTemplate(BaseModel):
    """
    Template for creating pitch decks.

    Defines the structure and requirements for a type of pitch deck.
    """

    model_config = ConfigDict(extra="forbid")

    template_id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")

    # Slide structure
    slide_templates: List[Dict[str, Any]] = Field(
        ..., description="Ordered list of slide templates"
    )

    # Requirements
    min_slides: int = Field(default=10, ge=1)
    max_slides: int = Field(default=20, le=30)
    required_slide_types: List[SlideType] = Field(default_factory=list)

    # Styling
    default_design_style: DesignStyle = Field(default=DesignStyle.MODERN)
    color_schemes: List[Dict[str, str]] = Field(default_factory=list)

    # Target use case
    best_for_stage: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)

    def create_deck_scaffold(self, metadata: PitchDeckMetadata) -> PitchDeck:
        """Create a new pitch deck scaffold from this template."""
        import uuid

        deck = PitchDeck(deck_id=str(uuid.uuid4()), metadata=metadata)

        # Create slides from template
        for i, slide_template in enumerate(self.slide_templates):
            slide = Slide[SlideContent](
                slide_id=str(uuid.uuid4()),
                slide_type=SlideType(slide_template["type"]),
                order=i,
                title=slide_template.get("title", ""),
                content=SlideContent(
                    headline=slide_template.get("default_headline", ""),
                    body_text=slide_template.get("instructions", ""),
                ),
                status=ContentStatus.PENDING,
            )
            deck.slides.append(slide)

        return deck


# Example specialized slide content for specific use cases
class FinancialSlideContent(SlideContent):
    """Specialized content for financial slides."""

    revenue_chart: Optional[ChartData] = None
    expense_breakdown: Optional[ChartData] = None
    financial_metrics: Optional[FinancialMetrics] = None
    projections_timeline: str = Field(default="3-5 years")
    key_assumptions: List[str] = Field(default_factory=list)


class TeamSlideContent(SlideContent):
    """Specialized content for team slides."""

    team_members: List[TeamMember] = Field(default_factory=list)
    advisors: List[TeamMember] = Field(default_factory=list)
    organizational_structure: Optional[str] = None
    hiring_plans: List[str] = Field(default_factory=list)
    culture_values: List[str] = Field(default_factory=list)


# Type aliases for common slide types
StandardSlide = Slide[SlideContent]
FinancialSlide = Slide[FinancialSlideContent]
TeamSlide = Slide[TeamSlideContent]
