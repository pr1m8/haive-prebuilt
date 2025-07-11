# src/haive/agents/news_reporter/example.py
"""
Example usage of the News Reporter agent.
"""

from haive.prebuilt.ai_insight.agent import NewsReporterAgent
from haive.prebuilt.ai_insight.models import (
    NewsSearchConfig,
    ReportConfig,
    SummaryStyle,
)
from haive.prebuilt.ai_insight.state import NewsReporterState


def run_basic_news_report(topic: str):
    """Run a basic news report on any topic."""

    # Create agent
    agent = NewsReporterAgent()

    # Create state with search configuration
    state = NewsReporterState(
        search_config=NewsSearchConfig(topic=topic, time_period="1w", max_results=20)
    )

    # Run agent
    result = agent.invoke(state)

    # Display results
    if result.news_report:
        print(f"\n{'=' * 80}")
        print(f"{result.news_report.title}")
        if result.news_report.subtitle:
            print(f"{result.news_report.subtitle}")
        print(f"{'=' * 80}")

        print(f"\nExecutive Summary:")
        print(result.news_report.executive_summary)

        print(f"\nIntroduction:")
        print(result.news_report.introduction)

        print(f"\n\nCategories ({len(result.news_report.categories)}):")
        for category in result.news_report.categories:
            print(f"\n{category.name} ({category.article_count} articles)")
            print(f"{category.description}")

            for article in category.articles[:2]:  # Show first 2
                print(f"\n  • {article.title}")
                print(f"    {article.summary}")
                print(f"    Source: {article.source}")

        if result.news_report.key_trends:
            print(f"\n\nKey Trends:")
            for trend in result.news_report.key_trends:
                print(f"  → {trend}")

        if result.saved_filename:
            print(f"\n\nReport saved to: {result.saved_filename}")


def run_customized_report():
    """Run a customized news report with specific settings."""

    agent = NewsReporterAgent()

    # Custom configuration
    state = NewsReporterState(
        search_config=NewsSearchConfig(
            topic="renewable energy innovations",
            search_type="news",
            time_period="1w",
            max_results=30,
        ),
        summary_style=SummaryStyle(
            target_audience="executive",
            length="brief",
            focus_areas=[
                "business impact",
                "investment opportunities",
                "market trends",
            ],
            simplify_technical=True,
            include_implications=True,
        ),
        report_config=ReportConfig(
            report_style="executive",
            max_categories=5,
            articles_per_category=3,
            include_trends=True,
            include_spotlight=True,
            output_format="markdown",
            save_to_file=True,
            filename_pattern="executive_{topic}_{date}",
        ),
    )

    result = agent.invoke(state)

    print(f"\nExecutive Report Generated")
    print(f"Topic: {result.topic}")
    print(f"Articles found: {result.articles_found}")
    print(f"Articles processed: {result.articles_processed}")
    print(f"Processing time: {result.processing_time:.2f}s")

    if result.news_report and result.news_report.spotlight_article:
        print(f"\n\nSpotlight Article:")
        print(f"Title: {result.news_report.spotlight_article.title}")
        print(f"Summary: {result.news_report.spotlight_article.summary}")


def run_multi_topic_comparison():
    """Compare news coverage across multiple topics."""

    topics = [
        "artificial intelligence regulation",
        "climate change policy",
        "space exploration",
    ]

    agent = NewsReporterAgent()
    reports = {}

    for topic in topics:
        print(f"\nAnalyzing: {topic}")

        state = NewsReporterState(
            search_config=NewsSearchConfig(
                topic=topic, time_period="1w", max_results=15
            ),
            summary_style=SummaryStyle(target_audience="general", length="brief"),
            report_config=ReportConfig(
                report_style="brief", include_trends=True, save_to_file=False
            ),
        )

        result = agent.invoke(state)
        reports[topic] = result

        print(f"  Found {result.articles_found} articles")
        print(f"  Identified {len(result.trends)} trends")

    # Compare coverage
    print(f"\n\n{'=' * 80}")
    print("Comparative Analysis")
    print(f"{'=' * 80}")

    for topic, report in reports.items():
        print(f"\n{topic.title()}:")
        print(f"  Coverage: {report.articles_found} articles")
        if report.news_report:
            print(f"  Categories: {len(report.news_report.categories)}")
            if report.trends:
                print(f"  Top trend: {report.trends[0]}")


def run_specialized_reports():
    """Generate different types of specialized reports."""

    agent = NewsReporterAgent()

    # Academic/Research Report
    academic_state = NewsReporterState(
        search_config=NewsSearchConfig(
            topic="quantum computing breakthroughs",
            search_type="general",  # Will search broadly
            time_period="1m",
            max_results=25,
        ),
        summary_style=SummaryStyle(
            target_audience="academic",
            length="detailed",
            simplify_technical=False,
            focus_areas=["methodology", "results", "implications"],
        ),
        report_config=ReportConfig(
            report_style="comprehensive", max_categories=8, articles_per_category=5
        ),
    )

    # Youth-focused Report
    youth_state = NewsReporterState(
        search_config=NewsSearchConfig(
            topic="social media trends and teen mental health",
            time_period="1w",
            max_results=20,
        ),
        summary_style=SummaryStyle(
            target_audience="youth",
            length="brief",
            simplify_technical=True,
            include_implications=True,
        ),
        report_config=ReportConfig(report_style="newsletter", include_spotlight=True),
    )

    print("Generating specialized reports...")

    # Run both
    academic_result = agent.invoke(academic_state)
    youth_result = agent.invoke(youth_state)

    print(
        f"\nAcademic Report: {academic_result.news_report.title if academic_result.news_report else 'No report'}"
    )
    print(
        f"Youth Report: {youth_result.news_report.title if youth_result.news_report else 'No report'}"
    )


if __name__ == "__main__":
    print("News Reporter Examples\n")

    # Example 1: Basic report on any topic
    print("1. Basic News Report - AI and Healthcare")
    run_basic_news_report("artificial intelligence in healthcare")

    # Example 2: Customized executive report
    print("\n\n2. Executive Report - Renewable Energy")
    run_customized_report()

    # Example 3: Multi-topic comparison
    print("\n\n3. Multi-Topic Comparison")
    run_multi_topic_comparison()

    # Example 4: Specialized reports
    print("\n\n4. Specialized Reports")
    run_specialized_reports()
