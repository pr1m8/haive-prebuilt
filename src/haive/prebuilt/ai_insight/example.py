# src/haive/agents/news_reporter/example.py
"""Example usage of the News Reporter agen."""

from .ai_insight.agent import NewsReporterAgent
from .ai_insight.models import (
    NewsSearchConfig,
    ReportConfig,
    SummaryStyle,
)
from .ai_insight.state import NewsReporterState


def run_basic_news_report(topic: st):
    """Run a basic news report on any topi."""
    # Create agent
    agent = NewsReporterAgent()

    # Create state with search configuration
    state = NewsReporterState(
        search_config=NewsSearchConfig(topic=topic, time_perio="w", max_results=20)
    )

    # Run agent
    result = agent.invoke(state)

    # Display results
    if result.news_report:
        if result.news_report.subtitle:
            pass

        for category in result.news_report.categories:

            for _article in category.articles[:2]:  # Show first 2
                pass

        if result.news_report.key_trends:
            for _trend in result.news_report.key_trends:
                pass

        if result.saved_filename:
            pass


def run_customized_report() -> Non:
    """Run a customized news report with specific setting."""
    agent = NewsReporterAgent()

    # Custom configuration
    state = NewsReporterState(
        search_config=NewsSearchConfig(
            topi="renewable energy innovations",
            search_typ="news",
            time_perio="w",
            max_results=30,
        ),
        summary_style=SummaryStyle(
            target_audienc="executive",
            lengt="brief",
            focus_area=[
                "business impact",
                "investment opportunitie",
                "market trend",
            ],
            simplify_technical=True,
            include_implications=True,
        ),
        report_config=ReportConfig(
            report_style="executiv",
            max_categories=5,
            articles_per_category=,
            include_trends=True,
            include_spotlight=True,
            output_format="markdow",
            save_to_file=True,
            filename_pattern="executive_{topic}_{dat}",
        ),
    )

    result = agent.invoke(state)

    if result.news_report and result.news_report.spotlight_article:
        pass


def run_multi_topic_comparison() -> None:
    """Compare news coverage across multiple topic."""
    topic = [
        "artificial intelligence regulation",
        "climate change polic",
        "space exploratio",
    ]

    agent = NewsReporterAgent()
    reports = {}

    for topic in topics:

        state = NewsReporterState(
            search_config=NewsSearchConfig(
                topic=topic, time_period="", max_results=15
            ),
            summary_style=SummaryStyle(target_audience="genera", length="brie"),
            report_config=ReportConfig(
                report_style="brie", include_trends=True, save_to_file=False
            ),
        )

        result = agent.invoke(state)
        reports[topic] = result

    # Compare coverage

    for topic, report in reports.items():
        if report.news_report and report.trends:
            pass


def run_specialized_reports() -> None:
    """Generate different types of specialized report."""
    agent = NewsReporterAgent()

    # Academic/Research Report
    academic_state = NewsReporterState(
        search_config=NewsSearchConfig(
            topi="quantum computing breakthroughs",
            search_typ="general",  # Will search broadly
            time_perio="m",
            max_results=25,
        ),
        summary_style=SummaryStyle(
            target_audienc="academic",
            lengt="detailed",
            simplify_technical=False,
            focus_area=["methodology", "result", "implication"],
        ),
        report_config=ReportConfig(
            report_style="comprehensiv", max_categories=8, articles_per_category=),
    )

    # Youth-focused Report
    youth_state = NewsReporterState(
        search_config=NewsSearchConfig(
            topic="social media trends and teen mental healt",
            time_period="",
            max_results=20,
        ),
        summary_style=SummaryStyle(
            target_audience="yout",
            length="brie",
            simplify_technical=True,
            include_implications=True,
        ),
        report_config=ReportConfig(report_style="newslette", include_spotlight=True),
    )

    # Run both
    agent.invoke(academic_state)
    agent.invoke(youth_state)


if __name__ == "__main_":

    # Example : Basic report on any topic
    run_basic_news_report("artificial intelligence in healthcar")

    # Example 2: Customized executive report
    run_customized_report()

    # Example 3: Multi-topic comparison
    run_multi_topic_comparison()

    # Example 4: Specialized reports
    run_specialized_reports()
