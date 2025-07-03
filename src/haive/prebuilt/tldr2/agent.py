from haive_agents.base import AgentConfig
from pydantic import Field


class TLDRAgentConfig(AgentConfig):
    news_query: str = Field(
        description="Input query to extract news search parameters from."
    )
    num_searches_remaining: int = Field(description="Number of articles to search for.")
    newsapi_params: dict = Field(description="Structured argument for the News API.")
    past_searches: list[dict] = Field(description="List of search params already used.")
