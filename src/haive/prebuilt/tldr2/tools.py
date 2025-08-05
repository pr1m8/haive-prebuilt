"""Tools for the News Research Agent.

This module defines all tools used by the news research agent for
web searching, content extraction, and analysis operations.

Tools are implemented as Pydantic models with proper typing and
documentation for use with LangChain's tool system.

Example:
    >>> from news_research.tools import web_search, extract_content
    >>> results = web_search.invoke({"query": "AI news", "max_results": 5})
    >>> content = extract_content.invoke({"url": "https://example.com/article"})

Note:
    All tools follow LangChain tool patterns and return structured data
    compatible with the agent's models.
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

try:
    from newsapi import NewsApiClient

    NEWSAPI_AVAILABLE = True
except ImportError:
    NewsApiClient = None
    NEWSAPI_AVAILABLE = False
from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)


class WebSearchInput(BaseModel):
    """Input schema for web search tool."""

    query: str = Field(description="Search query string")
    max_results: int = Field(description="Maximum number of results", default=10)
    sources: Optional[str] = Field(
        description="Comma-separated news sources", default=None
    )
    from_date: Optional[str] = Field(
        description="Start date (YYYY-MM-DD)", default=None
    )
    to_date: Optional[str] = Field(description="End date (YYYY-MM-DD)", default=None)


class WebSearchOutput(BaseModel):
    """Output schema for web search tool."""

    articles: List[Dict[str, Any]] = Field(description="List of article metadata")
    total_results: int = Field(description="Total number of results found")
    query: str = Field(description="Query used for search")


@tool(args_schema=WebSearchInput, return_direct=False)
def web_search(
    query: str,
    max_results: int = 10,
    sources: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Search for news articles using NewsAPI.

    This tool searches for news articles based on the provided query
    and filters. It returns metadata about matching articles.

    Args:
        query: Search query string
        max_results: Maximum number of results to return
        sources: Comma-separated list of news sources
        from_date: Start date for search (YYYY-MM-DD)
        to_date: End date for search (YYYY-MM-DD)

    Returns:
        Dictionary containing article metadata and search info

    Example:
        >>> results = web_search("AI healthcare", max_results=5)
        >>> print(f"Found {results['total_results']} articles")
    """
    if not NEWSAPI_AVAILABLE:
        return {
            "error": "NewsAPI not available. Install with: pip install newsapi-python",
            "articles": [],
            "total_results": 0,
        }

    try:
        # Initialize NewsAPI client
        newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

        # Set default dates if not provided
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        # Build API parameters
        params = {
            "q": query,
            "language": "en",
            "sort_by": "relevancy",
            "page_size": max_results,
            "from": from_date,
            "to": to_date,
        }

        if sources:
            params["sources"] = sources

        # Make API call
        response = newsapi.get_everything(**params)

        # Extract relevant article data
        articles = []
        for article in response.get("articles", [])[:max_results]:
            articles.append(
                {
                    "title": article.get("title", ""),
                    "url": article.get("url", ""),
                    "description": article.get("description", ""),
                    "source": article.get("source", {}),
                    "published_at": article.get("publishedAt", ""),
                    "author": article.get("author", ""),
                }
            )

        return {
            "articles": articles,
            "total_results": response.get("totalResults", 0),
            "query": query,
        }

    except Exception as e:
        logger.error(f"Error in web_search: {str(e)}")
        return {"articles": [], "total_results": 0, "query": query, "error": str(e)}


class ExtractContentInput(BaseModel):
    """Input schema for content extraction tool."""

    url: str = Field(description="URL of the article to extract")
    timeout: int = Field(description="Request timeout in seconds", default=10)


class ExtractContentOutput(BaseModel):
    """Output schema for content extraction tool."""

    url: str = Field(description="Original URL")
    title: str = Field(description="Article title")
    content: str = Field(description="Extracted text content")
    word_count: int = Field(description="Number of words extracted")
    success: bool = Field(description="Whether extraction was successful")
    error: Optional[str] = Field(description="Error message if failed", default=None)


@tool(args_schema=ExtractContentInput, return_direct=False)
def extract_content(url: str, timeout: int = 10) -> Dict[str, Any]:
    """Extract full text content from a news article URL.

    This tool fetches the web page and extracts the main article
    content using BeautifulSoup.

    Args:
        url: URL of the article to extract
        timeout: Request timeout in seconds

    Returns:
        Dictionary with extracted content and metadata

    Example:
        >>> content = extract_content("https://example.com/article")
        >>> print(f"Extracted {content['word_count']} words")
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract title
        title = ""
        if soup.title:
            title = soup.title.string
        elif soup.find("h1"):
            title = soup.find("h1").get_text()

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find article content in common containers
        article_content = ""
        content_tags = [
            soup.find("article"),
            soup.find("div", class_="article-content"),
            soup.find("div", class_="entry-content"),
            soup.find("div", class_="post-content"),
            soup.find("main"),
            soup.find("div", {"id": "content"}),
        ]

        for tag in content_tags:
            if tag:
                article_content = tag.get_text(separator=" ", strip=True)
                break

        # Fallback to body content if no article container found
        if not article_content:
            article_content = soup.get_text(separator=" ", strip=True)

        # Clean up the text
        article_content = " ".join(article_content.split())
        word_count = len(article_content.split())

        return {
            "url": url,
            "title": title,
            "content": article_content,
            "word_count": word_count,
            "success": True,
            "error": None,
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error extracting {url}: {str(e)}")
        return {
            "url": url,
            "title": "",
            "content": "",
            "word_count": 0,
            "success": False,
            "error": f"Request failed: {str(e)}",
        }
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {str(e)}")
        return {
            "url": url,
            "title": "",
            "content": "",
            "word_count": 0,
            "success": False,
            "error": str(e),
        }


class AnalyzeRelevanceInput(BaseModel):
    """Input schema for relevance analysis tool."""

    article_title: str = Field(description="Article title")
    article_description: str = Field(description="Article description")
    search_query: str = Field(description="Original search query")
    research_topic: str = Field(description="Main research topic")


@tool(args_schema=AnalyzeRelevanceInput, return_direct=False)
def analyze_relevance(
    article_title: str, article_description: str, search_query: str, research_topic: str
) -> Dict[str, Any]:
    """Analyze the relevance of an article to the research topic.

    This tool uses heuristics to score how relevant an article is
    to the research topic and search query.

    Args:
        article_title: Title of the article
        article_description: Brief description of the article
        search_query: Query used to find the article
        research_topic: Main topic being researched

    Returns:
        Dictionary with relevance score and explanation

    Note:
        This is a simplified heuristic. In production, this could
        use an LLM or more sophisticated NLP techniques.
    """
    try:
        # Combine article text
        article_text = f"{article_title} {article_description}".lower()

        # Extract keywords from query and topic
        query_keywords = set(search_query.lower().split())
        topic_keywords = set(research_topic.lower().split())
        all_keywords = query_keywords.union(topic_keywords)

        # Count keyword matches
        matches = sum(1 for keyword in all_keywords if keyword in article_text)

        # Calculate relevance score
        relevance_score = min(matches / len(all_keywords), 1.0) if all_keywords else 0.0

        # Generate explanation
        if relevance_score > 0.8:
            explanation = "Highly relevant - strong keyword match"
        elif relevance_score > 0.5:
            explanation = "Moderately relevant - good keyword overlap"
        elif relevance_score > 0.2:
            explanation = "Somewhat relevant - some keyword matches"
        else:
            explanation = "Low relevance - few keyword matches"

        return {
            "relevance_score": round(relevance_score, 2),
            "explanation": explanation,
            "keyword_matches": matches,
            "total_keywords": len(all_keywords),
        }

    except Exception as e:
        logger.error(f"Error analyzing relevance: {str(e)}")
        return {
            "relevance_score": 0.0,
            "explanation": "Error during analysis",
            "keyword_matches": 0,
            "total_keywords": 0,
        }


class BatchProcessInput(BaseModel):
    """Input schema for batch processing tool."""

    urls: List[str] = Field(description="List of URLs to process")
    operation: str = Field(description="Operation to perform (extract/analyze)")
    max_concurrent: int = Field(description="Maximum concurrent operations", default=5)


@tool(args_schema=BatchProcessInput, return_direct=False)
async def batch_process_articles(
    urls: List[str], operation: str = "extract", max_concurrent: int = 5
) -> Dict[str, Any]:
    """Process multiple articles concurrently.

    This tool enables efficient batch processing of multiple articles
    for extraction or analysis operations.

    Args:
        urls: List of article URLs to process
        operation: Type of operation ('extract' or 'analyze')
        max_concurrent: Maximum number of concurrent operations

    Returns:
        Dictionary with results for each URL and summary statistics

    Example:
        >>> results = await batch_process_articles(
        ...     urls=["url1", "url2", "url3"],
        ...     operation="extract"
        ... )
    """

    async def process_single(url: str) -> Dict[str, Any]:
        """Process a single URL."""
        try:
            if operation == "extract":
                # In async context, we'd use aiohttp instead
                # This is simplified for the example
                result = extract_content(url)
                return {"url": url, "result": result, "success": result["success"]}
            else:
                return {
                    "url": url,
                    "result": None,
                    "success": False,
                    "error": "Unknown operation",
                }
        except Exception as e:
            return {"url": url, "result": None, "success": False, "error": str(e)}

    # Create semaphore to limit concurrent operations
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_with_limit(url: str) -> Dict[str, Any]:
        async with semaphore:
            return await process_single(url)

    # Process all URLs concurrently with limit
    results = await asyncio.gather(
        *[process_with_limit(url) for url in urls], return_exceptions=True
    )

    # Compile results
    successful = sum(
        1 for r in results if isinstance(r, dict) and r.get("success", False)
    )
    failed = len(results) - successful

    return {
        "results": results,
        "summary": {
            "total": len(urls),
            "successful": successful,
            "failed": failed,
            "operation": operation,
        },
    }


# Tool function to check source credibility
@tool
def check_source_credibility(source_name: str) -> Dict[str, Any]:
    """Check the credibility rating of a news source.

    This tool provides credibility information about news sources
    based on a predefined list of ratings.

    Args:
        source_name: Name of the news source to check

    Returns:
        Dictionary with credibility score and details

    Note:
        In production, this would connect to a media bias/credibility API
    """
    # Simplified credibility ratings
    credibility_ratings = {
        "bbc-news": {"score": 0.9, "bias": "center", "factual": "high"},
        "cnn": {"score": 0.7, "bias": "left-center", "factual": "mixed"},
        "fox-news": {"score": 0.6, "bias": "right", "factual": "mixed"},
        "reuters": {"score": 0.95, "bias": "center", "factual": "very high"},
        "techcrunch": {"score": 0.8, "bias": "center", "factual": "high"},
        "bloomberg": {"score": 0.85, "bias": "center", "factual": "high"},
        "the-guardian": {"score": 0.8, "bias": "left-center", "factual": "high"},
        "the-new-york-times": {"score": 0.85, "bias": "left-center", "factual": "high"},
        "the-wall-street-journal": {
            "score": 0.85,
            "bias": "right-center",
            "factual": "high",
        },
        "associated-press": {"score": 0.95, "bias": "center", "factual": "very high"},
    }

    source_lower = source_name.lower().replace(" ", "-")

    if source_lower in credibility_ratings:
        rating = credibility_ratings[source_lower]
        return {
            "source": source_name,
            "credibility_score": rating["score"],
            "bias": rating["bias"],
            "factual_reporting": rating["factual"],
            "is_credible": rating["score"] >= 0.7,
        }
    else:
        return {
            "source": source_name,
            "credibility_score": 0.5,
            "bias": "unknown",
            "factual_reporting": "unknown",
            "is_credible": False,
            "note": "Source not in database",
        }


# Tool for filtering articles by date
@tool
def filter_by_date(
    articles: List[Dict[str, Any]], days_ago: int = 7
) -> List[Dict[str, Any]]:
    """Filter articles by publication date.

    This tool filters a list of articles to include only those
    published within the specified number of days.

    Args:
        articles: List of article dictionaries with 'published_at' field
        days_ago: Number of days to look back

    Returns:
        Filtered list of articles
    """
    cutoff_date = datetime.now() - timedelta(days=days_ago)
    filtered_articles = []

    for article in articles:
        try:
            # Parse publication date
            pub_date_str = article.get("published_at", "")
            if pub_date_str:
                # Handle ISO format
                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                if pub_date >= cutoff_date:
                    filtered_articles.append(article)
        except Exception as e:
            logger.warning(f"Error parsing date for article: {e}")
            # Include article if date parsing fails
            filtered_articles.append(article)

    return filtered_articles


# Export all tools
__all__ = [
    "web_search",
    "extract_content",
    "analyze_relevance",
    "batch_process_articles",
    "check_source_credibility",
    "filter_by_date",
]


# Import os for environment variables
