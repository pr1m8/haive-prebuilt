from typing import Any

from haive.core.engine.aug_llm.config import AugLLMConfig, AzureLLMConfig
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

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

    pitch_deck_content: dict[str, Any]


class PitchDeckFeedback(BaseModel):
    """Feedback for a pitch deck."""

    overall_score: float = Field(..., ge=0.0, le=10.0)
    strengths: list[str]
    weaknesses: list[str]
    improvement_suggestions: list[dict[str, str]]  # slide -> suggestion
    missing_elements: list[str]
    investor_concerns: list[str]
    revised_narrative: str | None = None


pitch_deck_review_aug_llm = AugLLMConfig(
    name="pitch_deck_review_agent",
    prompt_template=pitch_deck_review_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.4),
    structured_output_model=PitchDeckFeedback,
    system_message=PITCH_DECK_REVIEW_SYSTEM_PROMPT,
)
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
    funding_amount: float | None = None
    startup_brief: dict[str, Any]


class SlideOutline(BaseModel):
    """Outline for a single slide."""

    slide_type: SlideType
    title: str
    headline: str
    key_points: list[str]
    visual_suggestions: list[str]
    speaker_notes: str


class PitchDeckOutlineResponse(BaseModel):
    """Complete pitch deck outline."""

    slides: list[SlideOutline]
    narrative_flow: str
    key_messages: list[str]
    design_recommendations: list[str]


pitch_deck_outline_aug_llm = AugLLMConfig(
    name="pitch_deck_outline_agent",
    prompt_template=pitch_deck_outline_prompt,
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.6),
    structured_output_model=PitchDeckOutlineResponse,
    system_message=PITCH_DECK_OUTLINE_SYSTEM_PROMPT,
)
