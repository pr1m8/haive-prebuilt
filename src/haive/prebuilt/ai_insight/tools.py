# src/haive/agents/news_reporter/tools.py
"""
General tools for News Reporter System.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from tavily import TavilyClient

from haive.prebuilt.ai_insight.models import Article, NewsSearchConfig

# Initialize Tavily client
tavily_client = None
if os.getenv("TAVILY_API_KEY"):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def search_news(config: NewsSearchConfig) -> List[Article]:
    """
    Search for news on any topic using Tavily API.

    Args:
        config: Search configuration with topic and parameters

    Returns:
        List of found articles
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
        for result in response.get("results", []):
            article = Article(
                title=result.get("title", "Untitled"),
                url=result.get("url", ""),
                content=result.get("content", ""),
                source=result.get("source", "Unknown"),
                relevance_score=result.get("score", 0.5),
            )
            articles.append(article)

        return articles

    except Exception as e:
        print(f"Error searching news: {e}")
        return []


@tool
def save_report_to_file(
    report_content: str,
    topic: str,
    format: str = "markdown",
    custom_filename: Optional[str] = None,
) -> str:
    """
    Save report content to file.

    Args:
        report_content: The report content to save
        topic: Topic for filename
        format: File format (markdown, html, json)
        custom_filename: Optional custom filename

    Returns:
        Path to saved file
    """
    # Generate filename
    if custom_filename:
        filename = custom_filename
    else:
        date_str = datetime.now().strftime("%Y%m%d")
        topic_str = topic.lower().replace(" ", "_")[:30]
        extension = {"markdown": "md", "html": "html", "json": "json"}.get(
            format, "txt"
        )
        filename = f"{topic_str}_report_{date_str}.{extension}"

    # Save file
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        return filename
    except Exception as e:
        print(f"Error saving file: {e}")
        return ""


@tool
def export_report_json(report: Dict[str, Any], filename: Optional[str] = None) -> str:
    """
    Export report data as JSON.

    Args:
        report: Report data to export
        filename: Optional filename

    Returns:
        Path to saved JSON file
    """
    if not filename:
        filename = f"news_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)
        return filename
    except Exception as e:
        print(f"Error exporting JSON: {e}")
        return ""


@tool
def filter_articles_by_relevance(
    articles: List[Article], min_score: float = 0.5, max_articles: Optional[int] = None
) -> List[Article]:
    """
    Filter and sort articles by relevance score.

    Args:
        articles: List of articles to filter
        min_score: Minimum relevance score
        max_articles: Maximum number to return

    Returns:
        Filtered and sorted articles
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
def group_articles_by_source(articles: List[Article]) -> Dict[str, List[Article]]:
    """
    Group articles by their source publication.

    Args:
        articles: List of articles

    Returns:
        Dictionary mapping source to articles
    """
    grouped = {}
    for article in articles:
        source = article.source
        if source not in grouped:
            grouped[source] = []
        grouped[source].append(article)

    return grouped
