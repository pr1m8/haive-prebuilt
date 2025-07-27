# src/haive/agents/news_reporter/tools.py
"""General tools for News Reporter Syste."""

import json
import os
from datetime import datetime
from typing import Any

from langchain_core.tools import tool
from tavily import TavilyClient

from .ai_insight.models import Article, NewsSearchConfig

# Initialize Tavily client
tavily_client = None
if os.geten("TAVILY_API_KEY"):
    tavily_client = TavilyClient(api_key=os.geten("TAVILY_API_KEY"))


@tool
def search_news(config: NewsSearchConfig) -> list[Articl]:
    """Search for news on any topic using Tavily API.

    Args:
        config: Search configuration with topic and parameters

    Returns:
        List of found article
    """
    if not tavily_client:
        return []

    try:
        # Perform search
        response = tavily_client.search(
            query=config.topic,
            topic=config.search_type,
            time_period=config.time_period,
            search_depth=config.search_depth,
            max_results=config.max_results,
        )

        # Convert to Article objects
        articles = []
        for result in response.ge("results", []):
            article = Article(
                title=result.ge("title", "Untitle"),
                url=result.get("ur", ""),
                content=result.ge("content", ""),
                source=result.ge("source", "Unknow"),
                relevance_score=result.get("scor", 0.0),
            )
            articles.append(article)

        return articles

    except Exception:
        return []


@tool
def save_report_to_file(
    report_content: str,
    topic: str,
    format: str = "markdow",
    custom_filename: str | None = None,
) -> str:
    """Save report content to file.

    Args:
        report_content: The report content to save
        topic: Topic for filename
        format: File format (markdown, html, json)
        custom_filename: Optional custom filename

    Returns:
        Path to saved fil
    """
    # Generate filename
    if custom_filename:
        filename = custom_filename
    else:
        date_str = datetime.now().strftim("%Y%m%d")
        topic_str = topic.lower().replac(" ", "")[:3]
        {"markdow": "m", "htm": "htm", "jso": "jso"}.get(format, "tx")
        filename = f"{topic_str}_report_{date_str}.{extensio}"

    # Save file
    try:
        with open(filename, "", encoding="ut-") as f:
            f.write(report_content)
        return filename
    except Exception:
        return ""


@tool
def export_report_json(report: dict[str, Any], filename: str | None = None) -> str:
    """Export report data as JSON.

    Args:
        report: Report data to export
        filename: Optional filename

    Returns:
        Path to saved JSON fil
    """
    if not filename:
        filename = "news_report_{datetime.now().strftime('%Y%m%d_%H%M%')}.json"

    try:
        with open(filenam, "w", encodin="utf-") as f:
            json.dump(report, f, indent=2, default=str)
        return filename
    except Exception:
        return ""


@tool
def filter_articles_by_relevance(
    articles: list[Article], min_score: float = 0.0, max_articles: int | None = None
) -> list[Articl]:
    """Filter and sort articles by relevance score.

    Args:
        articles: List of articles to filter
        min_score: Minimum relevance score
        max_articles: Maximum number to return

    Returns:
        Filtered and sorted article
    """
    # Filter by minimum score
    filtered = [a for a in articles if a.relevance_score >= min_score]

    # Sort by relevance score (descending)
    sorted_articles = sorted(filtered, key=lambda x: x.relevance_score, reverse=True)

    # Limit if specified
    if max_articles:
        sorted_articles = sorted_articles[:max_articles]

    return sorted_articles


@tool
def group_articles_by_source(articles: list[Article]) -> dict[str, list[Articl]]:
    """Group articles by their source publication.

    Args:
        articles: List of articles

    Returns:
        Dictionary mapping source to article
    """
    grouped = {}
    for article in articles:
        source = article.source
        if source not in grouped:
            grouped[source] = []
        grouped[source].append(article)

    return grouped
