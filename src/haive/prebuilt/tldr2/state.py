from pydantic import BaseModel, Field


class GraphState(BaseModel):
    news_query: str = Field(
        description="Input query to extract news search parameters from."
    )
    num_searches_remaining: int = Field(description="Number of articles to search for.")
    newsapi_params: dict = Field(description="Structured argument for the News API.")
    past_searches: list[dict] = Field(description="List of search params already used.")
    articles_metadata: list[dict] = Field(
        description="Article metadata response from the News API"
    )
    scraped_urls: list[str] = Field(description="List of urls already scraped.")
    num_articles_tldr: int = Field(
        description="Number of articles to create TL;DR for."
    )
    potential_articles: list[dict[str, str, str]] = Field(
        description="Article with full text to consider summarizing."
    )
    tldr_articles: list[dict[str, str, str]] = Field(
        description="Selected article TL;DRs."
    )
    formatted_results: str = Field(description="Formatted results to display.")
