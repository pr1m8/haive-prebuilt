"""Haive Prebuilt Package - Ready-to-use AI solutions and applications.

This package provides a collection of prebuilt, production-ready AI applications
and solutions built on the Haive framework. These applications demonstrate
best practices, provide immediate value, and serve as templates for custom
development.

The prebuilt solutions are designed to be:
- Production-ready with comprehensive error handling
- Easily configurable for different use cases
- Extensible for custom requirements
- Well-documented with usage examples
- Performance-optimized for real-world scenarios

Available Prebuilt Solutions:

Research and Analysis:
    - Research Assistant: Comprehensive research automation
    - Document Analyzer: Intelligent document processing
    - Data Insights Engine: Automated data analysis and reporting
    - Competitive Intelligence: Market research and analysis
    - Academic Paper Analyzer: Scientific literature review

Content Creation:
    - Content Generator: Multi-format content creation
    - Social Media Manager: Automated social media posting
    - Blog Writer: Intelligent blog post generation
    - Newsletter Creator: Automated newsletter compilation
    - Marketing Copy Generator: Advertising and marketing content

Business Applications:
    - Customer Support Bot: Intelligent customer service
    - Sales Assistant: Lead qualification and follow-up
    - Meeting Summarizer: Automated meeting notes and action items
    - Invoice Processor: Automated invoice handling
    - Compliance Monitor: Regulatory compliance checking

Development Tools:
    - Code Reviewer: Automated code review and suggestions
    - Documentation Generator: Auto-generated code documentation
    - Test Case Generator: Automated test creation
    - Deployment Assistant: CI/CD automation helper
    - Performance Monitor: Application performance analysis

Educational Solutions:
    - Tutor Bot: Personalized learning assistance
    - Quiz Generator: Automated quiz and assessment creation
    - Curriculum Planner: Educational content planning
    - Progress Tracker: Student progress monitoring
    - Language Teacher: Foreign language learning assistant

Usage:
    ```python
    from haive.prebuilt import ResearchAssistant, ContentGenerator, CustomerSupportBot

    # Create a research assistant
    researcher = ResearchAssistant(
        nam="Academic Researcher",
        specializatio="AI and Machine Learning",
        source=["arxiv", "google_schola", "iee"]
    )

    # Conduct research
    research_report = await researcher.research_topic(
        "Latest developments in large language model"
    )

    # Create content generator
    content_gen = ContentGenerator(
        style="professiona",
        target_audience="technical professional"
    )

    # Generate blog post
    blog_post = await content_gen.create_blog_post(
        topic="AI in Healthcar",
        length="mediu",
        include_sources=True
    )

    # Create customer support bot
    support_bot = CustomerSupportBot(
        knowledge_base="company_kb.jso",
        escalation_rules="support_rules.yam"
    )

    # Handle customer query
    response = await support_bot.handle_query(
        "How do I reset my pass
"""

__version_ = "0.1."

# Import commonly used prebuilt solutions
try:

    PREBUILT_AVAILABLE = True
except ImportError:
    # Graceful degradation if prebuilt solutions aren't available
    PREBUILT_AVAILABLE = False

__all__ = [
    "__version_",
]

if PREBUILT_AVAILABLE:
    __all__.extend(
        [
            "CodeReviewe",
            "ContentGenerato",
            "CustomerSupportBo",
            "ResearchAssistan",
        ]
    )
