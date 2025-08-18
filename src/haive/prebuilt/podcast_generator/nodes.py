# Main graph
from langchain_core.messages import HumanMessage
from langgraph.graph import Send

from haive.prebuilt.podcast_generator.prompts import (
    conclusion_instructions,
    intro_instructions,
    report_writer_instructions,
)
from haive.prebuilt.podcast_generator.state import (
    PodcastGeneratorState as ResearchGraphState,
)

# TODO: This needs to be properly imported or defined
podcast_model = None  # This should be defined elsewhere or imported


def initiate_all_interviews(state: ResearchGraphState):
    """This is the "map" step where we run each interview sub-graph using Send API."""
    topic = state["topic"]
    return [
        Send(
            "Create podcast",
            {
                "topic": topic,
                "messages": [
                    HumanMessage(
                        content=f"So you said you were researching about {subtopic}?"
                    )
                ],
            },
        )
        for subtopic in state["subtopics"]
    ]


def write_report(state: ResearchGraphState):
    """Write Report.

Args:
    state: [TODO: Add description]
"""
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report
    system_message = report_writer_instructions.format(
        topic=topic, context=formatted_str_sections
    )
    report = podcast_model.send_message(system_message)
    return {"content": report.text}


def write_introduction(state: ResearchGraphState):
    """Write Introduction.

Args:
    state: [TODO: Add description]
"""
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report

    instructions = intro_instructions.format(
        topic=topic, formatted_str_sections=formatted_str_sections
    )
    intro = podcast_model.send_message(instructions)
    return {"introduction": intro.text}


def write_conclusion(state: ResearchGraphState):
    """Write Conclusion.

Args:
    state: [TODO: Add description]
"""
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report

    instructions = conclusion_instructions.format(
        topic=topic, formatted_str_sections=formatted_str_sections
    )
    conclusion = podcast_model.send_message(instructions)
    return {"conclusion": conclusion.text}


def finalize_report(state: ResearchGraphState):
    """The is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion."""
    # Save full final report
    content = state["content"]
    final_report = (
        state["introduction"]
        + "\n\n---\n\n"
        + content
        + "\n\n---\n\n"
        + state["conclusion"]
    )

    return {"final_report": final_report}


def Start_parallel(state):
    """No-op node that should be interrupted on."""
