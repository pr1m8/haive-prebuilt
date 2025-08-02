"""Pitch deck models for the Haive framework.

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
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Generic, Literal, TypeVar
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator, model_validator
TContent = TypeVar('TContent', bound=BaseModel)
TMetrics = TypeVar('TMetrics', bound=BaseModel)

class SlideType(str, Enum):
    """Types of slides commonly found in pitch decks."""
    TITLE = 'title'
    PROBLEM = 'problem'
    SOLUTION = 'solution'
    MARKET_SIZE = 'market_size'
    BUSINESS_MODEL = 'business_model'
    COMPETITION = 'competition'
    COMPETITIVE_ADVANTAGE = 'competitive_advantage'
    GO_TO_MARKET = 'go_to_market'
    TEAM = 'team'
    TRACTION = 'traction'
    FINANCIALS = 'financials'
    FUNDRAISING = 'fundraising'
    ROADMAP = 'roadmap'
    CALL_TO_ACTION = 'call_to_action'
    APPENDIX = 'appendix'
    CUSTOM = 'custom'

class ContentStatus(str, Enum):
    """Status of content generation."""
    PENDING = 'pending'
    GENERATING = 'generating'
    GENERATED = 'generated'
    REVIEWING = 'reviewing'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    REVISION_NEEDED = 'revision_needed'

class DesignStyle(str, Enum):
    """Visual design styles for the pitch deck."""
    MINIMAL = 'minimal'
    MODERN = 'modern'
    CORPORATE = 'corporate'
    CREATIVE = 'creative'
    TECHNICAL = 'technical'
    PLAYFUL = 'playful'
    ELEGANT = 'elegant'
    BOLD = 'bold'

class ExportFormat(str, Enum):
    """Supported export formats for pitch decks."""
    PDF = 'pdf'
    PPTX = 'pptx'
    GOOGLE_SLIDES = 'google_slides'
    HTML = 'html'
    MARKDOWN = 'markdown'
    KEYNOTE = 'keynote'

class DataPoint(BaseModel):
    """Represents a single data point that can be used in slides.

    This is useful for financial data, metrics, market statistics, etc.
    """
    model_config = ConfigDict(extra='forbid')
    label: str = Field(..., description='Label for the data point')
    value: float | int | str = Field(..., description='The actual value')
    unit: str | None = Field(None, description="Unit of measurement (e.g., '$', '%', 'users')")
    source: str | None = Field(None, description='Source of the data')
    confidence: float = Field(1.0, ge=0.0, le=1.0, description='Confidence in the data accuracy')
    timestamp: datetime | None = Field(None, description='When this data point was recorded')

    @property
    def formatted_value(self) -> str:
        """Get formatted value with unit."""
        if isinstance(self.value, (int, float)) and self.unit:
            return f'{self.unit}{self.value:,}' if self.unit == '$' else f'{self.value:,} {self.unit}'
        return str(self.value)

class ChartData(BaseModel):
    """Data structure for charts and visualizations."""
    model_config = ConfigDict(extra='forbid')
    chart_type: Literal['bar', 'line', 'pie', 'scatter', 'area', 'combo'] = Field(..., description='Type of chart')
    title: str = Field(..., description='Chart title')
    data_points: list[DataPoint] = Field(default_factory=list, description='Data points for the chart')
    x_axis_label: str | None = Field(None, description='X-axis label')
    y_axis_label: str | None = Field(None, description='Y-axis label')
    colors: list[str] | None = Field(None, description='Color scheme for the chart')

    @field_validator('data_points')
    @classmethod
    def validate_data_points(cls, v):
        """Ensure we have at least one data point."""
        if not v:
            raise ValueError('Chart must have at least one data point')
        return v

class SlideContent(BaseModel):
    """Base content for a slide with common fields.

    This can be extended for specific slide types with additional fields.
    """
    model_config = ConfigDict(extra='forbid')
    headline: str = Field(..., description='Main headline for the slide')
    subheadline: str | None = Field(None, description='Supporting subheadline')
    body_text: str | None = Field(None, description='Main body text content')
    bullet_points: list[str] = Field(default_factory=list, description='Bullet points for the slide')
    call_to_action: str | None = Field(None, description='Call to action text')
    speaker_notes: str | None = Field(None, description='Notes for the presenter')
    images: list[str] = Field(default_factory=list, description='URLs or paths to images')
    charts: list[ChartData] = Field(default_factory=list, description='Charts to display')
    icons: list[str] = Field(default_factory=list, description='Icon identifiers to use')

    @field_validator('headline')
    @classmethod
    def validate_headline(cls, v):
        """Ensure headline is not too long."""
        if len(v) > 100:
            raise ValueError('Headline should be concise (max 100 characters)')
        return v

class TeamMember(BaseModel):
    """Information about a team member."""
    model_config = ConfigDict(extra='forbid')
    name: str = Field(..., description='Full name')
    role: str = Field(..., description='Role/title in the company')
    bio: str = Field(..., max_length=500, description='Short biography')
    expertise: list[str] = Field(default_factory=list, description='Areas of expertise')
    linkedin_url: str | None = Field(None, description='LinkedIn profile URL')
    photo_url: str | None = Field(None, description='Photo URL')
    key_achievements: list[str] = Field(default_factory=list, description='Notable achievements')

class FinancialMetrics(BaseModel):
    """Financial metrics and projections."""
    model_config = ConfigDict(extra='forbid')
    revenue_current: DataPoint | None = None
    revenue_projected: list[DataPoint] = Field(default_factory=list)
    burn_rate: DataPoint | None = None
    runway_months: float | None = None
    gross_margin: float | None = Field(None, ge=0.0, le=1.0)
    customer_acquisition_cost: DataPoint | None = None
    lifetime_value: DataPoint | None = None

    @model_validator(mode='after')
    def validate_metrics(self):
        """Validate financial metrics relationships."""
        if self.customer_acquisition_cost and self.lifetime_value:
            cac_value = float(self.customer_acquisition_cost.value)
            ltv_value = float(self.lifetime_value.value)
            if cac_value > ltv_value:
                pass
        return self

class AgentMetadata(BaseModel):
    """Metadata about agent contributions to content generation.

    Tracks which agents contributed to what content for auditing and improvement.
    """
    model_config = ConfigDict(extra='forbid')
    agent_id: str = Field(..., description='ID of the agent that generated/modified content')
    agent_type: str = Field(..., description="Type of agent (e.g., 'content_writer', 'data_analyst')")
    action: str = Field(..., description="Action performed (e.g., 'generated', 'revised', 'validated')")
    timestamp: datetime = Field(default_factory=datetime.now, description='When the action occurred')
    confidence_score: float = Field(1.0, ge=0.0, le=1.0, description="Agent's confidence in its output")
    reasoning: str | None = Field(None, description="Agent's reasoning for decisions made")
    tool_calls: list[str] = Field(default_factory=list, description='Tools used by the agent')

class SlideRevision(BaseModel):
    """Tracks revisions to a slide."""
    model_config = ConfigDict(extra='forbid')
    revision_id: str = Field(..., description='Unique revision identifier')
    timestamp: datetime = Field(default_factory=datetime.now)
    previous_content: SlideContent | None = None
    changes_made: list[str] = Field(default_factory=list, description='Description of changes')
    agent_metadata: AgentMetadata | None = None
    reason: str | None = Field(None, description='Reason for revision')

class Slide(BaseModel, Generic[TContent]):
    """A single slide in the pitch deck.

    Generic over content type to allow specialized slide content while
    maintaining type safety.
    """
    model_config = ConfigDict(extra='forbid')
    slide_id: str = Field(..., description='Unique identifier for the slide')
    slide_type: SlideType = Field(..., description='Type of slide')
    order: int = Field(..., ge=0, description='Order in the deck (0-indexed)')
    title: str = Field(..., description='Slide title')
    content: TContent = Field(..., description='Slide content')
    status: ContentStatus = Field(default=ContentStatus.PENDING)
    quality_score: float | None = Field(None, ge=0.0, le=1.0, description='Quality assessment score')
    layout: str = Field(default='standard', description='Layout template to use')
    color_scheme: dict[str, str] | None = Field(None, description='Custom color overrides')
    animation_style: str | None = Field(None, description='Animation/transition style')
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    agent_metadata: list[AgentMetadata] = Field(default_factory=list)
    revisions: list[SlideRevision] = Field(default_factory=list)
    _validation_errors: list[str] = PrivateAttr(default_factory=list)
    _generation_attempts: int = PrivateAttr(default=0)

    @model_validator(mode='after')
    def update_timestamp(self):
        """Update timestamp when model is modified."""
        self.updated_at = datetime.now()
        return self

    def add_agent_contribution(self, agent_metadata: AgentMetadata) -> None:
        """Track agent contribution to this slide."""
        self.agent_metadata.append(agent_metadata)
        self.updated_at = datetime.now()

    def validate_content(self) -> list[str]:
        """Validate slide content and return any issues.

        Override in subclasses for specific validation rules.
        """
        errors = []
        if not self.content.headline:
            errors.append('Slide must have a headline')
        if self.slide_type != SlideType.CUSTOM and (not self.title):
            errors.append('Slide must have a title')
        self._validation_errors = errors
        return errors

class PitchDeckMetadata(BaseModel):
    """Metadata about the pitch deck."""
    model_config = ConfigDict(extra='forbid')
    company_name: str = Field(..., description='Name of the company')
    tagline: str | None = Field(None, description='Company tagline')
    industry: str = Field(..., description='Industry/sector')
    stage: Literal['idea', 'pre_seed', 'seed', 'series_a', 'series_b', 'series_c', 'later'] = Field(...)
    funding_amount_sought: DataPoint | None = None
    valuation: DataPoint | None = None
    use_of_funds: list[dict[str, Any]] = Field(default_factory=list)
    version: str = Field(default='1.0.0')
    language: str = Field(default='en')
    confidential: bool = Field(default=True)
    target_audience: list[str] = Field(default_factory=lambda: ['investors'], description='Who this deck is for')
    design_style: DesignStyle = Field(default=DesignStyle.MODERN)
    brand_colors: dict[str, str] | None = Field(None, description='Brand color palette')
    font_preferences: dict[str, str] | None = Field(None, description='Font preferences')

class QualityMetrics(BaseModel):
    """Metrics for assessing pitch deck quality."""
    model_config = ConfigDict(extra='forbid')
    clarity_score: float = Field(..., ge=0.0, le=1.0, description='How clear the message is')
    completeness_score: float = Field(..., ge=0.0, le=1.0, description='How complete the deck is')
    visual_appeal_score: float = Field(..., ge=0.0, le=1.0, description='Visual design quality')
    data_credibility_score: float = Field(..., ge=0.0, le=1.0, description='Credibility of data/claims')
    storytelling_score: float = Field(..., ge=0.0, le=1.0, description='Narrative flow quality')

    @property
    def overall_score(self) -> float:
        """Calculate overall quality score."""
        scores = [self.clarity_score, self.completeness_score, self.visual_appeal_score, self.data_credibility_score, self.storytelling_score]
        return sum(scores) / len(scores)

    def get_improvement_areas(self) -> list[str]:
        """Identify areas needing improvement."""
        areas = []
        if self.clarity_score < 0.7:
            areas.append('Message clarity needs improvement')
        if self.completeness_score < 0.8:
            areas.append('Deck is missing important sections')
        if self.visual_appeal_score < 0.6:
            areas.append('Visual design could be enhanced')
        if self.data_credibility_score < 0.7:
            areas.append('Data sources and credibility need strengthening')
        if self.storytelling_score < 0.7:
            areas.append('Narrative flow could be improved')
        return areas

class PitchDeck(BaseModel):
    """Complete pitch deck model.

    This is the main model that contains all slides and orchestrates
    the pitch deck creation process.
    """
    model_config = ConfigDict(extra='forbid')
    deck_id: str = Field(..., description='Unique identifier for the pitch deck')
    metadata: PitchDeckMetadata = Field(..., description='Deck metadata')
    slides: list[Slide[SlideContent]] = Field(default_factory=list)
    status: ContentStatus = Field(default=ContentStatus.PENDING)
    quality_metrics: QualityMetrics | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    generation_config: dict[str, Any] = Field(default_factory=dict)
    agent_contributions: list[AgentMetadata] = Field(default_factory=list)
    _slide_index: dict[str, int] = PrivateAttr(default_factory=dict)
    _generation_stats: dict[str, Any] = PrivateAttr(default_factory=dict)

    @model_validator(mode='after')
    def validate_deck(self):
        """Validate deck structure and update indices."""
        self._slide_index = {slide.slide_id: i for i, slide in enumerate(self.slides)}
        slide_types = {slide.slide_type for slide in self.slides}
        required_types = {SlideType.TITLE, SlideType.PROBLEM, SlideType.SOLUTION}
        missing = required_types - slide_types
        if missing and self.status != ContentStatus.PENDING:
            pass
        return self

    def add_slide(self, slide: Slide[SlideContent], position: int | None=None) -> None:
        """Add a slide to the deck."""
        if position is None:
            self.slides.append(slide)
        else:
            self.slides.insert(position, slide)
        for i, s in enumerate(self.slides):
            s.order = i
        self.updated_at = datetime.now()
        self._slide_index[slide.slide_id] = position or len(self.slides) - 1

    def get_slide_by_type(self, slide_type: SlideType) -> Slide[SlideContent] | None:
        """Get the first slide of a given type."""
        for slide in self.slides:
            if slide.slide_type == slide_type:
                return slide
        return None

    def get_slides_by_status(self, status: ContentStatus) -> list[Slide[SlideContent]]:
        """Get all slides with a specific status."""
        return [slide for slide in self.slides if slide.status == status]

    def calculate_completion_percentage(self) -> float:
        """Calculate how complete the deck is."""
        if not self.slides:
            return 0.0
        completed = sum((1 for slide in self.slides if slide.status == ContentStatus.APPROVED))
        return completed / len(self.slides) * 100

    def get_next_slide_to_generate(self) -> Slide[SlideContent] | None:
        """Get the next slide that needs generation."""
        for slide in self.slides:
            if slide.status in [ContentStatus.PENDING, ContentStatus.REVISION_NEEDED]:
                return slide
        return None

    def export_config(self, format: ExportFormat) -> dict[str, Any]:
        """Generate export configuration for the specified format.

        Returns configuration that can be used by export agents.
        """
        config = {'format': format.value, 'deck_id': self.deck_id, 'company_name': self.metadata.company_name, 'design_style': self.metadata.design_style.value, 'include_speaker_notes': True, 'include_appendix': any((s.slide_type == SlideType.APPENDIX for s in self.slides))}
        if format == ExportFormat.PDF:
            config['page_size'] = '16:9'
            config['include_animations'] = False
        elif format == ExportFormat.PPTX:
            config['template'] = 'modern'
            config['include_animations'] = True
        return config

    def to_review_format(self) -> dict[str, Any]:
        """Convert deck to a format suitable for review.

        Returns a simplified version for review agents or humans.
        """
        return {'deck_id': self.deck_id, 'company': self.metadata.company_name, 'stage': self.metadata.stage, 'total_slides': len(self.slides), 'completion': f'{self.calculate_completion_percentage():.1f}%', 'slides': [{'order': slide.order, 'type': slide.slide_type.value, 'title': slide.title, 'headline': slide.content.headline, 'status': slide.status.value, 'quality_score': slide.quality_score} for slide in self.slides], 'quality_metrics': self.quality_metrics.model_dump() if self.quality_metrics else None}

class PitchDeckTemplate(BaseModel):
    """Template for creating pitch decks.

    Defines the structure and requirements for a type of pitch deck.
    """
    model_config = ConfigDict(extra='forbid')
    template_id: str = Field(..., description='Unique template identifier')
    name: str = Field(..., description='Template name')
    description: str = Field(..., description='Template description')
    slide_templates: list[dict[str, Any]] = Field(..., description='Ordered list of slide templates')
    min_slides: int = Field(default=10, ge=1)
    max_slides: int = Field(default=20, le=30)
    required_slide_types: list[SlideType] = Field(default_factory=list)
    default_design_style: DesignStyle = Field(default=DesignStyle.MODERN)
    color_schemes: list[dict[str, str]] = Field(default_factory=list)
    best_for_stage: list[str] = Field(default_factory=list)
    industries: list[str] = Field(default_factory=list)

    def create_deck_scaffold(self, metadata: PitchDeckMetadata) -> PitchDeck:
        """Create a new pitch deck scaffold from this template."""
        deck = PitchDeck(deck_id=str(uuid.uuid4()), metadata=metadata)
        for i, slide_template in enumerate(self.slide_templates):
            slide = Slide[SlideContent](slide_id=str(uuid.uuid4()), slide_type=SlideType(slide_template['type']), order=i, title=slide_template.get('title', ''), content=SlideContent(headline=slide_template.get('default_headline', ''), body_text=slide_template.get('instructions', '')), status=ContentStatus.PENDING)
            deck.slides.append(slide)
        return deck

class FinancialSlideContent(SlideContent):
    """Specialized content for financial slides."""
    revenue_chart: ChartData | None = None
    expense_breakdown: ChartData | None = None
    financial_metrics: FinancialMetrics | None = None
    projections_timeline: str = Field(default='3-5 years')
    key_assumptions: list[str] = Field(default_factory=list)

class TeamSlideContent(SlideContent):
    """Specialized content for team slides."""
    team_members: list[TeamMember] = Field(default_factory=list)
    advisors: list[TeamMember] = Field(default_factory=list)
    organizational_structure: str | None = None
    hiring_plans: list[str] = Field(default_factory=list)
    culture_values: list[str] = Field(default_factory=list)
StandardSlide = Slide[SlideContent]
FinancialSlide = Slide[FinancialSlideContent]
TeamSlide = Slide[TeamSlideContent]