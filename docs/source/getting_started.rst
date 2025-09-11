Getting Started with Haive Prebuilt Agents
==========================================

Welcome to Haive Prebuilt - the fastest way to deploy specialized AI agents for business, research, and creative applications.

.. note::
   **Beta Status**: This package is currently being refactored into the new dynamic agent architecture. 
   All agents are functional, but APIs may evolve. Pin to specific versions for production use.

Installation
------------

Install via poetry in your project::

    poetry add haive-prebuilt

Or include in your ``pyproject.toml``::

    [tool.poetry.dependencies]
    haive-prebuilt = "^0.1.0"

Quick Start
-----------

Deploy your first specialized agent in under 5 minutes:

**Business Intelligence Agent**::

    from haive.prebuilt.company_researcher import CompanyResearcher
    from haive.core.engine.aug_llm import AugLLMConfig
    
    # Create configuration
    config = AugLLMConfig(
        temperature=0.3,  # More deterministic for business analysis
        max_tokens=2000
    )
    
    # Deploy company research agent
    researcher = CompanyResearcher(name="BusinessAnalyst", engine=config)
    
    # Analyze a company
    result = await researcher.arun(
        "Provide a comprehensive analysis of Apple Inc. including financial performance, market position, and competitive advantages"
    )

**Creative Content Agent**::

    from haive.prebuilt.blog_writer_agent import BlogWriterAgent
    
    # Deploy content creation agent
    writer = BlogWriterAgent(
        name="ContentCreator", 
        engine=AugLLMConfig(temperature=0.8)  # More creative
    )
    
    # Generate blog content
    article = await writer.arun(
        "Write a 1500-word blog post about the future of renewable energy, targeting a general audience"
    )

**Research Assistant Agent**::

    from haive.prebuilt.scientific_paper_agent import ScientificPaperAgent
    
    # Deploy research agent
    research_agent = ScientificPaperAgent(
        name="ResearchAssistant",
        engine=AugLLMConfig(temperature=0.2)  # More precise
    )
    
    # Analyze research papers
    analysis = await research_agent.arun(
        "Analyze the methodology and findings of recent papers on quantum computing applications in cryptography"
    )

Agent Categories Overview
-------------------------

**💼 Business Intelligence (5+ Agents)**
   - Company Researcher: Market analysis and competitive intelligence
   - Sales Call Analyzer: Performance optimization and insights  
   - Customer Support: Automated customer service
   - Project Manager: Task coordination and planning
   - Career Assistant: Professional development guidance

**🔬 Research & Academia (5+ Agents)**
   - Scientific Paper Agent: Research analysis and synthesis
   - Academic Task Learning: Educational content creation
   - Systematic Review: Literature review automation
   - Open Researcher: Open science collaboration
   - Essay Grading: Academic assessment

**🎨 Creative & Content (5+ Agents)**
   - Blog Writer Agent: Professional content creation
   - Podcast Generator: Audio content production
   - GIF Generator: Visual content creation
   - TTS Poem Generator: Poetry and audio content
   - Content Intelligence: Content optimization

**⚖️ Legal & Compliance (4+ Agents)**
   - Contract Analysis: Legal document review
   - Clause AI: Contract optimization
   - EU Green Compliance: Environmental compliance
   - Constitutional Agent: Legal framework analysis

**🛠️ Technical & Development (4+ Agents)**
   - DB Discovery: Database analysis
   - Graph Inspector: Data structure analysis
   - E2E Testing: Test automation
   - Self Improving: Adaptive agents

**🚀 Startup & Innovation (4+ Agents)**
   - Startup Suite: Business planning
   - AI Insight: Technology trend analysis
   - GTLA: Go-to-market assistance  
   - Shop Genie: E-commerce optimization

Configuration Patterns
-----------------------

**Temperature Guidelines**::

    # Business & Legal (Precision)
    config = AugLLMConfig(temperature=0.1)
    
    # Research & Analysis (Balanced)  
    config = AugLLMConfig(temperature=0.3)
    
    # General Purpose (Default)
    config = AugLLMConfig(temperature=0.7)
    
    # Creative & Content (Creative)
    config = AugLLMConfig(temperature=0.9)

**Structured Output**::

    from pydantic import BaseModel, Field
    
    class CompanyAnalysis(BaseModel):
        financial_health: str = Field(description="Financial assessment")
        market_position: str = Field(description="Competitive position") 
        risk_factors: list[str] = Field(description="Key risks")
        opportunities: list[str] = Field(description="Growth opportunities")
    
    # Use with structured output
    config = AugLLMConfig(structured_output_model=CompanyAnalysis)
    researcher = CompanyResearcher(name="analyst", engine=config)

Multi-Agent Workflows
---------------------

Combine multiple prebuilt agents for complex workflows::

    from haive.agents.multi import MultiAgent
    from haive.prebuilt.company_researcher import CompanyResearcher  
    from haive.prebuilt.blog_writer_agent import BlogWriterAgent
    from haive.prebuilt.contract_analysis import ContractAnalyzer
    
    # Create specialized workflow
    due_diligence_workflow = MultiAgent(
        name="due_diligence_pipeline",
        agents=[
            CompanyResearcher(name="researcher", engine=research_config),
            ContractAnalyzer(name="legal", engine=legal_config),
            BlogWriterAgent(name="reporter", engine=content_config)
        ],
        execution_mode="sequential"
    )
    
    # Execute comprehensive analysis
    result = await due_diligence_workflow.arun(
        "Perform due diligence on TechCorp acquisition including company analysis, contract review, and summary report"
    )

Best Practices
--------------

**1. Choose the Right Agent**::

    # For factual analysis - use research agents
    from haive.prebuilt.open_researcher import OpenResearcher
    
    # For creative work - use content agents  
    from haive.prebuilt.podcast_generator import PodcastGenerator
    
    # For business tasks - use business agents
    from haive.prebuilt.sales_call_analyzer import SalesCallAnalyzer

**2. Configure Appropriately**::

    # Match temperature to task type
    factual_config = AugLLMConfig(temperature=0.1)      # Precise
    balanced_config = AugLLMConfig(temperature=0.5)     # Balanced  
    creative_config = AugLLMConfig(temperature=0.9)     # Creative

**3. Use Structured Output When Needed**::

    # For consistent data extraction
    config = AugLLMConfig(structured_output_model=YourModel)
    
    # For integration with downstream systems
    agent = YourPrebuiltAgent(engine=config)

**4. Monitor and Optimize**::

    # Enable debug mode during development
    result = await agent.arun(input_data, debug=True)
    
    # Log performance metrics
    import logging
    logging.getLogger("haive.prebuilt").setLevel(logging.INFO)

Common Deployment Patterns
---------------------------

**Standalone Service**::

    # Single-purpose deployment
    customer_support = CustomerSupportAgent(
        name="support_bot",
        engine=AugLLMConfig(temperature=0.4)
    )
    
    # API endpoint integration
    async def handle_support_request(request):
        return await customer_support.arun(request.message)

**Background Processing**::

    # Batch processing workflow
    document_analyzer = ContractAnalyzer(name="batch_processor")
    
    for document in document_queue:
        analysis = await document_analyzer.arun(document.content)
        save_analysis(document.id, analysis)

**Real-time Integration**::

    # Streaming/real-time processing
    content_optimizer = ContentIntelligenceAgent(name="optimizer")
    
    async def optimize_content(content_stream):
        async for content in content_stream:
            optimized = await content_optimizer.arun(content)
            yield optimized

Troubleshooting
---------------

**Common Issues**

1. **Import Errors**: Ensure haive-core is installed::

    poetry add haive-core

2. **Configuration Issues**: Check engine configuration::

    config = AugLLMConfig()  # Uses defaults
    print(config.validate_configuration())

3. **Performance Issues**: Adjust temperature and max_tokens::

    # For faster responses
    config = AugLLMConfig(max_tokens=500, temperature=0.5)

4. **Memory Issues**: Use streaming for large inputs::

    # Process in chunks for large documents
    result = await agent.arun(content_chunk, stream=True)

**Debug Mode**::

    # Enable detailed logging
    import logging
    logging.getLogger("haive").setLevel(logging.DEBUG)
    
    # Use debug flag
    result = await agent.arun(input_data, debug=True)
    print(f"Execution time: {result.execution_time}ms")

Next Steps
----------

- :doc:`agent_overview` - Detailed overview of all available agents
- :doc:`configuration` - Advanced configuration options  
- :doc:`examples` - Real-world usage examples
- :doc:`business/company_researcher` - Business intelligence deep dive
- :doc:`creative/blog_writer_agent` - Content creation guide

Need Help?
----------

- **Documentation**: Browse agent-specific guides
- **GitHub Issues**: https://github.com/pr1m8/haive-prebuilt/issues  
- **Discord**: Join the Haive community
- **Enterprise Support**: enterprise@haive.ai