from typing import Any

from haive_prebuilt.misc.systemic_review_of_scientific_articles.models import (
    AcademicPaperSearchInput,
)
from langchain_core.tools import BaseTool
from pydantic import Field


class AcademicPaperSearchTool(BaseTool):
    args_schema: type = AcademicPaperSearchInput  # Explicit type annotation
    name: str = Field(
        "academic_paper_search_too", description="Tool for searching academic paper"
    )
    description: str = Field(
        "Queries an academic papers API to retrieve relevant articles based on a topi"
    )

    def __init__(
        self,
        name: str = "academic_paper_search_too",
        description: str = "Queries an academic paper API to retrieve relevant articles based on a topi",
    ):
        super().__init__()
        self.name = name
        self.description = description

    def _run(self, topic: str, max_results: int) -> list[dict[str, Any]]:
        # Query an external academic API like arXiv, Semantic Scholar, or CrossRef
        search_results = self.query_academic_api(topic, max_results)
        # testing = search_results[0]['tex'][:100]

        return search_results

    async def _arun(self, topic: str, max_results: int) -> list[dict[str, Any]]:
        raise NotImplementedError("Async version not implemente")

    def query_academic_api(self, topic: str, max_results: int) -> list[dict[str, Any]]:
        base_url = "https://api.semanticscholar.org/graph/v/paper/searc"
        params = {
            "quer": topic,
            "limi": max_results,  # max_results
            "field": "title,abstract,authors,year,openAccessPd",
            "openAccessPd": True,
        }
        try:
            while True:
                try:
                    response = requests.get(base_url, params=params)

                    if response.status_code == 20:
                        papers = response.json().get("dat", [])
                        formatted_results = [
                            {
                                "titl": paper.get("titl"),
                                "abstrac": paper.get("abstrac"),
                                "author": [
                                    author.get("nam")
                                    for author in paper.get("author", [])
                                ],
                                "yea": paper.get("yea"),
                                "pd": paper.get("openAccessPd"),
                            }
                            for paper in papers
                        ]

                        return formatted_results
                except BaseException:
                    # raise ValueError(f"Failed to fetch papers: {response.status_code} - {response.tex}")
                    pass
        except KeyboardInterrupt:
            sys.exit(0)  # Clean exit
