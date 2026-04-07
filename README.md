# haive-prebuilt

[![PyPI version](https://img.shields.io/pypi/v/haive-prebuilt.svg)](https://pypi.org/project/haive-prebuilt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/haive-prebuilt.svg)](https://pypi.org/project/haive-prebuilt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/pr1m8/haive-prebuilt/actions/workflows/ci.yml/badge.svg)](https://github.com/pr1m8/haive-prebuilt/actions/workflows/ci.yml)
[![Docs](https://github.com/pr1m8/haive-prebuilt/actions/workflows/docs.yml/badge.svg)](https://pr1m8.github.io/haive-prebuilt/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/haive-prebuilt/dm/haive-prebuilt.svg)](https://pypi.org/project/haive-prebuilt/)

**Pre-configured Haive agent presets and templates for common use cases.**

40+ ready-to-deploy agents for specific business domains: customer support, research, content generation, code review, and more. Built on the Haive framework with sensible defaults — drop in and use, or customize as needed.

---

## Why haive-prebuilt?

The Haive framework gives you the building blocks. `haive-prebuilt` gives you the finished products. Each agent is:

- **Pre-tuned** — Temperature, system message, and tools selected for the use case
- **Domain-specific** — Configured for a particular industry or task
- **Production-ready** — Tested with real LLMs (no mocks)
- **Customizable** — Override any setting via the standard Haive config pattern

Use `haive-prebuilt` when you need an agent for a common use case and don't want to start from scratch. Use the foundation packages (`haive-core`, `haive-agents`) when you need something custom.

---

## Available Agents

### Customer Support
- **Customer Support Agent** — Multi-turn conversation with escalation
- **FAQ Bot** — Document-grounded Q&A
- **Ticket Triage Agent** — Classify and route support tickets

### Research & Analysis
- **Market Research Agent** — Web search + synthesis for market analysis
- **Competitive Analysis Agent** — Compare products/companies
- **Trend Analyst** — Identify and report on trends

### Content Generation
- **Blog Writer** — Long-form content with research
- **Social Media Manager** — Posts for Twitter, LinkedIn, etc.
- **Email Drafter** — Professional email drafting
- **Newsletter Generator** — Curated weekly newsletters

### Code & Development
- **Code Reviewer** — Reviews PRs and suggests improvements
- **Bug Triage Agent** — Classify and prioritize bug reports
- **Documentation Generator** — Auto-generate docstrings and READMEs

### Data & Analytics
- **Data Analyst** — Pandas + SQL for data exploration
- **Report Generator** — Convert data into narrative reports
- **Anomaly Detector** — Identify outliers in datasets

### Domain-Specific
- **Legal Document Reviewer**
- **Medical Note Summarizer**
- **Financial Analyst**
- **HR Resume Screener**

---

## Quick Start

```python
from haive.prebuilt import get_agent

# Get a pre-configured agent
agent = get_agent("customer_support")
result = agent.run("How do I reset my password?")

# Or instantiate directly
from haive.prebuilt.customer_support import CustomerSupportAgent
agent = CustomerSupportAgent(
    company_name="Acme Corp",
    knowledge_base_url="https://docs.acme.com",
)
```

---

## Customization

Every prebuilt agent uses standard Haive patterns. Override any config:

```python
from haive.prebuilt.research import MarketResearchAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Override the engine
agent = MarketResearchAgent(
    engine=AugLLMConfig(
        model="claude-opus-4-6",
        temperature=0.5,
        system_message="Custom instructions...",
    ),
    max_iterations=10,
)
```

---

## Installation

```bash
pip install haive-prebuilt
```

---

## Documentation

📖 **Full documentation:** https://pr1m8.github.io/haive-prebuilt/

---

## Related Packages

| Package | Description |
|---------|-------------|
| [haive-core](https://pypi.org/project/haive-core/) | Foundation: engines, graphs |
| [haive-agents](https://pypi.org/project/haive-agents/) | Production agent implementations |
| [haive-tools](https://pypi.org/project/haive-tools/) | Tool implementations |

---

## License

MIT © [pr1m8](https://github.com/pr1m8)
