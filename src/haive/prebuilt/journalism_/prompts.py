"""Prompt templates for the Journalism AI Assistant.

This module contains all prompt templates used by the journalism assistant
for various analysis tasks. Prompts are separated from engines for better
maintainability and reusability.

Each prompt is designed for specific journalism tasks with detailed
instructions and examples to guide the LLM.

Example:
    >>> from journalism_assistant.prompts import SUMMARIZATION_PROMPT
    >>> prompt = SUMMARIZATION_PROMPT.format(article_tex="Article content...")

Note:
    Prompts use LangChain's ChatPromptTemplate for message-based formatting
    with variable substitution.
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)


# System personas for different roles
JOURNALIST_SYSTE = """You are an experienced journalist and editor with expertise in:
- Fact-checking and verification
- Clear, concise writing
- Identifying bias and maintaining objectivity
- AP style and journalism ethics
- Source evaluation and attributio"""

FACT_CHECKER_SYSTE = """You are a professional fact-checker with expertise in:
- Identifying verifiable claims
- Research and source evaluation
- Distinguishing facts from opinions
- Recognizing misleading information
- Verification methodologie"""

EDITOR_SYSTE = """You are a senior editor with expertise in:
- Grammar, style, and clarity
- Identifying bias and loaded language
- Improving readability
- Maintaining journalistic standards
- Constructive feedbac"""


# Action identification prompt with few-shot examples
ACTION_IDENTIFICATION_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are an AI assistant that identifies journalism analysis actions from user requests.

Map user requests to these specific actions:
- summarization: Create article summary
- fact-checking: Verify claims and statements
- tone-analysis: Analyze tone and sentiment
- quote-extraction: Extract quotes
- grammar-and-bias-review: Check grammar and bias
- no-action-required: No specific action needed
- invalid: Request outside scope

Important rules:
. Fo "everything", "full repor", or "comprehensive analysi" → list ALL individual actions
2. Only list explicitly requested actions
3. Multiple actions can be selected
4. Be precise - don't infer unstated actions""",
        ),
        MessagesPlaceholder(variable_nam="messages"),
        (
            "huma",
            """Example:
- "Summarize this article" → ["summarizatio"]
- "Check if this is accurat" → ["fact-checkin"]
- "What's the tone?" → ["tone-analysi"]
- "Find all quote" → ["quote-extractio"]
- "Review grammar and bia" → ["grammar-and-bias-revie"]
- "Do everythin" → ["summarizatio", "fact-checkin", "tone-analysi", "quote-extractio", "grammar-and-bias-revie"]
- "Thank" → ["no-action-require"]
- "What's the weather?" → ["invali"]

User request: {input_text}""",
        ),
    ]
)


# Enhanced summarization prompt
SUMMARIZATION_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            JOURNALIST_SYSTE
            + """

As a journalist, create summaries that:
1. Lead with the most newsworthy information
2. Follow the inverted pyramid structure
3. Include WHO, WHAT, WHEN, WHERE, WHY, HOW
4. Maintain neutral, objective tone
5. Preserve important context

Structure:
- 3-7 main points covering key events/findings
- List of key people with their roles
- Important statistics or data points
- One cohesive summary paragraph (150-20 word)""",
        ),
        MessagesPlaceholder(variable_nam="messages"),
        (
            "huma",
            """Article to summarize ({word_count} words):

{article_text}

Create a journalistic summary following the guideline.""",
        ),
    ]
)


# Enhanced fact-checking prompt
FACT_CHECKING_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            FACT_CHECKER_SYSTE
            + """

Your fact-checking process:
1. Identify ALL factual claims (statistics, quotes, events, attributions)
. Categorize each claim:
    - confirmed: Verifiable and accurate
    - refuted: Demonstrably false or misleading
    - unverifiable: Cannot be verified with available information
    - vague: Lacks specificity (missing who/what/when/where details)

For each claim provide:
- The exact claim as stated
- Your categorization with confidence level
- Clear explanation of your findings
- Suggested search keywords for unverifiable claims

Red flags to check:
- Unsourced statistics
- Vague attribution ("experts say", "studies sho")
- Absolute statements without evidence
- Out-of-context quotes
- Misleading comparisons""",
        ),
        MessagesPlaceholder(variable_nam="messages"),
        (
            "huma",
            """Text to fact-check:
{text_chunk}

Context: {context}

Search results available:
{search_results}

Perform thorough fact-checking analysi.""",
        ),
    ]
)


# Tone analysis prompt with bias detection
TONE_BIAS_ANALYSIS_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            EDITOR_SYSTE
            + """

Analyze tone and bias by examining:

TONE INDICATORS:
- Word choice (neutral vs. loaded language)
- Sentence structure (active vs. passive voice)
- Narrative framing
- Emotional appeals
- Overall sentiment

BIAS TYPES TO DETECT:
- Selection bias: What's included/excluded?
- Framing bias: How are issues presented?
- Confirmation bias: Cherry-picked evidence?
- Source bias: Whose voices are heard?
- Language bias: Loaded terms, dog whistles?

Provide:
1. Overall tone classification
2. Sentiment score (-1 to 1)
3. Specific examples with explanations
4. Detected biases with severity
5. Objectivity score (0-1)""",
        ),
        MessagesPlaceholder(variable_nam="messages"),
        (
            "huma",
            """Analyze tone and bias in:
{text_chunk}

Detected bias indicators:
{bias_indicators}

Provide comprehensive tone and bias analysi.""",
        ),
    ]
)


# Quote extraction and attribution prompt
QUOTE_EXTRACTION_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            JOURNALIST_SYSTE
            + """

Extract and analyze quotes following journalism standards:

EXTRACTION RULES:
1. Only direct quotes (within quotation marks)
2. Preserve exact wording
3. Identify speaker with full name/title
4. Note context (when, where, why said)
. Flag missing attributions

ANALYSIS INCLUDES:
- Speaker identification and credibility
- Context and significance
- Source diversity assessment
- Attribution quality
- Most newsworthy quotes

RED FLAGS:
- Anonymous sources without justification
- Quotes without clear attribution
- Out-of-context snippets
- Single-source dominanc""",
        ),
        MessagesPlaceholder(variable_nam="messages"),
        (
            "huma",
            """Extract quotes from:
{text_chunk}

Initial extraction found:
{extracted_quotes}

Source diversity analysis:
{source_analysis}

Provide complete quote analysis with journalism standard.""",
        ),
    ]
)


# Grammar and bias review prompt
GRAMMAR_BIAS_REVIEW_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            EDITOR_SYSTE
            + """

Perform a thorough editorial review examining:

GRAMMAR & STYLE:
- Spelling and typos
- Grammar errors
- Punctuation issues
- Clarity problems
- AP style violations
- Awkward phrasing

BIAS INDICATORS:
- Loaded/emotional language
- Unbalanced presentations
- Missing perspectives
- Unfair characterizations
- Leading questions
- Buried ledes

ASSESSMENT METRICS:
- Writing quality (0-1)
- Readability (0-1)
- Bias level (0=neutral, =heavily biased)

Provide specific examples and constructive suggestion.""",
        ),
        MessagesPlaceholder(variable_nam="messages"),
        (
            "huma",
            """Review for grammar and bias:
{text_chunk}

Readability analysis:
{readability_metrics}

Bias indicators detected:
{bias_indicators}

Provide editorial review with specific improvement.""",
        ),
    ]
)


# Comprehensive report generation prompt
REPORT_GENERATION_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a senior journalism analyst preparing an executive report.

Synthesize all analyses into a professional report that:

1. EXECUTIVE SUMMARY
    - Overall article quality assessment
    - Key strengths and weaknesses
    - Critical issues requiring attention

2. DETAILED FINDINGS
    - Factual accuracy assessment
    - Writing quality and clarity
    - Objectivity and balance
    - Source diversity and attribution

. RECOMMENDATIONS
    - Specific, actionable improvements
    - Priority order for changes
    - Industry best practices

Focus on:
- Constructive, professional tone
- Specific examples from analyses
- Practical improvements
- Journalism standards and ethic""",
        ),
        MessagesPlaceholder(variable_nam="messages"),
        (
            "huma",
            """Generate comprehensive report from these analyses:

SUMMARY:
{summary_result}

FACT-CHECK:
{fact_check_result}

TONE ANALYSIS:
{tone_analysis_result}

QUOTES:
{quote_result}

GRAMMAR/BIAS:
{grammar_bias_result}

Create professional journalism analysis repor.""",
        ),
    ]
)


# Chunk combination prompts for different analysis types
CHUNK_COMBINATION_PROMPT = {
    "fact_checking": PromptTemplate(
        templat="""Combine these fact-check results from multiple chunks into a unified analysis:

{chunk_results}

Merge by:
1. Eliminating duplicate claims
2. Maintaining consistent categorization
3. Combining evidence for same claims
4. Preserving all unique findings
. Calculating overall statistics

Create comprehensive fact-check result.""",
        input_variable=["chunk_results"],
    ),
    "tone_analysi": PromptTemplate(
        template="""Combine these tone analyses from multiple chunks:

{chunk_results}

Synthesize by:
1. Determining overall tone across all chunks
2. Averaging sentiment scores
3. Collecting all bias examples
4. Identifying patterns across chunks
. Calculating final objectivity score

Create unified tone analysi.""",
        input_variable=["chunk_results"],
    ),
    "quote_extractio": PromptTemplate(
        template="""Combine quote extractions from multiple chunks:

{chunk_results}

Merge by:
1. Eliminating duplicate quotes
2. Maintaining speaker consistency
3. Preserving all unique quotes
4. Combining source statistics
. Assessing overall source diversity

Create comprehensive quote analysi.""",
        input_variable=["chunk_results"],
    ),
    "grammar_bias_revie": PromptTemplate(
        template="""Combine grammar/bias reviews from multiple chunks:

{chunk_results}

Synthesize by:
1. Collecting all issues found
2. Eliminating duplicates
3. Calculating overall scores
4. Identifying patterns
. Prioritizing recommendations

Create unified revie.""",
        input_variable=["chunk_results"],
    ),
}


# Specialized prompts for specific scenarios
BREAKING_NEWS_PROMPT = PromptTemplate(
    templat="""Analyze this breaking news article with focus on:
1. Verification of initial reports
2. Source reliability in fast-moving situation
3. What's confirmed vs. speculation
4. Missing information gaps
5. Need for follow-up

Article: {article_text}

Provide rapid assessment for breaking news.""",
    input_variable=["article_text"],
)


OPINION_PIECE_PROMPT = PromptTemplate(
    templat="""Analyze this opinion piece considering:
1. Clear labeling as opinion
2. Factual claims within opinion
3. Transparency about author perspective
4. Supporting evidence quality
. Counterargument acknowledgment

Article: {article_text}

Assess opinion piece by journalism standard.""",
    input_variable=["article_text"],
)


INVESTIGATIVE_PROMPT = PromptTemplate(
    templat="""Analyze this investigative piece examining:
1. Source documentation
2. Evidence trail
3. Methodology transparency
4. Right of reply inclusion
. Public interest justification

Article: {article_text}

Evaluate investigative journalism standard.""",
    input_variable=["article_text"],
)


# Helper function to create custom prompts
def create_custom_journalism_prompt(
    role: str, task: str, guidelines: List[str], include_messages: bool = True
) -> ChatPromptTemplat:
    """Create a custom journalism analysis prompt.

    Args:
        role: The role/expertise of the analyzer
        task: Description of the analysis task
        guidelines: List of specific guidelines
        include_messages: Whether to include message history

    Returns:
        ChatPromptTemplate: Configured prompt templat
    """
    "{role}\n\n{task}\n\nGuidelines:\n" + "\n".join(
        "{i+}. {guideline}" for i, guideline in enumerate(guidelines)
    )

    if include_messages:
        messages.append(MessagesPlaceholder(variable_nam="messages"))

    messages.appen(("human", "{input_tex}"))

    return ChatPromptTemplate.from_messages(messages)


# Export all prompts
__all__ = [
    "ACTION_IDENTIFICATION_PROMP",
    "BREAKING_NEWS_PROMP",
    "CHUNK_COMBINATION_PROMPT",
    "FACT_CHECKING_PROMP",
    "GRAMMAR_BIAS_REVIEW_PROMP",
    "INVESTIGATIVE_PROMP",
    "OPINION_PIECE_PROMP",
    "QUOTE_EXTRACTION_PROMP",
    "REPORT_GENERATION_PROMP",
    "SUMMARIZATION_PROMP",
    "TONE_BIAS_ANALYSIS_PROMP",
    "create_custom_journalism_promp",
]
