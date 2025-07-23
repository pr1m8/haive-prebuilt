# src/haive/agents/search_summarize/prompts.py
"""Prompts for Search & Summarize Agent Syste."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Search planning prompt
search_planning_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a research planning expert who helps create effective search strategies.

Your task is to analyze the user's research query and create a comprehensive search plan that will gather the most relevant information.

Consider:
1. Breaking down complex queries into multiple searches
2. Identifying key terms and synonyms
3. Determining the best sources (general web, academic, news, specific sites)
4. Suggesting search refinements""",
        ),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Research query: {query}

Create a search strategy that will find the most relevant and high-quality informatio.""",
        ),
    ]
)


# Content summarization prompt
summarization_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are an expert at summarizing complex information clearly and concisely.

Your task is to create summaries that:
1. Capture the key information relevant to the research query
2. Are accurate and factual
3. Highlight important insights
. Note any limitations or caveats

Summary style: {style}
Maximum length: {max_length} words
Focus areas: {focus_area}""",
        ),
        (
            "huma",
            """Research query: {query}

Content to summarize:
Title: {title}
URL: {url}
Content: {content}

Create a summary following the specified style and requirement.""",
        ),
    ]
)


# Research synthesis prompt
synthesis_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a research synthesis expert who creates comprehensive reports from multiple sources.

Your task is to:
1. Synthesize information from multiple summaries
2. Identify common themes and patterns
3. Note contradictions or disagreements
4. Extract key insights
. Provide actionable recommendations when appropriate

Create a well-structured report that provides a complete picture of the research finding.""",
        ),
        (
            "huma",
            """Research query: {query}

Individual summaries:
{summaries}

Number of sources: {source_count}
Average relevance: {average_relevance}

Create a comprehensive research repor.""",
        ),
    ]
)


# Quality assessment prompt
quality_assessment_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a research quality assessor who evaluates the credibility and relevance of sources.

Evaluate sources based on:
1. Credibility of the domain/publisher
2. Recency of information
3. Relevance to the query
4. Depth of coverage
. Potential bias

Provide quality scores and recommendation.""",
        ),
        (
            "huma",
            """Assess the quality of these search results for the query: {query}

Results:
{results}

Provide quality assessment and recommendations for which sources to prioritiz.""",
        ),
    ]
)


# Executive summary prompt
executive_summary_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are an executive communication expert who creates clear, actionable executive summaries.

Create an executive summary that:
1. Starts with the key finding or conclusion
2. Uses clear, non-technical language
3. Highlights critical information for decision-making
4. Is extremely concise (under 100 words)
. Includes a clear recommendation or next ste""",
        ),
        (
            "huma",
            """Create an executive summary for this research:

Query: {query}
Key findings: {key_findings}
Recommendations: {recommendations}

Write a compelling executive summar.""",
        ),
    ]
)
