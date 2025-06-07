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
