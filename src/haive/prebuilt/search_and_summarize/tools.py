# src/haive/agents/search_summarize/tools.py
"""
Search tools for the Search & Summarize agent.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import tool

from haive.prebuilt.search_and_summarize.models import SearchResult, SearchResults

# Initialize search tools
ddg_search = DuckDuckGoSearchResults(max_results=10)

# Optional: Google Search (requires API key)
# google_search = GoogleSearchAPIWrapper()


@tool
def search_web(query: str, max_results: int = 5) -> SearchResults:
    """
    Search the web using DuckDuckGo.

    Args:
        query: Search query
        max_results: Maximum number of results to return

    Returns:
        SearchResults object with found results
    """
    start_time = datetime.now()

    try:
        # Perform search
        raw_results = ddg_search.run(query)

        # Parse results
        results = []
        if isinstance(raw_results, str):
            # Parse the string format from DuckDuckGo
            entries = raw_results.split("], [")
            for entry in entries:
                parts = entry.split(", ")
                if len(parts) >= 3:
                    snippet = parts[0].strip("[").strip("'").strip('"')
                    title = (
                        parts[1].strip("'").strip('"') if len(parts) > 1 else "Untitled"
                    )
                    link = (
                        parts[2].strip("]").strip("'").strip('"')
                        if len(parts) > 2
                        else ""
                    )

                    if link:
                        domain = urlparse(link).netloc
                        results.append(
                            SearchResult(
                                title=title,
                                snippet=snippet,
                                url=link,
                                source_domain=domain,
                            )
                        )

        # Limit results
        results = results[:max_results]

        search_time = (datetime.now() - start_time).total_seconds()

        return SearchResults(
            query=query,
            results=results,
            total_results=len(results),
            search_time=search_time,
        )

    except Exception as e:
        # Return empty results on error
        return SearchResults(
            query=query,
            results=[],
            total_results=0,
            search_time=(datetime.now() - start_time).total_seconds(),
        )


@tool
def search_academic(query: str, max_results: int = 5) -> SearchResults:
    """
    Search academic sources (Google Scholar, arXiv, etc.).

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        SearchResults from academic sources
    """
    # Add academic search modifiers
    academic_query = f"{query} site:scholar.google.com OR site:arxiv.org OR site:pubmed.ncbi.nlm.nih.gov OR site:jstor.org"
    return search_web(academic_query, max_results)


@tool
def search_news(query: str, max_results: int = 5) -> SearchResults:
    """
    Search recent news articles.

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        SearchResults from news sources
    """
    # Add news search modifiers and time constraint
    news_query = f'{query} news "last week" OR "today" OR "yesterday"'
    return search_web(news_query, max_results)


@tool
def search_site(query: str, site: str, max_results: int = 5) -> SearchResults:
    """
    Search within a specific website.

    Args:
        query: Search query
        site: Domain to search within (e.g., 'nature.com')
        max_results: Maximum number of results

    Returns:
        SearchResults from the specific site
    """
    site_query = f"site:{site} {query}"
    results = search_web(site_query, max_results)

    # Update query to reflect site search
    results.query = f"{query} (on {site})"
    return results


@tool
async def fetch_page_content(url: str) -> str:
    """
    Fetch and extract text content from a webpage.

    Args:
        url: URL to fetch

    Returns:
        Extracted text content
    """
    try:
        # Use WebBaseLoader for better extraction
        loader = WebBaseLoader([url])
        docs = loader.load()

        if docs:
            return docs[0].page_content[:5000]  # Limit to 5000 chars

        # Fallback to requests
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)

        return text[:5000]  # Limit to 5000 chars

    except Exception as e:
        return f"Error fetching content: {str(e)}"


@tool
def extract_domain_info(url: str) -> Dict[str, str]:
    """
    Extract information about a domain.

    Args:
        url: URL to analyze

    Returns:
        Dictionary with domain information
    """
    parsed = urlparse(url)
    domain = parsed.netloc

    # Remove www. prefix
    if domain.startswith("www."):
        domain = domain[4:]

    # Determine domain type
    domain_type = "unknown"
    if domain.endswith(".edu"):
        domain_type = "educational"
    elif domain.endswith(".gov"):
        domain_type = "government"
    elif domain.endswith(".org"):
        domain_type = "organization"
    elif domain.endswith(".com"):
        if any(news in domain for news in ["news", "times", "post", "journal"]):
            domain_type = "news"
        else:
            domain_type = "commercial"

    return {"domain": domain, "type": domain_type, "full_url": url}


@tool
def rank_results_by_relevance(
    results: List[SearchResult], query: str, prefer_domains: Optional[List[str]] = None
) -> List[SearchResult]:
    """
    Rank search results by relevance to query.

    Args:
        results: List of search results
        query: Original query
        prefer_domains: Optional list of preferred domains

    Returns:
        Ranked list of search results
    """
    query_terms = set(query.lower().split())

    for result in results:
        score = 0.0

        # Score based on query terms in title and snippet
        title_terms = set(result.title.lower().split())
        snippet_terms = set(result.snippet.lower().split())

        title_matches = len(query_terms & title_terms)
        snippet_matches = len(query_terms & snippet_terms)

        score += (title_matches * 2.0) / len(query_terms)  # Title matches worth more
        score += snippet_matches / len(query_terms)

        # Boost preferred domains
        if prefer_domains:
            domain = urlparse(str(result.url)).netloc
            if any(pref in domain for pref in prefer_domains):
                score *= 1.5

        # Normalize score
        result.relevance_score = min(score / 3.0, 1.0)

    # Sort by relevance score
    return sorted(results, key=lambda r: r.relevance_score or 0.0, reverse=True)
