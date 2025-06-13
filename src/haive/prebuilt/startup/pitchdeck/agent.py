"""
Pitch deck generation subgraph for creating compelling pitch decks.

This subgraph handles the creation of pitch deck outlines, slide content,
and deck refinement.
"""

from typing import Any, Dict, List, Literal, Optional

from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from haive.prebuilt.startup.ideation.models import StartupIdea
from haive.prebuilt.startup.pitchdeck.models import (
    DesignStyle,
    PitchDeck,
    PitchDeckMetadata,
    QualityMetrics,
    Slide,
    SlideContent,
    SlideType,
)
from haive.prebuilt.startup.pitchdeck.prompts import (
    pitch_deck_outline_aug_llm,
    pitch_deck_review_aug_llm,
    slide_content_aug_llm,
    storytelling_aug_llm,
)


class PitchDeckState(StateSchema):
    """State for pitch deck generation subgraph."""

    messages: List[BaseMessage] = Field(default_factory=list)

    # Input
    startup_idea: Optional[StartupIdea] = None
    pitch_deck_brief: Optional[Dict[str, Any]] = None
    deck_metadata: Optional[PitchDeckMetadata] = None

    # Deck creation
    deck_outline: Optional[Dict[str, Any]] = None
    pitch_deck: Optional[PitchDeck] = None
    current_slide_index: int = 0

    # Content generation
    narrative: Optional[Dict[str, Any]] = None
    slides_content: List[SlideContent] = Field(default_factory=list)

    # Quality and review
    review_feedback: Optional[Dict[str, Any]] = None
    quality_metrics: Optional[QualityMetrics] = None
    revision_count: int = 0
    max_revisions: int = 2

    # Status
    outline_complete: bool = False
    content_complete: bool = False
    deck_approved: bool = False


def create_deck_outline_node(state: PitchDeckState) -> Dict[str, Any]:
    """Create the pitch deck outline."""
    if not state.startup_idea and not state.pitch_deck_brief:
        return {
            "messages": [HumanMessage(content="No startup information for pitch deck")]
        }

    engine = pitch_deck_outline_aug_llm.create_runnable()

    # Use brief if available, otherwise create from idea
    if state.pitch_deck_brief:
        brief = state.pitch_deck_brief
    else:
        brief = state.startup_idea.to_pitch_deck_brief()

    # Get metadata or create default
    metadata = state.deck_metadata or PitchDeckMetadata(
        company_name=brief["company_name"],
        tagline=brief.get("tagline", ""),
        industry=(
            state.startup_idea.category.value if state.startup_idea else "technology"
        ),
        stage="seed",
    )

    result = engine.invoke(
        {
            "company_name": metadata.company_name,
            "stage": metadata.stage,
            "industry": metadata.industry,
            "funding_amount": (
                metadata.funding_amount_sought.value
                if metadata.funding_amount_sought
                else None
            ),
            "startup_brief": brief,
        }
    )

    # Create initial pitch deck structure
    import uuid

    pitch_deck = PitchDeck(deck_id=str(uuid.uuid4()), metadata=metadata, slides=[])

    # Add slides from outline
    for i, slide_outline in enumerate(result.slides):
        slide = Slide[SlideContent](
            slide_id=str(uuid.uuid4()),
            slide_type=slide_outline.slide_type,
            order=i,
            title=slide_outline.title,
            content=SlideContent(
                headline=slide_outline.headline,
                body_text="",  # To be filled
                bullet_points=slide_outline.key_points,
                speaker_notes=slide_outline.speaker_notes,
            ),
        )
        pitch_deck.slides.append(slide)

    return {
        "deck_outline": result.model_dump(),
        "pitch_deck": pitch_deck,
        "outline_complete": True,
        "messages": [
            HumanMessage(
                content=f"Created outline with {len(pitch_deck.slides)} slides"
            )
        ],
    }


def create_narrative_node(state: PitchDeckState) -> Dict[str, Any]:
    """Create compelling narrative for the pitch."""
    if not state.pitch_deck:
        return {
            "messages": [HumanMessage(content="No pitch deck for narrative creation")]
        }

    engine = storytelling_aug_llm.create_runnable()

    # Extract key information
    problem = ""
    solution = ""
    vision = ""

    if state.startup_idea:
        problem = state.startup_idea.problem.description
        solution = state.startup_idea.solution.description
        vision = f"Building a world where {problem} is solved through {solution}"
    elif state.pitch_deck_brief:
        problem = state.pitch_deck_brief.get("problem", {}).get("description", "")
        solution = state.pitch_deck_brief.get("solution", {}).get("description", "")
        vision = state.pitch_deck_brief.get("vision", "Transforming the industry")

    result = engine.invoke(
        {
            "company_name": state.pitch_deck.metadata.company_name,
            "problem": problem,
            "solution": solution,
            "customer_stories": [],  # Would come from validation
            "vision": vision,
        }
    )

    return {
        "narrative": result.model_dump(),
        "messages": [HumanMessage(content="Created compelling narrative")],
    }


def generate_slide_content_node(state: PitchDeckState) -> Dict[str, Any]:
    """Generate content for the next slide."""
    if not state.pitch_deck or state.current_slide_index >= len(
        state.pitch_deck.slides
    ):
        return {"content_complete": True}

    engine = slide_content_aug_llm.create_runnable()

    # Get current slide
    slide = state.pitch_deck.slides[state.current_slide_index]

    # Prepare supporting data based on slide type
    supporting_data = {}
    if slide.slide_type == SlideType.MARKET_SIZE and state.startup_idea:
        if state.startup_idea.market_research:
            supporting_data = {
                "tam": state.startup_idea.market_research.total_addressable_market,
                "growth_rate": state.startup_idea.market_research.growth_rate,
            }

    result = engine.invoke(
        {
            "slide_type": slide.slide_type,
            "slide_title": slide.title,
            "key_points": slide.content.bullet_points,
            "supporting_data": supporting_data,
            "target_message": slide.content.headline,
        }
    )

    # Update slide content
    slide.content = result

    # Add narrative elements if available
    if state.narrative and slide.slide_type == SlideType.PROBLEM:
        slide.content.body_text = state.narrative.get(
            "problem_story", slide.content.body_text
        )

    return {
        "current_slide_index": state.current_slide_index + 1,
        "slides_content": state.slides_content + [result],
        "messages": [
            HumanMessage(content=f"Generated content for slide {slide.title}")
        ],
    }


def review_pitch_deck_node(state: PitchDeckState) -> Dict[str, Any]:
    """Review the complete pitch deck."""
    if not state.pitch_deck:
        return {"messages": [HumanMessage(content="No pitch deck to review")]}

    engine = pitch_deck_review_aug_llm.create_runnable()

    # Convert pitch deck to review format
    deck_content = state.pitch_deck.to_review_format()

    result = engine.invoke({"pitch_deck_content": deck_content})

    # Create quality metrics from review
    quality_metrics = QualityMetrics(
        clarity_score=result.overall_score / 10,
        completeness_score=0.8 if len(state.pitch_deck.slides) >= 10 else 0.6,
        visual_appeal_score=0.7,  # Default - would need design analysis
        data_credibility_score=(
            0.8 if state.startup_idea and state.startup_idea.market_research else 0.5
        ),
        storytelling_score=0.8 if state.narrative else 0.6,
    )

    # Determine if approved
    deck_approved = result.overall_score >= 7.0 and len(result.missing_elements) == 0

    return {
        "review_feedback": result.model_dump(),
        "quality_metrics": quality_metrics,
        "deck_approved": deck_approved,
        "revision_count": state.revision_count + 1,
        "messages": [
            HumanMessage(content=f"Review complete. Score: {result.overall_score}/10")
        ],
    }


def apply_feedback_node(state: PitchDeckState) -> Dict[str, Any]:
    """Apply review feedback to improve the deck."""
    if not state.review_feedback or not state.pitch_deck:
        return {"messages": [HumanMessage(content="No feedback to apply")]}

    feedback = state.review_feedback

    # Apply top improvement suggestions
    messages = []
    for slide_id, suggestion in list(
        feedback.get("improvement_suggestions", {}).items()
    )[:3]:
        messages.append(f"Applied: {suggestion}")
        # In practice, would regenerate specific slides

    # Update deck status
    state.pitch_deck.status = "REVISION_NEEDED"

    return {
        "messages": [HumanMessage(content=f"Applied {len(messages)} improvements")],
        "current_slide_index": 0,  # Reset to regenerate content
    }


def determine_next_step(state: PitchDeckState) -> str:
    """Determine next step in pitch deck creation."""
    if not state.outline_complete:
        return "outline"
    elif not state.narrative:
        return "narrative"
    elif state.current_slide_index < len(state.pitch_deck.slides):
        return "generate_content"
    elif not state.review_feedback:
        return "review"
    elif not state.deck_approved and state.revision_count < state.max_revisions:
        return "apply_feedback"
    else:
        return "end"


def build_pitch_deck_subgraph() -> StateGraph:
    """Build the pitch deck generation subgraph."""
    graph = StateGraph(PitchDeckState)

    # Add nodes
    graph.add_node("create_outline", create_deck_outline_node)
    graph.add_node("create_narrative", create_narrative_node)
    graph.add_node("generate_slide_content", generate_slide_content_node)
    graph.add_node("review_deck", review_pitch_deck_node)
    graph.add_node("apply_feedback", apply_feedback_node)

    # Entry routing
    graph.add_conditional_edges(
        START,
        determine_next_step,
        {
            "outline": "create_outline",
            "narrative": "create_narrative",
            "generate_content": "generate_slide_content",
            "review": "review_deck",
            "end": END,
        },
    )

    # Outline leads to narrative
    graph.add_edge("create_outline", "create_narrative")

    # Narrative leads to content generation
    graph.add_edge("create_narrative", "generate_slide_content")

    # Content generation loops or proceeds to review
    graph.add_conditional_edges(
        "generate_slide_content",
        determine_next_step,
        {
            "generate_content": "generate_slide_content",  # Loop for next slide
            "review": "review_deck",
            "end": END,
        },
    )

    # Review can lead to feedback or end
    graph.add_conditional_edges(
        "review_deck",
        determine_next_step,
        {"apply_feedback": "apply_feedback", "end": END},
    )

    # Feedback loops back to content generation
    graph.add_edge("apply_feedback", "generate_slide_content")

    return graph.compile()
