"""Example usage for PhD academic research.

This module provides example usage of the Scientific Paper Agent
for various academic research scenarios.

The examples are designed to evaluate the agent on:
- Completing tasks representative of PhD researcher work
- Addressing specific tasks requiring research within defined timeframes
- Tackling tasks across multiple research areas
- Critically evaluating responses using specific paper information
"""

# Example test queries for academic research
test_inputs = [
    "Download and summarize the findings of this paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11379842/pdf/11671_2024_Article_407.pdf",
    "Can you find papers on quantum machine learning?",
    """Find recent papers (2023-2024) about CRISPR applications in treating genetic disorders,
    focusing on clinical trials and safety protocols""",
    """Find and analyze papers from 2023-2024 about the application of transformer architectures in protein folding prediction,
    specifically looking for novel architectural modifications with experimental validation.""",
]


async def run_research_examples():
    """Run research examples with the Scientific Paper Agent.

    This function demonstrates various use cases for academic research
    using the Scientific Paper Agent.
    """
    # TODO: Import and initialize the Scientific Paper Agent
    # from haive.prebuilt.scientific_paper_agent import ScientificPaperAgent
    # agent = ScientificPaperAgent()

    print("Scientific Paper Agent Examples")
    print("=" * 40)

    outputs = []

    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n## Example {i}")
        print(f"Input: {test_input}")

        # TODO: Replace with actual agent call
        # result = await agent.process(test_input)
        # outputs.append(result)

        # Placeholder output
        placeholder_output = f"[Placeholder result for query {i}]"
        outputs.append(placeholder_output)
        print(f"Output: {placeholder_output}")

    return outputs


def run_basic_example():
    """Run a basic synchronous example."""
    print("Basic Scientific Paper Agent Example")
    print("=" * 40)

    # TODO: Initialize agent and process a simple query
    example_query = "Find papers on machine learning applications in biology"
    print(f"Query: {example_query}")
    print("Result: [Placeholder - agent implementation needed]")


async def main():
    """Main example function."""
    print("Scientific Paper Agent - Example Usage")
    print("=" * 50)

    # Run basic example
    run_basic_example()

    print("\n")

    # Run advanced examples
    results = await run_research_examples()

    print(f"\nCompleted {len(results)} research examples")


if __name__ == "__main__":
    # Run basic example (synchronous)
    run_basic_example()

    # Run async examples
    # asyncio.run(main())
