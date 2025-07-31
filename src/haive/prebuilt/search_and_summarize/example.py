# src/haive/agents/search_summarize/example.py
"""
Example usage of the Search & Summarize agent.
"""

from langchain_core.messages import HumanMessage

from haive.prebuilt.search_and_summarize.agent import (
    SearchSummarizeAgent,
    create_research_agent,
)
from haive.prebuilt.search_and_summarize.models import SearchQuery, SummaryConfig
from haive.prebuilt.search_and_summarize.state import SearchSummarizeState


def basic_example():
    """Basic usage example."""
    # Create agent
    agent = SearchSummarizeAgent()

    # Create state with query
    state = SearchSummarizeState(
        messages=[
            HumanMessage(
                content="What are the latest advancements in quantum computing?"
            )
        ]
    )

    # Run agent
    result = agent.invoke(state)

    # Display results
    if result.research_report:
        print(f"Research Report: {result.query_text}")
        print("=" * 80)
        print(f"\nExecutive Summary:\n{result.research_report.executive_summary}")
        print("\nKey Insights:")
        for insight in result.research_report.key_insights:
            print(f"  • {insight}")

        print(f"\n\nSource Summaries ({result.research_report.source_count} sources):")
        for summary in result.research_report.summaries:
            print(f"\n{summary.source_title}")
            print(f"URL: {summary.source_url}")
            print(f"Summary: {summary.summary}")
            if summary.key_points:
                print("Key Points:")
                for point in summary.key_points:
                    print(f"  - {point}")


def advanced_example():
    """Advanced example with specific configuration."""
    # Create a specialized research agent
    agent = create_research_agent(
        search_types=["general", "academic", "news"],
        preferred_domains=["nature.com", "science.org", "mit.edu"],
        summary_style="key_facts",
        max_results=10,
    )

    # Create state with detailed configuration
    state = SearchSummarizeState(
        search_query=SearchQuery(
            query="Impact of artificial intelligence on healthcare diagnostics",
            specific_site="pubmed.ncbi.nlm.nih.gov",
            max_results=15,
            search_type="academic",
        ),
        summary_config=SummaryConfig(
            style="key_facts",
            max_length=200,
            focus_areas=["accuracy improvements", "cost reduction", "patient outcomes"],
            include_quotes=True,
        ),
    )

    # Run research
    result = agent.invoke(state)

    # Display comprehensive results
    if result.research_report:
        print_research_report(result.research_report)

        # Show processing metrics
        print("\n\nProcessing Metrics:")
        print(f"  Total sources found: {result.total_sources}")
        print(f"  Sources summarized: {result.sources_summarized}")
        print(f"  Processing time: {result.processing_time:.2f}s")
        print(f"  Average relevance: {result.research_report.average_relevance:.2f}")


def site_specific_example():
    """Example searching specific sites."""
    agent = SearchSummarizeAgent()

    # Search multiple specific sites
    queries = [
        "climate change impacts site:nasa.gov",
        "climate change solutions site:un.org",
        "climate change research site:nature.com",
    ]

    for query in queries:
        state = SearchSummarizeState(messages=[HumanMessage(content=query)])

        result = agent.invoke(state)

        if result.research_report:
            print(f"\n{'=' * 80}")
            print(f"Query: {query}")
            print(f"Summary: {result.research_report.executive_summary}")


def comparative_research_example():
    """Example comparing information from different sources."""
    agent = SearchSummarizeAgent()

    # Research with focus on contradictions
    state = SearchSummarizeState(
        messages=[
            HumanMessage(
                content="effectiveness of intermittent fasting for weight loss"
            )
        ],
        summary_config=SummaryConfig(
            style="paragraph",
            focus_areas=["scientific evidence", "health benefits", "potential risks"],
            max_length=300,
        ),
    )

    result = agent.invoke(state)

    if result.research_report:
        print_research_report(result.research_report)

        # Highlight contradictions if found
        if result.research_report.contradictions:
            print("\n\nContradicting Information Found:")
            for contradiction in result.research_report.contradictions:
                print(f"  ⚠️  {contradiction}")

        # Show common themes
        if result.research_report.common_themes:
            print("\n\nCommon Themes:")
            for theme in result.research_report.common_themes:
                print(f"  ✓ {theme}")


def print_research_report(report):
    """Pretty print a research report."""
    print(f"\n{'=' * 80}")
    print(f"Research Report: {report.query}")
    print(f"{'=' * 80}")

    print("\nExecutive Summary:")
    print(report.executive_summary)

    print("\n\nKey Insights:")
    for i, insight in enumerate(report.key_insights, 1):
        print(f"{i}. {insight}")

    print(f"\n\nSource Summaries ({report.source_count} sources):")
    for i, summary in enumerate(report.summaries, 1):
        print(f"\n{i}. {summary.source_title}")
        print(f"   URL: {summary.source_url}")
        print(f"   Relevance: {summary.relevance_score:.2f}")
        print(f"   Summary: {summary.summary}")

        if summary.key_points:
            print("   Key Points:")
            for point in summary.key_points:
                print(f"     • {point}")

        if summary.quotes:
            print("   Notable Quotes:")
            for quote in summary.quotes:
                print(f'     "{quote}"')

    if report.recommendations:
        print("\n\nRecommendations:")
        for rec in report.recommendations:
            print(f"  → {rec}")


if __name__ == "__main__":
    print("Running Search & Summarize Examples...")

    print("\n1. Basic Example:")
    basic_example()

    print("\n\n2. Advanced Example:")
    advanced_example()

    print("\n\n3. Site-Specific Example:")
    site_specific_example()

    print("\n\n4. Comparative Research Example:")
    comparative_research_example()
