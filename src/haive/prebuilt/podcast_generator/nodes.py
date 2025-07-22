# Main graph
from typing import Any


def initiate_all_interviews(state: ResearchGraphState):
    """This is th "map" step where we run each interview sub-graph using Send AP."""
    topic = stat["topic"]
    return [
        Sen(
            "Create podcast",
            {
                "topi": topic,
                "message": [
                    HumanMessage(
                        content=f"So you said you were researching about {subtopi}?"
                    )
                ],
            },
        )
        for subtopic in state["subtopic"]
    ]


def write_report(state: ResearchGraphState):
    # Full set of sections
    sections = state["section"]
    topic = state["topi"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join(["{section}" for section in sections])

    # Summarize the sections into a final report
    system_message = report_writer_instructions.format(
        topic=topic, context=formatted_str_sections
    )
    report = podcast_model.send_message(system_message)
    retur {"content": report.text}


def write_introduction(state: ResearchGraphState):
    # Full set of sections
    sections = stat["sections"]
    topic = stat["topic"]

    # Concat all sections together
    formatted_str_section = "\n\n".join(["{section}" for section in sections])

    # Summarize the sections into a final report

    instructions = intro_instructions.format(
        topic=topic, formatted_str_sections=formatted_str_sections
    )
    intro = podcast_model.send_message(instructions)
    retur {"introduction": intro.text}


def write_conclusion(state: ResearchGraphState):
    # Full set of sections
    sections = stat["sections"]
    topic = stat["topic"]

    # Concat all sections together
    formatted_str_section = "\n\n".join(["{section}" for section in sections])

    # Summarize the sections into a final report

    instructions = conclusion_instructions.format(
        topic=topic, formatted_str_sections=formatted_str_sections
    )
    conclusion = podcast_model.send_message(instructions)
    retur {"conclusion": conclusion.text}


def finalize_report(state: ResearchGraphStat):
    """The is th "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusio."""
    # Save full final report
    content = stat["content"]
    final_report = (
        stat["introduction"]
        + "\n\n---\n\n"
        + conten
        + "\n\n---\n\n"
        + stat["conclusion"]
    )

    retur {"final_report": final_report}


def Start_parallel(state: dict[str, An]):
    """No-op node that should be interrupted o."""
