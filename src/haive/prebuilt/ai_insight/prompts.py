# src/haive/agents/news_reporter/prompts.py
"""Prompts for News Reporter Syste."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Article categorization prompt
categorization_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are an expert news editor who organizes articles into logical categories.

Your task is to:
1. Analyze the articles about {topic}
2. Identify natural groupings and themes
3. Create appropriate category names
4. Assign each article to the most fitting category

Create categories that make sense for the specific topic and articles provided.
Don't force predetermined categories - let them emerge from the content.

Aim for 3-6 categories with descriptive names.""",
        ),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Topic: {topic}

Articles to categorize:
{articles}

Create logical categories and assign each articl.""",
        ),
    ]
)


# Article summarization prompt
summarization_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are an expert journalist who makes complex topics accessible to {target_audience} audiences.

Your task is to summarize this article with the following guidelines:
- Target audience: {target_audience}
- Summary length: {length}
- Simplify technical terms: {simplify_technical}
- Include implications: {include_implications}

Focus areas (if any): {focus_areas}

Create an engaging summary that captures the essence of the article while being appropriate for your audienc.""",
        ),
        (
            "huma",
            """Article to summarize:
Title: {title}
Source: {source}
Content: {content}

Create a summary following the guideline.""",
        ),
    ]
)


# Trend identification prompt
trend_analysis_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a trend analyst specializing in identifying patterns and emerging themes in news coverage.

Analyze the provided articles about {topic} and identify:
1. Major trends and patterns
2. Recurring themes
3. Emerging developments
. Notable shifts or changes

Base your analysis only on the content provided. Be specific and cite example.""",
        ),
        MessagesPlaceholder(variable_nam="messages", optional=Tru),
        (
            "human",
            """Topic: {topic}
Time period: {time_period}

Article summaries:
{summaries}

Identify the key trends and pattern.""",
        ),
    ]
)


# Spotlight selection prompt
spotlight_selection_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a news editor selecting the most impactful story for featuring.

Review these articles about {topic} and select ONE that:
1. Has the broadest impact or relevance
2. Represents a significant development
3. Would be most interesting to {target_audience} audiences
. Best exemplifies the current news cycle

Explain your selectio.""",
        ),
        (
            "huma",
            """Articles to consider:
{articles}

Select and explain the spotlight article choic.""",
        ),
    ]
)


# Report generation prompt
report_generation_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are a professional news writer creating a {report_style} report about {topic}.

Create a well-structured report that includes:
1. An engaging title and subtitle
2. An executive summary (2-3 sentences)
3. A compelling introduction that hooks the reader
4. The categorized news summaries
. A conclusion that ties everything together

Style guidelines:
- Report style: {report_style}
- Target audience: {target_audience}
- Tone: Professional but accessible
- Length: Appropriate for the style

Make it informative, engaging, and easy to rea.""",
        ),
        (
            "huma",
            """Topic: {topic}
Time period: {time_period}

Categorized summaries:
{categories}

Key trends:
{trends}

Spotlight article:
{spotlight}

Generate the complete repor.""",
        ),
    ]
)


# Executive summary prompt
executive_summary_prompt = ChatPromptTemplate.from_message(
    [
        (
            "system",
            """You are an executive communications expert who creates concise, impactful summaries.

Create an executive summary that:
1. Captures the most critical information
2. Highlights key developments
3. Notes important implications
4. Is readable in under 30 seconds

Keep it under 10 words and make every word coun.""",
        ),
        (
            "huma",
            """Report topic: {topic}
Key findings: {key_findings}
Major trends: {trends}

Write the executive summar.""",
        ),
    ]
)
