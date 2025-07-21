"""Tools for the Journalism AI Assistant.

This module provides all tools used by the journalism assistant for
web searching, content extraction, text processing, and analysis.

Tools include web search integration, HTML parsing, text chunking,
and various utility functions for journalism workflows.

Example:
    >>> from journalism_assistant.tools import search_web, extract_web_content
    >>> results = search_web("climate change statistics 2024")
    >>> content = extract_web_content("https://example.com/article")

Note:
    Tools are implemented as LangChain-compatible functions with
    proper schemas for input/output typing.
"""

import logging
import re
import time
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

from duckduckgo_search import DDGS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.prebuilt.journalism_.models import (
    ArticleChunk,
    SearchResult,
)

# Configure logging
logger = logging.getLogger(__name__)

# Initialize DuckDuckGo search
ddgs = DDGS()


class WebSearchInput(BaseModel):
    """Input schema for web search tool."""

    keywords: str = Field(
        description="Search keywords or query", min_length=1, max_length=200
    )
    max_results: int = Field(
        description="Maximum number of results to return", default=5, ge=1, le=20
    )


@tool(args_schema=WebSearchInput)
def search_web(keywords: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search the web using DuckDuckGo for fact-checking and research.

    This tool performs web searches to find relevant information
    for fact-checking claims and researching topics.

    Args:
        keywords: Search query keywords
        max_results: Maximum number of results to return

    Returns:
        List of search results with title, URL, and snippet

    Example:
        >>> results = search_web("COVID-19 vaccine efficacy 2024", max_results=3)
        >>> for result in results:
        ...     print(f"{result['title']}: {result['url']}")
    """
    try:
        # Perform search with retry logic
        search_results = []
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                results = ddgs.text(keywords=keywords, max_results=max_results)

                for result in results:
                    search_results.append(
                        {
                            "title": result.get("title", ""),
                            "url": result.get("href", ""),
                            "snippet": result.get("body", ""),
                            "source": result.get("source", "Unknown"),
                        }
                    )
                break

            except Exception as e:
                logger.warning(f"Search attempt {retry_count + 1} failed: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2**retry_count)  # Exponential backoff
                else:
                    raise

        logger.info(f"Found {len(search_results)} results for: {keywords}")
        return search_results

    except Exception as e:
        logger.error(f"Web search failed for '{keywords}': {e}")
        return []


class ExtractWebContentInput(BaseModel):
    """Input schema for web content extraction."""

    url: str = Field(description="URL to extract content from")
    extract_links: bool = Field(
        description="Whether to extract links from the page", default=False
    )


@tool(args_schema=ExtractWebContentInput)
def extract_web_content(url: str, extract_links: bool = False) -> Dict[str, Any]:
    """Extract and clean content from a web page.

    This tool fetches web page content and extracts clean text,
    removing scripts, styles, and other non-content elements.

    Args:
        url: URL of the web page to extract
        extract_links: Whether to extract links from the page

    Returns:
        Dictionary with extracted content and metadata

    Example:
        >>> content = extract_web_content("https://example.com/article")
        >>> print(f"Extracted {content['word_count']} words")
    """
    try:
        # Load the web page
        loader = WebBaseLoader([url])
        html_content = str(loader.scrape())

        # Transform HTML to clean text
        bs_transformer = BeautifulSoupTransformer()

        # Remove unwanted tags
        cleaned_html = bs_transformer.remove_unwanted_tags(
            html_content, ["script", "style", "noscript", "meta", "head"]
        )

        # Extract main content (usually in <p> tags)
        content = bs_transformer.extract_tags(
            cleaned_html,
            ["p", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote"],
            remove_comments=True,
        )

        # Remove unnecessary lines and whitespace
        content = bs_transformer.remove_unnecessary_lines(content)

        # Extract links if requested
        links = []
        if extract_links:
            # Simple regex to find URLs
            url_pattern = r'href=[\'"]?([^\'" >]+)'
            links = re.findall(url_pattern, html_content)
            links = [link for link in links if link.startswith(("http://", "https://"))]

        # Calculate word count
        word_count = len(content.split())

        return {
            "url": url,
            "content": content,
            "word_count": word_count,
            "links": links,
            "success": True,
            "extracted_at": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to extract content from {url}: {e}")
        return {
            "url": url,
            "content": "",
            "word_count": 0,
            "links": [],
            "success": False,
            "error": str(e),
        }


@tool
def chunk_text(
    text: str, chunk_size: int = 100000, chunk_overlap: int = 1000
) -> List[str]:
    """Split text into manageable chunks for processing.

    This tool splits large text into smaller chunks while maintaining
    context through overlap, suitable for LLM processing.

    Args:
        text: Text to split into chunks
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks

    Example:
        >>> chunks = chunk_text(long_article, chunk_size=50000)
        >>> print(f"Split into {len(chunks)} chunks")
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
        length_function=len,
    )

    chunks = text_splitter.split_text(text)
    logger.info(f"Split text into {len(chunks)} chunks")

    return chunks


@tool
def extract_quotes(text: str) -> List[Dict[str, str]]:
    """Extract quoted text from an article.

    This tool identifies and extracts direct quotes from text,
    attempting to identify the speaker when possible.

    Args:
        text: Text to extract quotes from

    Returns:
        List of dictionaries with quote text and speaker

    Example:
        >>> quotes = extract_quotes(article_text)
        >>> for quote in quotes:
        ...     print(f'"{quote["text"]}" - {quote["speaker"]}')
    """
    quotes = []

    # Pattern for quotes with attribution
    # Matches: "Quote text," said Speaker Name.
    # Or: Speaker Name said, "Quote text."
    patterns = [
        r'"([^"]+)"[,\s]+(?:said|says|stated|explained|noted|added|according to)\s+([A-Z][^,.]+)',
        r'([A-Z][^,]+)\s+(?:said|says|stated|explained|noted|added)[,:\s]+"([^"]+)"',
        r'"([^"]+)"[,\s]+([A-Z][^,]+)\s+(?:said|says|stated|explained|noted|added)',
        r'"([^"]+)"',  # Fallback for quotes without attribution
    ]

    for pattern in patterns[:-1]:  # Try attributed patterns first
        matches = re.findall(pattern, text, re.MULTILINE)
        for match in matches:
            if len(match) == 2:
                # Determine which group is quote vs speaker
                if match[0].startswith('"'):
                    quote_text = match[0]
                    speaker = match[1].strip()
                else:
                    speaker = match[0].strip()
                    quote_text = match[1]

                quotes.append(
                    {"text": quote_text, "speaker": speaker, "type": "attributed"}
                )

    # Find unattributed quotes
    unattributed_pattern = r'"([^"]+)"'
    all_quotes = re.findall(unattributed_pattern, text)

    # Add unattributed quotes not already captured
    attributed_texts = {q["text"] for q in quotes}
    for quote_text in all_quotes:
        if quote_text not in attributed_texts and len(quote_text) > 20:
            quotes.append(
                {"text": quote_text, "speaker": "Unknown", "type": "unattributed"}
            )

    logger.info(f"Extracted {len(quotes)} quotes from text")
    return quotes


@tool
def identify_key_claims(text: str) -> List[str]:
    """Identify factual claims in text that should be fact-checked.

    This tool analyzes text to identify statements that make
    factual claims suitable for verification.

    Args:
        text: Text to analyze for claims

    Returns:
        List of identified claims

    Example:
        >>> claims = identify_key_claims(article_text)
        >>> print(f"Found {len(claims)} claims to fact-check")
    """
    claims = []

    # Split into sentences
    sentences = re.split(r"[.!?]+", text)

    # Patterns that often indicate factual claims
    claim_indicators = [
        r"\b\d+\s*(?:percent|%)",  # Percentages
        r"\b\d+\s*(?:million|billion|thousand)\b",  # Large numbers
        r"\b(?:study|research|report|survey)\s+(?:shows|finds|indicates|suggests)\b",
        r"\b(?:according to|data from|statistics show)\b",
        r"\b(?:increased|decreased|rose|fell)\s+by\s+\d+",
        r"\b(?:first|largest|smallest|fastest|slowest)\b",
        r"\b(?:causes|caused|leads to|results in)\b",
        r"\b(?:proven|confirmed|verified|established)\b",
    ]

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20:
            continue

        # Check if sentence contains claim indicators
        for pattern in claim_indicators:
            if re.search(pattern, sentence, re.IGNORECASE):
                claims.append(sentence)
                break

    # Remove duplicates while preserving order
    seen = set()
    unique_claims = []
    for claim in claims:
        if claim not in seen:
            seen.add(claim)
            unique_claims.append(claim)

    logger.info(f"Identified {len(unique_claims)} factual claims")
    return unique_claims


@tool
def detect_bias_indicators(text: str) -> List[Dict[str, str]]:
    """Detect potential bias indicators in text.

    This tool identifies language patterns that may indicate
    various types of bias in writing.

    Args:
        text: Text to analyze for bias

    Returns:
        List of potential bias indicators with explanations
    """
    bias_indicators = []

    # Bias pattern definitions
    bias_patterns = {
        "loaded_language": {
            "patterns": [
                r"\b(?:obviously|clearly|undoubtedly|certainly)\b",
                r"\b(?:disastrous|catastrophic|wonderful|amazing)\b",
                r"\b(?:radical|extreme|far-left|far-right)\b",
            ],
            "description": "Uses emotionally charged or absolute language",
        },
        "generalization": {
            "patterns": [
                r"\b(?:all|every|none|never|always)\s+\w+",
                r"\b(?:everyone|nobody|everything|nothing)\b",
            ],
            "description": "Makes sweeping generalizations",
        },
        "one_sided": {
            "patterns": [
                r"\b(?:only|just|merely|simply)\b",
                r"\b(?:fails to|refuses to|won\'t)\b",
            ],
            "description": "Presents only one perspective",
        },
        "attribution_bias": {
            "patterns": [
                r"\b(?:claims|alleges|purports)\b",
                r"\b(?:so-called|supposed|self-proclaimed)\b",
            ],
            "description": "Uses skeptical attribution for certain sources",
        },
    }

    for bias_type, config in bias_patterns.items():
        for pattern in config["patterns"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context (surrounding text)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()

                bias_indicators.append(
                    {
                        "type": bias_type,
                        "text": match.group(),
                        "context": context,
                        "description": config["description"],
                    }
                )

    logger.info(f"Detected {len(bias_indicators)} potential bias indicators")
    return bias_indicators


@tool
def analyze_source_diversity(quotes: List[Dict[str, str]]) -> Dict[str, Any]:
    """Analyze the diversity of sources quoted in an article.

    This tool examines quoted sources to assess diversity and
    potential source bias.

    Args:
        quotes: List of quotes with speaker information

    Returns:
        Analysis of source diversity
    """
    if not quotes:
        return {
            "total_quotes": 0,
            "unique_sources": 0,
            "diversity_score": 0.0,
            "most_quoted": [],
            "single_source_dominance": False,
        }

    # Count quotes by speaker
    speaker_counts = {}
    for quote in quotes:
        speaker = quote.get("speaker", "Unknown")
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1

    total_quotes = len(quotes)
    unique_sources = len(speaker_counts)

    # Calculate diversity score (0-1, higher is more diverse)
    # Using Shannon entropy normalized by max possible entropy
    if unique_sources > 1:
        from math import log2

        entropy = 0
        for count in speaker_counts.values():
            p = count / total_quotes
            entropy -= p * log2(p)
        max_entropy = log2(unique_sources)
        diversity_score = entropy / max_entropy if max_entropy > 0 else 0
    else:
        diversity_score = 0.0

    # Find most quoted sources
    most_quoted = sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Check for single source dominance
    max_quotes = max(speaker_counts.values())
    single_source_dominance = max_quotes > total_quotes * 0.5

    return {
        "total_quotes": total_quotes,
        "unique_sources": unique_sources,
        "diversity_score": round(diversity_score, 2),
        "most_quoted": [
            {"source": source, "count": count} for source, count in most_quoted
        ],
        "single_source_dominance": single_source_dominance,
    }


@tool
def search_and_summarize(keywords: str, max_results: int = 3) -> List[Dict[str, str]]:
    """Search for information and summarize the results.

    This tool combines web search with content extraction to provide
    summarized information for fact-checking.

    Args:
        keywords: Search keywords
        max_results: Maximum number of results to process

    Returns:
        List of search results with summaries
    """
    # Search for information
    search_results = search_web(keywords, max_results)

    summarized_results = []
    for result in search_results:
        try:
            # Extract content from URL
            content_data = extract_web_content(result["url"])

            if content_data["success"]:
                # Get first 500 words as summary
                words = content_data["content"].split()[:500]
                summary = " ".join(words)

                summarized_results.append(
                    {
                        "title": result["title"],
                        "url": result["url"],
                        "summary": summary,
                        "word_count": content_data["word_count"],
                        "source": result.get("source", "Unknown"),
                    }
                )
            else:
                # Use snippet if extraction fails
                summarized_results.append(
                    {
                        "title": result["title"],
                        "url": result["url"],
                        "summary": result["snippet"],
                        "word_count": len(result["snippet"].split()),
                        "source": result.get("source", "Unknown"),
                    }
                )

        except Exception as e:
            logger.error(f"Error processing {result['url']}: {e}")
            continue

    return summarized_results


@tool
def calculate_readability_score(text: str) -> Dict[str, Any]:
    """Calculate readability metrics for text.

    This tool analyzes text readability using various metrics
    like average sentence length and syllable count estimates.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with readability metrics
    """
    # Split into sentences
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    if not sentences:
        return {
            "avg_sentence_length": 0,
            "avg_word_length": 0,
            "readability_score": 0,
            "complexity": "unknown",
        }

    # Calculate metrics
    total_words = 0
    total_chars = 0

    for sentence in sentences:
        words = sentence.split()
        total_words += len(words)
        total_chars += sum(len(word) for word in words)

    avg_sentence_length = total_words / len(sentences) if sentences else 0
    avg_word_length = total_chars / total_words if total_words > 0 else 0

    # Simple readability score (0-1, higher is easier)
    # Based on sentence and word length
    readability_score = 1.0
    if avg_sentence_length > 25:
        readability_score -= 0.3
    elif avg_sentence_length > 20:
        readability_score -= 0.2
    elif avg_sentence_length > 15:
        readability_score -= 0.1

    if avg_word_length > 6:
        readability_score -= 0.3
    elif avg_word_length > 5:
        readability_score -= 0.2
    elif avg_word_length > 4:
        readability_score -= 0.1

    readability_score = max(0, readability_score)

    # Determine complexity
    if readability_score >= 0.8:
        complexity = "easy"
    elif readability_score >= 0.6:
        complexity = "moderate"
    elif readability_score >= 0.4:
        complexity = "difficult"
    else:
        complexity = "very difficult"

    return {
        "avg_sentence_length": round(avg_sentence_length, 1),
        "avg_word_length": round(avg_word_length, 1),
        "total_sentences": len(sentences),
        "total_words": total_words,
        "readability_score": round(readability_score, 2),
        "complexity": complexity,
    }


# Export all tools
__all__ = [
    "search_web",
    "extract_web_content",
    "chunk_text",
    "extract_quotes",
    "identify_key_claims",
    "detect_bias_indicators",
    "analyze_source_diversity",
    "search_and_summarize",
    "calculate_readability_score",
]
