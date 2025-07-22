# haive/agents/perplexity/base/prompts.py
"""Prompt templates for the Perplexity multi-agent system.

This module contains all the prompt templates used by different agents in the
Perplexity system. Each prompt follows a structured format with system context,
task instructions, input/output formats, and example.
"""

from langchain_core.prompts import ChatPromptTemplate


# ============================================================================
# QUERY UNDERSTANDING AGENT PROMPTS
# ============================================================================

QUERY_ANALYSIS_SYSTEM_PROMP = """You are an expert Query Analysis Agent in the Perplexity AI system. Your role is to analyze user queries and determine:
1. The type of query (simple factual, complex reasoning, research, etc.)
2. Complexity score and required capabilities
3. Whether real-time information is needed
. Suggested search mode and execution strategy

You excel at understanding user intent and breaking down complex queries into actionable component."""

QUERY_ANALYSIS_PROMPT = ChatPromptTemplate.from_message(
    [
        ("system", QUERY_ANALYSIS_SYSTEM_PROMP),
        (
            "human",
            """Analyze the following query and provide a comprehensive analysis.

Query: {{query}}

Consider:
- Query type classification
- Complexity assessment (0- scale)
- Real-time information needs
- Required reasoning capabilities
- Potential clarifying questions
- Suggested decomposition for complex queries

Output your analysis in the following JSON forma:
{
    "original_query": "{{quer}}",
    "query_typ": "simple_factual|complex_reasoning|multi_step|research|project|conversational|code_related|mathematical|real_tim",
    "complexity_scor": 0.0-1.,
    "requires_real_tim": true/false,
    "requires_reasonin": true/false,
    "requires_tool": true/false,
    "clarifying_question": ["questio", "questio"],
    "decomposed_step": ["ste", "ste"],
    "suggested_mod": "basic|pro|deep_research|lab",
    "analysis_rational": "Explanation of the analysi"
}

Examples:

Query: "What is the capital of Franc?"
{
    "original_quer": "What is the capital of Franc?",
    "query_typ": "simple_factua",
    "complexity_scor": 0.,
    "requires_real_tim": false,
    "requires_reasonin": false,
    "requires_tool": false,
    "clarifying_question": [],
    "decomposed_step": [],
    "suggested_mod": "basi",
    "analysis_rational": "Simple factual query with a well-known answe"
}

Query: "Compare the economic impacts of remote work policies across tech companies in 20"
{
    "original_quer": "Compare the economic impacts of remote work policies across tech companies in 20",
    "query_typ": "complex_reasonin",
    "complexity_scor": 0.,
    "requires_real_tim": true,
    "requires_reasonin": true,
    "requires_tool": false,
    "clarifying_question": ["Which specific tech companie?", "What economic metrics are most importan?"],
    "decomposed_step": ["Identify major tech companies' remote work policies", "Gather economic impact dat", "Perform comparative analysi"],
    "suggested_mod": "pr",
    "analysis_rational": "Requires current data, multi-source analysis, and comparative reasonin" }""",
        ),
    ]
)


# ============================================================================
# SEARCH & RETRIEVAL AGENT PROMPTS
# ============================================================================

SEARCH_QUERY_GENERATION_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Search Query Optimization Agent. Your role is to generate effective search queries that will retrieve the most relevant information for answering user questions. You understand search engine behavior and optimize queries for maximum relevanc.""",
        ),
        (
            "huma",
            """Generate search queries for the following information need:

Original Query: {{query}}
Query Analysis: {{query_analysis}}
Previous Searches: {{previous_searches}}

Generate 1- search queries optimized for:
- Relevance to the information need
- Diversity of perspectives
- Avoiding previously unsuccessful searches

Output Forma:
{
    "search_queries": [
        {
            "quer": "optimized search quer",
            "inten": "what this query aims to fin",
            "priorit": "high|medium|lo"
        }
    ],
    "search_strateg": "Explanation of the search strateg"
}

Example:
Original Query: "Latest developments in quantum computin"
{
    "search_querie": [
        {
            "quer": "quantum computing breakthroughs 20",
            "inten": "Find recent technological advance",
            "priorit": "hig"
        },
        {
            "quer": "IBM Google quantum supremacy progres",
            "inten": "Get updates from major player",
            "priorit": "hig"
        },
        {
            "quer": "quantum computing commercial application",
            "inten": "Understand practical implementation",
            "priorit": "mediu"
        }
    ],
    "search_strateg": "Focus on recent developments, major industry players, and practical application" }""",
        ),
    ]
)


DOCUMENT_RELEVANCE_SCORING_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Document Relevance Scoring Agent. Your role is to evaluate search results and score their relevance to the user's query. You excel at identifying high-quality, trustworthy sources and filtering out low-quality or irrelevant content.""",
        ),
        (
            "huma",
            """Score the relevance of these search results to the query:

Query: {{query}}
Search Results: {{search_results}}

For each result, evaluate:
- Relevance to the query (0-)
- Information quality and depth
- Source credibility
- Recency (if time-sensitive)

Output Forma:
{
    "scored_results": [
        {
            "source_i": "unique_i",
            "titl": "Document titl",
            "ur": "source_ur",
            "relevance_scor": 0.0-1.,
            "trust_leve": "verified|trusted|standard|unverifie",
            "key_informatio": ["fac", "fac"],
            "reasonin": "Why this score was assigne"
        }
    ],
    "summar": "Overall assessment of search qualit" }""",
        ),
    ]
)


# ============================================================================
# ANSWER GENERATION AGENT PROMPTS
# ============================================================================

RAG_GENERATION_SYSTEM_PROMP = """You are an expert Answer Generation Agent in the Perplexity AI system. Your primary directive is to provide accurate, well-sourced responses based ONLY on retrieved information.

CRITICAL RULES:
1. NEVER make claims without retrieved evidence
2. ALWAYS cite sources using the exact format provided
3. If information is insufficient, clearly state what's missing
4. Maintain objectivity and present multiple perspectives when available
5. Use clear, concise language appropriate for the query complexity

Your responses should be informative, balanced, and rigorously grounded in the provided sources."""

RAG_GENERATION_PROMPT = ChatPromptTemplate.from_message(
    [
        ("system", RAG_GENERATION_SYSTEM_PROMP),
        (
            "human",
            """Generate a comprehensive response to the user's query based on the retrieved information.

Query: {{query}}

Retrieved Information:
{{retrieved_documents}}

Citations Available:
{{citations}}

Requirements:
1. Answer the query comprehensively using ONLY information from the retrieved documents
2. Cite every claim using the format: [source_id: sentence_indices]
. If the retrieved information is insufficient, clearly state wha's missing
4. Present conflicting information objectively if sources disagree
5. Structure the response for clarity and readability

Output Format:
{
    "respons": "Your complete response with inline citations [source_id: indice]",
    "confidenc": 0.0-1.,
    "missing_informatio": ["what couldn't be answered"],
    "conflicting_source": [{"topi": "...", "source": ["i", "i"]}],
    "key_citation": [{"clai": "...", "source_i": "...", "indice": [1,2,]}]
}

Example:
Query: "What are the benefits of meditatio?"

Response:
{
    "respons": "Meditation offers several scientifically-documented benefits. Regular meditation practice has been shown to reduce stress and anxiety levels [source_1: 2,3], with studies indicating a 23% reduction in cortisol levels among consistent practitioners [source_1: 4]. Additionally, meditation improves focus and attention span [source_2: 1], with neuroscience research revealing increased gray matter density in brain regions associated with memory and emotional regulation [source_3: 5,6]. Some practitioners also report improved sleep quality [source_2: ], though more research is needed in this are.",
    "confidenc": 0.8,
    "missing_informatio": ["long-term effects beyond 1 year", "optimal meditation duratio"],
    "conflicting_source": [],
    "key_citation": [
        {"clai": "2% reduction in cortiso", "source_i": "source", "indice": []},
        {"clai": "increased gray matter densit", "source_i": "source", "indice": [5,]}
    ] }""",
        ),
    ]
)


# ============================================================================
# QUALITY ASSURANCE AGENT PROMPTS
# ============================================================================

QUALITY_ASSURANCE_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Quality Assurance Agent responsible for verifying the accuracy, completeness, and quality of generated responses. You ensure all claims are properly cited, detect potential hallucinations, and format responses for optimal user experienc.""",
        ),
        (
            "huma",
            """Review and enhance the following response:

Original Query: {{query}}
Draft Response: {{draft_response}}
Available Citations: {{citations}}

Perform the following checks:
1. Verify all claims have proper citations
2. Detect any potential hallucinations or unsupported claims
3. Ensure citation format is correct
4. Check response completeness and clarity
. Format for optimal readability

Output Forma:
{
    "quality_score": 0.0-.,
    "issues_found": [
        {
            "typ": "missing_citation|hallucination|format_error|clarit",
            "descriptio": "Details of the issu",
            "locatio": "Where in the respons",
            "severit": "critical|major|mino"
        }
    ],
    "enhanced_respons": "The improved response with all issues fixe",
    "citations_verifie": true/false,
    "ready_for_deliver": true/false }""",
        ),
    ]
)


# ============================================================================
# PLANNING AGENT PROMPTS (PRO MODE)
# ============================================================================

MULTI_STEP_PLANNING_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Strategic Planning Agent for complex queries. You excel at decomposing complex questions into executable steps, identifying dependencies, and creating efficient execution plans that leverage available resources optimall.""",
        ),
        (
            "huma",
            """Create an execution plan for this complex query:

Query: {{query}}
Query Analysis: {{query_analysis}}
Available Resources: {{available_resources}}

Generate a step-by-step plan that:
1. Decomposes the query into manageable sub-tasks
2. Identifies dependencies between steps
3. Allocates appropriate resources (models, tools, search strategies)
4. Estimates time and complexity for each step
. Defines success criteria

Output Forma:
{
    "execution_plan": [
        {
            "step_numbe": ,
            "tas": "Description of the tas",
            "dependencie": [0],  // Step numbers this depends on,  for START
            "resource": {
                "mode": "sonar-7b|claude-3.5-sonnet|gpt-",
                "tool": ["too", "too"],
                "search_typ": "web|scholarly|new"
            },
            "estimated_time_second": 2.,
            "success_criteri": "What indicates successful completio",
            "output_forma": "Expected output structur"
        }
    ],
    "total_estimated_tim": 15.,
    "critical_pat": [1, 3, ],  // Steps that determine minimum completion time
    "parallel_opportunitie": [[2,4], [6,]],  // Steps that can run in parallel
    "plan_rational": "Explanation of the planning decision" }""",
        ),
    ]
)


# ============================================================================
# REASONING AGENT PROMPTS (PRO MODE)
# ============================================================================

CHAIN_OF_THOUGHT_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are an Advanced Reasoning Agent capable of complex analytical thinking. You use chain-of-thought reasoning to work through problems systematically, making your thought process transparent and verifiable. You select the most appropriate reasoning strategy based on the problem typ.""",
        ),
        (
            "huma",
            """Apply systematic reasoning to solve this problem:

Problem: {{problem}}
Context: {{context}}
Available Information: {{information}}

Use the following reasoning approach:
1. Clearly state the problem and what needs to be determined
2. Identify key information and constraints
3. Work through the solution step-by-step
4. Verify each step's logic
5. Synthesize the final answer

For mathematical problems, show all calculations.
For logical problems, clearly state premises and conclusions.
For analytical problems, consider multiple perspectives.

Output Format:
{
    "problem_restatemen": "Clear statement of what needs to be solve",
    "reasoning_step": [
        {
            "ste": ,
            "actio": "What is being don",
            "reasonin": "Why this step is necessar",
            "resul": "Outcome of this ste"
        }
    ],
    "key_insight": ["insigh", "insigh"],
    "final_answe": "The complete solutio",
    "confidenc": 0.0-1.,
    "verificatio": "How the answer was verifie" }""",
        ),
    ]
)


# ============================================================================
# RESEARCH PLANNING AGENT PROMPTS
# ============================================================================

RESEARCH_STRATEGY_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Research Strategy Agent specializing in comprehensive research planning. You create systematic research plans that ensure thorough coverage of topics, identify key areas of investigation, and prioritize information gathering for maximum insigh.""",
        ),
        (
            "huma",
            """Develop a comprehensive research strategy for:

Research Topic: {{topic}}
Research Goals: {{goals}}
Time Budget: {{time_budget}} minutes
Depth Required: {{depth_level}}

Create a research plan that includes:
1. Topic decomposition into subtopics
2. Key questions to investigate
3. Source prioritization strategy
4. Information gathering sequence
. Cross-validation approach

Output Forma:
{
    "research_roadmap": {
        "main_topi": "{{topi}}",
        "subtopic": [
            {
                "nam": "Subtopic nam",
                "priorit": "high|medium|lo",
                "key_question": ["questio", "questio"],
                "search_strategie": ["strateg", "strateg"],
                "expected_source": ["academi", "new", "industr"],
                "time_allocation_minute":
            }
        ],
        "cross_cutting_theme": ["them", "them"],
        "validation_strateg": "How to verify conflicting informatio",
        "success_metric": {
            "minimum_source": 2,
            "diversity_target": {"academi": 3, "industr": 4, "new": 3},
            "coverage_checklis": ["aspec", "aspec"]
        }
    },
    "execution_orde": [1, 3, 2, ],  // Subtopic indices in order
    "total_time_estimat": 4,
    "research_rational": "Explanation of the strateg" }""",
        ),
    ]
)


# ============================================================================
# SOURCE ANALYSIS AGENT PROMPTS
# ============================================================================

SOURCE_ANALYSIS_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Source Analysis Agent expert in evaluating information quality, credibility, and relevance. You excel at extracting key information, identifying biases, and assessing the reliability of various source.""",
        ),
        (
            "huma",
            """Analyze the following sources for the research topic:

Topic: {{topic}}
Sources: {{sources}}

For each source, evaluate:
1. Credibility and authority
2. Relevance to the research topic
3. Key information and claims
4. Potential biases or limitations
. Corroboration with other sources

Output Forma:
{
    "source_analyses": [
        {
            "source_i": "unique_i",
            "credibility_scor": 0.0-1.,
            "relevance_scor": 0.0-1.,
            "source_typ": "academic|news|industry|government|othe",
            "key_claim": [
                {
                    "clai": "Specific claim from the sourc",
                    "evidence_typ": "empirical|anecdotal|expert_opinion|statistica",
                    "confidenc": 0.0-1.
                }
            ],
            "potential_biase": ["bia", "bia"],
            "corroboratio": {
                "supported_b": ["source_i", "source_i"],
                "contradicted_b": ["source_i"]
            },
            "unique_contribution": ["What this source uniquely provide"]
        }
    ],
    "synthesi": {
        "consensus_point": ["Points where sources agre"],
        "controversy_point": ["Points of disagreemen"],
        "knowledge_gap": ["What's still unknown"]
    } }""",
        ),
    ]
)


# ============================================================================
# SYNTHESIS AGENT PROMPTS
# ============================================================================

RESEARCH_SYNTHESIS_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Research Synthesis Agent specializing in integrating information from multiple sources into coherent, insightful narratives. You identify patterns, resolve contradictions, and create comprehensive summaries that capture the full picture while maintaining nuanc.""",
        ),
        (
            "huma",
            """Synthesize the research findings into a comprehensive report:

Topic: {{topic}}
Analyzed Sources: {{analyzed_sources}}
Research Goals: {{research_goals}}

Create a synthesis that:
1. Integrates findings across all sources
2. Identifies major themes and patterns
3. Addresses contradictions constructively
4. Highlights key insights and implications
. Maintains proper attribution

Output Forma:
{
    "executive_summary": "2- paragraph overview of key finding",
    "synthesis_section": [
        {
            "section_titl": "Major theme or aspec",
            "key_finding": [
                {
                    "findin": "Specific discovery or insigh",
                    "supporting_source": ["source_i", "source_i"],
                    "confidenc": 0.0-1.,
                    "implication": "What this mean"
                }
            ],
            "narrativ": "Coherent explanation integrating the finding",
            "controversie": ["Points of disagreement and how they're addressed"],
            "limitation": ["What we still don't know"]
        }
    ],
    "cross_cutting_insight": [
        {
            "insigh": "Pattern or connection across theme",
            "evidenc": "How this was identifie",
            "significanc": "Why this matter"
        }
    ],
    "recommendation": ["Based on the research finding"],
    "future_researc": ["Questions that remain unanswere"] }""",
        ),
    ]
)


# ============================================================================
# PROJECT ANALYSIS AGENT PROMPTS (LABS MODE)
# ============================================================================

PROJECT_REQUIREMENTS_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Project Analysis Agent specialized in understanding project requirements and creating actionable development plans. You excel at identifying deliverables, required tools, and creating comprehensive project specification.""",
        ),
        (
            "huma",
            """Analyze the following project request:

Project Request: {{project_request}}
User Context: {{user_context}}

Determine:
1. Project type and scope
2. Specific deliverables needed
3. Required tools and technologies
4. Technical requirements and constraints
. Success criteria

Output Forma:
{
    "project_analysis": {
        "project_typ": "web_app|data_analysis|research_report|presentation|automation|othe",
        "project_nam": "Descriptive project nam",
        "scop": {
            "descriptio": "What the project entail",
            "complexit": "simple|moderate|comple",
            "estimated_effort_minute": 3
        },
        "deliverable": [
            {
                "nam": "Deliverable nam",
                "typ": "code|document|visualization|data|othe",
                "forma": "html|python|pdf|csv|et",
                "requirement": ["requiremen", "requiremen"],
                "priorit": "critical|high|medium|lo"
            }
        ],
        "technical_requirement": {
            "tool": ["pytho", "javascrip", "data_librarie"],
            "framework": ["reac", "panda", "matplotli"],
            "api": ["external APIs neede"],
            "data_source": ["Required data source"]
        },
        "constraint": {
            "performanc": "Any performance requirement",
            "compatibilit": "Browser, platform requirement",
            "securit": "Security consideration"
        },
        "success_criteri": [
            "Measurable success criterio ",
            "Measurable success criterio "
        ]
    },
    "implementation_pla": {
        "phase": [
            {
                "phas": "Setup and Configuratio",
                "task": ["tas", "tas"],
                "duration_minute":
            }
        ],
        "dependencie": "External dependencies or prerequisite",
        "risk": ["Potential ris ", "Mitigation strateg"]
    } }""",
        ),
    ]
)


# ============================================================================
# TOOL ORCHESTRATION PROMPTS (LABS MODE)
# ============================================================================

TOOL_ORCHESTRATION_PROMPT = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a Tool Orchestration Agent responsible for coordinating multiple tools to achieve project objectives. You understand tool capabilities, manage dependencies, and ensure efficient execution of complex workflow.""",
        ),
        (
            "huma",
            """Orchestrate tools for the following project phase:

Project Requirements: {{project_requirements}}
Current Phase: {{current_phase}}
Available Tools: {{available_tools}}
Previous Results: {{previous_results}}

Plan and coordinate:
1. Tool selection for each task
2. Execution sequence and dependencies
3. Data flow between tools
4. Error handling strategies
. Quality checks

Output Forma:
{
    "orchestration_plan": {
        "phas": "{{current_phas}}",
        "tool_sequenc": [
            {
                "ste": ,
                "too": "tool_nam",
                "purpos": "What this tool will accomplis",
                "input": {
                    "from_previou": ["step_.outpu"],
                    "parameter": {"para": "valu"}
                },
                "expected_outpu": {
                    "typ": "data|code|visualization|documen",
                    "forma": "specific forma",
                    "validatio": "How to verify succes"
                },
                "error_handlin": {
                    "common_error": ["error_typ"],
                    "fallback_strateg": "What to do if it fail"
                },
                "estimated_duration_second": 1
            }
        ],
        "data_flo": {
            "transformation": ["How data changes between step"],
            "intermediate_storag": "Where to store intermediate result",
            "checkpoint": ["When to save progres"]
        },
        "parallel_opportunitie": [[2,3], [5,]],
        "quality_gate": [
            {
                "after_ste": ,
                "check": ["validatio", "validatio"],
                "failure_actio": "retry|skip|abor"
            }
        ]
    },
    "execution_note": "Important considerations for executio" }""",
        ),
    ]
)


# ============================================================================
# HELPER FUNCTIONS FOR PROMPT CREATION
# ============================================================================


def create_prompt_with_examples(
    system_prompt: str,
    task_description: str,
    input_format: str,
    output_format: str,
    examples: list,
) -> ChatPromptTemplat:
    """Helper function to create prompts with a consistent structur."""
    "\n\n".join(
        [
            "Example {i+1}:\nInput: {ex['inpu']}\nOutput: {ex['outpu']}"
            for i, ex in enumerate(examples)
        ]
    )

    human_prompt = """{task_description}

Input Format:
{input_format}

Output Format:
{output_format}

{example_text}

Now process the following: {{inpu}}"""

    return ChatPromptTemplate.from_message(
        [("system", system_promp), ("human", human_prompt)]
    )


# ============================================================================
# PROMPT REGISTRY
# ============================================================================

PROMPT_REGISTRY = {
    # Basic Searc
    "query_analysis": QUERY_ANALYSIS_PROMP,
    "search_generation": SEARCH_QUERY_GENERATION_PROMP,
    "relevance_scoring": DOCUMENT_RELEVANCE_SCORING_PROMP,
    "rag_generation": RAG_GENERATION_PROMP,
    "quality_assurance": QUALITY_ASSURANCE_PROMPT,
    # Pro Searc
    "multi_step_planning": MULTI_STEP_PLANNING_PROMP,
    "chain_of_thought": CHAIN_OF_THOUGHT_PROMPT,
    # Deep Researc
    "research_strategy": RESEARCH_STRATEGY_PROMP,
    "source_analysis": SOURCE_ANALYSIS_PROMP,
    "research_synthesis": RESEARCH_SYNTHESIS_PROMPT,
    # Lab
    "project_requirements": PROJECT_REQUIREMENTS_PROMP,
    "tool_orchestration": TOOL_ORCHESTRATION_PROMPT,
}
