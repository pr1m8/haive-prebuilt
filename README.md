# haive-prebuilt

[![PyPI version](https://img.shields.io/pypi/v/haive-prebuilt.svg)](https://pypi.org/project/haive-prebuilt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/haive-prebuilt.svg)](https://pypi.org/project/haive-prebuilt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/pr1m8/haive-prebuilt/actions/workflows/ci.yml/badge.svg)](https://github.com/pr1m8/haive-prebuilt/actions/workflows/ci.yml)
[![Docs](https://github.com/pr1m8/haive-prebuilt/actions/workflows/docs.yml/badge.svg)](https://pr1m8.github.io/haive-prebuilt/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/haive-prebuilt.svg)](https://pypi.org/project/haive-prebuilt/)

**Pre-configured Haive agent presets and templates for common use cases.**

40+ ready-to-deploy agents for specific business domains: customer support, research, content generation, code review, and more. Built on the Haive framework, configured for production use.

## Installation

```bash
pip install haive-prebuilt
```

## Features

- **🎯 Domain-specific** — Pre-tuned for specific industries and use cases
- **⚡ Zero-config** — Works out of the box with sensible defaults
- **🔧 Customizable** — Override any setting via the standard Haive config pattern
- **📦 Complete** — Each agent includes prompts, tools, state schemas, and workflows

## Quick Start

```python
from haive.prebuilt import get_agent

# Get a pre-configured agent
agent = get_agent("customer_support")
result = agent.run("How do I reset my password?")
```

## Documentation

📖 **Full documentation:** https://pr1m8.github.io/haive-prebuilt/

## Related Packages

| Package | Description |
|---------|-------------|
| [haive-core](https://pypi.org/project/haive-core/) | Foundation: engines, graphs |
| [haive-agents](https://pypi.org/project/haive-agents/) | Production agents |

## License

MIT © [pr1m8](https://github.com/pr1m8)
