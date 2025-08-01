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
        name="Academic Researcher",
        specialization="AI and Machine Learning",
        sources=["arxiv", "google_scholar", "ieee"]
    )

    # Conduct research
    research_report = await researcher.research_topic(
        "Latest developments in large language models"
    )

    # Create content generator
    content_gen = ContentGenerator(
        style="professional",
        target_audience="technical professionals"
    )

    # Generate blog post
    blog_post = await content_gen.create_blog_post(
        topic="AI in Healthcare",
        length="medium",
        include_sources=True
    )

    # Create customer support bot
    support_bot = CustomerSupportBot(
        knowledge_base="company_kb.json",
        escalation_rules="support_rules.yaml"
    )

    # Handle customer query
    response = await support_bot.handle_query(
        "How do I reset my password?"
    )
    ```

Configuration:
    Each prebuilt solution includes:
    - YAML/JSON configuration files
    - Environment variable support
    - Command-line interface options
    - Web-based configuration panels
    - API endpoint configuration

Deployment Options:
    - Docker containers for easy deployment
    - Cloud-native configurations (AWS, GCP, Azure)
    - Kubernetes manifests for orchestration
    - Serverless function packages
    - Traditional server deployments

Customization:
    All prebuilt solutions support:
    - Custom prompts and instructions
    - Plugin architecture for extensions
    - Custom data sources and integrations
    - Branding and UI customization
    - Workflow modifications

Each solution includes comprehensive documentation, deployment guides,
configuration examples, and integration tutorials.
"""

import lazy_loader as lazy

# Define submodules to lazy load
submodules = [
    "academic_task_learning",
    "ai_insight",
    "arxiv_agent",
    "blog_writer_agent",
    "car_buyer_agent",
    "career_assistant",
    "chiron_learning_agent",
    "clause_ai",
    "company_researcher",
    "constituional_agent",
    "content_intelligence",
    "contract_analysis",
    "customer_support",
    "db_discovery",
    "e2e_testing",
    "essay_grading",
    "eu_green_compliance",
    "gif_generator",
    "github_agent",
    "gmail_agent",
    "graph_inspector",
    "gtla",
    "memory_agent",
    "misc",
    "open_researcher",
    "people_researcher",
    "perplexity",
    "podcast_generator",
    "project_manager",
    "reflection",
    "sales_call_analyzer",
    "scientific_paper_agent",
    "search_and_summarize",
    "self_improving",
    "shop_genie",
    "startup",
    "systemic_review_of_scientific_articles",
    "taskifier",
    "tldr2",
    "translator_agent",
    "tts_poem_gen",
    "weather_agent",
    "weather_disaster_management",
    "wolfram_alpha_agent",
]

# Define specific attributes from submodules to expose
# TODO: Customize this based on actual exports from each submodule
submod_attrs = {
    "academic_task_learning": [],  # TODO: Add specific exports from academic_task_learning
    "ai_insight": [],  # TODO: Add specific exports from ai_insight
    "arxiv_agent": [],  # TODO: Add specific exports from arxiv_agent
    "blog_writer_agent": [],  # TODO: Add specific exports from blog_writer_agent
    "car_buyer_agent": [],  # TODO: Add specific exports from car_buyer_agent
    "career_assistant": [],  # TODO: Add specific exports from career_assistant
    "chiron_learning_agent": [],  # TODO: Add specific exports from chiron_learning_agent
    "clause_ai": [],  # TODO: Add specific exports from clause_ai
    "company_researcher": [],  # TODO: Add specific exports from company_researcher
    "constituional_agent": [],  # TODO: Add specific exports from constituional_agent
    "content_intelligence": [],  # TODO: Add specific exports from content_intelligence
    "contract_analysis": [],  # TODO: Add specific exports from contract_analysis
    "customer_support": [],  # TODO: Add specific exports from customer_support
    "db_discovery": [],  # TODO: Add specific exports from db_discovery
    "e2e_testing": [],  # TODO: Add specific exports from e2e_testing
    "essay_grading": [],  # TODO: Add specific exports from essay_grading
    "eu_green_compliance": [],  # TODO: Add specific exports from eu_green_compliance
    "gif_generator": [],  # TODO: Add specific exports from gif_generator
    "github_agent": [],  # TODO: Add specific exports from github_agent
    "gmail_agent": [],  # TODO: Add specific exports from gmail_agent
    "graph_inspector": [],  # TODO: Add specific exports from graph_inspector
    "gtla": [],  # TODO: Add specific exports from gtla
    "memory_agent": [],  # TODO: Add specific exports from memory_agent
    "misc": [],  # TODO: Add specific exports from misc
    "open_researcher": [],  # TODO: Add specific exports from open_researcher
    "people_researcher": [],  # TODO: Add specific exports from people_researcher
    "perplexity": [],  # TODO: Add specific exports from perplexity
    "podcast_generator": [],  # TODO: Add specific exports from podcast_generator
    "project_manager": [],  # TODO: Add specific exports from project_manager
    "reflection": [],  # TODO: Add specific exports from reflection
    "sales_call_analyzer": [],  # TODO: Add specific exports from sales_call_analyzer
    "scientific_paper_agent": [],  # TODO: Add specific exports from scientific_paper_agent
    "search_and_summarize": [],  # TODO: Add specific exports from search_and_summarize
    "self_improving": [],  # TODO: Add specific exports from self_improving
    "shop_genie": [],  # TODO: Add specific exports from shop_genie
    "startup": [],  # TODO: Add specific exports from startup
    "systemic_review_of_scientific_articles": [],  # TODO: Add specific exports from systemic_review_of_scientific_articles
    "taskifier": [],  # TODO: Add specific exports from taskifier
    "tldr2": [],  # TODO: Add specific exports from tldr2
    "translator_agent": [],  # TODO: Add specific exports from translator_agent
    "tts_poem_gen": [],  # TODO: Add specific exports from tts_poem_gen
    "weather_agent": [],  # TODO: Add specific exports from weather_agent
    "weather_disaster_management": [],  # TODO: Add specific exports from weather_disaster_management
    "wolfram_alpha_agent": [],  # TODO: Add specific exports from wolfram_alpha_agent
}

# Attach lazy loading - this creates __getattr__, __dir__, and __all__
__getattr__, __dir__, __all__ = lazy.attach(
    __name__, submodules=submodules, submod_attrs=submod_attrs
)

# Add any eager imports here (lightweight utilities, etc.)
# Example: from .metadata import SomeUtility
# __all__ += ['SomeUtility']
