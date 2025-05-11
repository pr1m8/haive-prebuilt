from typing import List

from haive_agents.base import AgentConfig
from haive_agents.tldr2.models import NewsApiParams
from haive_agents.tldr2.state import GraphState
from pydantic import Field


class TLDRAgentConfig(AgentConfig):
    news_query: str = Field(
        description="Input query to extract news search parameters from."
    )
    num_searches_remaining: int = Field(description="Number of articles to search for.")
    newsapi_params: dict = Field(description="Structured argument for the News API.")
    past_searches: List[dict] = Field(description="List of search params already used.")
