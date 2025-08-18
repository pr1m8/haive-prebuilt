import ast
import os
from typing import List, Union

import openai
import pymupdf4llm
import requests
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from haive.prebuilt.systemic_review_of_scientific_articles.prompts import (
    abstract_prompt,
    analyze_paper_prompt,
    conclusions_prompt,
    critique_draft_prompt,
    decision_prompt,
    introduction_prompt,
    methods_prompt,
    planner_prompt,
    references_prompt,
    research_prompt,
    results_prompt,
    revise_draft_prompt,
)
from haive.prebuilt.systemic_review_of_scientific_articles.state import AgentState
from haive.prebuilt.systemic_review_of_scientific_articles.tools import (
    AcademicPaperSearchTool,
)

# Type aliases
AnyMessage = Union[AIMessage, HumanMessage, SystemMessage, ToolMessage]

# Configuration
model = ChatOpenAI(model="gpt-4o", temperature=0.1)
temperature = 0.1

# Tools setup
tools = {"academic_paper_search_tool": AcademicPaperSearchTool()}


def process_input(state: AgentState):
    """Process Input.

Args:
    state: [TODO: Add description]
"""
    max_revision = 2
    messages = state.get("messages", [])

    last_human_index = len(messages) - 1
    for i in reversed(range(len(messages))):
        if isinstance(messages[i], HumanMessage):
            last_human_index = i
            break

    return {
        "last_human_index": last_human_index,
        "max_revisions": max_revision,
        "revision_num": 1,
    }


def get_relevant_messages(state: AgentState) -> List[AnyMessage]:
    """
    Don't get tool call messages for AI from history.
    Get state from everything up to the most recent human message
    """
    messages = state["messages"]
    filtered_history = []
    for message in messages:
        if isinstance(message, HumanMessage) and message.content != "":
            filtered_history.append(message)
        elif (
            isinstance(message, AIMessage)
            and message.content != ""
            and message.response_metadata["finish_reason"] == "stop"
        ):
            filtered_history.append(message)
    last_human_index = state["last_human_index"]
    return filtered_history[:-1] + messages[last_human_index:]


# Plan Node and Research Node implementations below


def plan_node(state: AgentState):
    """Plan Node.

Args:
    state: [TODO: Add description]
"""
    print("PLANNER")
    relevant_messages = get_relevant_messages(state)
    messages = [SystemMessage(content=planner_prompt)] + relevant_messages
    response = model.invoke(messages, temperature=temperature)
    print(response)
    print()
    return {"systematic_review_outline": [response]}


def research_node(state: AgentState):
    """Research Node.

Args:
    state: [TODO: Add description]
"""
    print("RESEARCHER")
    review_plan = state["systematic_review_outline"]
    messages = [SystemMessage(content=research_prompt)] + review_plan
    response = model.invoke(messages, temperature=temperature)
    print(response)
    print()
    return {"messages": [response]}


def take_action(state: AgentState):
    """Get last message from agent state.
    If we get to this state, the language model wanted to use a tool.
    The tool calls attribute will be attached to message in the Agent State. Can be a list of tool calls.
    Find relevant tool and invoke it, passing in the arguments
    """
    print("GET SEARCH RESULTS")
    last_message = state["messages"][-1]

    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return {"messages": state["messages"]}

    results = []
    for t in last_message.tool_calls:
        print(f"Calling: {t}")

        if t["name"] not in tools:  # check for bad tool name
            print("\n ....bad tool name....")
            result = "bad tool name, retry"  # instruct llm to retry if bad
        else:
            # pass in arguments for tool call
            result = tools[t["name"]].invoke(t["args"])

        # append result as a tool message
        results.append(
            ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(result))
        )

    return {"messages": results}  # langgraph adding to state in between iterations


def decision_node(state: AgentState):
    """Decision Node.

Args:
    state: [TODO: Add description]
"""
    print("DECISION-MAKER")
    review_plan = state["systematic_review_outline"]
    relevant_messages = get_relevant_messages(state)
    messages = (
        [SystemMessage(content=decision_prompt)] + review_plan + relevant_messages
    )
    response = model.invoke(messages, temperature=temperature)
    print(response)
    print()
    return {"messages": [response]}


def article_download(state: AgentState):
    """Article Download.

Args:
    state: [TODO: Add description]
"""
    print("DOWNLOAD PAPERS")
    last_message = state["messages"][-1]

    try:
        # Handle different types of content
        if isinstance(last_message.content, str):
            urls = ast.literal_eval(last_message.content)
        else:
            urls = last_message.content

        filenames = []
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()

                # Create a papers directory if it doesn't exist
                if not os.path.exists("data"):
                    os.makedirs("data")

                # Generate a filename from the URL
                filename = f"data/{url.split('/')[-1]}"
                if not filename.endswith(".pdf"):
                    filename += ".pdf"

                # Save the PDF
                with open(filename, "wb") as f:
                    f.write(response.content)

                filenames.append({"paper": filename})
                print(f"Successfully downloaded: {filename}")

            except Exception as e:
                print(f"Error downloading {url}: {str(e)}")
                continue

        # Return AIMessage instead of raw strings
        return {
            "papers": [
                AIMessage(
                    content=filenames, response_metadata={"finish_reason": "stop"}
                )
            ]
        }

    except Exception as e:
        # Return error as AIMessage
        return {
            "messages": [
                AIMessage(
                    content=f"Error processing downloads: {str(e)}",
                    response_metadata={"finish_reason": "error"},
                )
            ]
        }


def paper_analyzer(state: AgentState):
    """Paper Analyzer.

Args:
    state: [TODO: Add description]
"""
    print("ANALYZE PAPERS")
    analyses = ""
    for paper in state["papers"][-1].content:
        md_text = pymupdf4llm.to_markdown(f"./{paper['paper']}")
        messages = [
            SystemMessage(content=analyze_paper_prompt),
            HumanMessage(content=md_text),
        ]

        model = ChatOpenAI(model="gpt-4o")
        response = model.invoke(messages, temperature=0.1)
        print(response)
        analyses += response.content
    return {"analyses": [analyses]}


def _make_api_call(model, messages, temperature=0.1):
    @retry(
        retry=retry_if_exception_type(openai.RateLimitError),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(5),
    )
    def _call():
        try:
            return model.invoke(messages, temperature=temperature)
        except openai.RateLimitError as e:
            print(f"Rate limit reached. Waiting before retry... ({e})")
            raise

    return _call()


def write_abstract(state: AgentState):
    """Write Abstract.

Args:
    state: [TODO: Add description]
"""
    print("WRITE ABSTRACT")
    review_plan = state["systematic_review_outline"]
    analyses = state["analyses"]
    messages = [SystemMessage(content=abstract_prompt)] + review_plan + analyses
    model = ChatOpenAI(model="gpt-4o-mini")
    response = _make_api_call(model, messages)
    print(response)
    print()
    return {"abstract": [response]}


def write_introduction(state: AgentState):
    """Write Introduction.

Args:
    state: [TODO: Add description]
"""
    print("WRITE INTRODUCTION")
    review_plan = state["systematic_review_outline"]
    analyses = state["analyses"]
    messages = [SystemMessage(content=introduction_prompt)] + review_plan + analyses
    model = ChatOpenAI(model="gpt-4o-mini")
    response = _make_api_call(model, messages)
    print(response)
    print()
    return {"introduction": [response]}


def write_methods(state: AgentState):
    """Write Methods.

Args:
    state: [TODO: Add description]
"""
    print("WRITE METHODS")
    review_plan = state["systematic_review_outline"]
    analyses = state["analyses"]
    messages = [SystemMessage(content=methods_prompt)] + review_plan + analyses
    model = ChatOpenAI(model="gpt-4o-mini")
    response = _make_api_call(model, messages)
    print(response)
    print()
    return {"methods": [response]}


def write_results(state: AgentState):
    """Write Results.

Args:
    state: [TODO: Add description]
"""
    print("WRITE RESULTS")
    review_plan = state["systematic_review_outline"]
    analyses = state["analyses"]
    messages = [SystemMessage(content=results_prompt)] + review_plan + analyses
    model = ChatOpenAI(model="gpt-4o-mini")
    response = _make_api_call(model, messages)
    print(response)
    print()
    return {"results": [response]}


def write_conclusion(state: AgentState):
    """Write Conclusion.

Args:
    state: [TODO: Add description]
"""
    print("WRITE CONCLUSION")
    review_plan = state["systematic_review_outline"]
    analyses = state["analyses"]
    messages = [SystemMessage(content=conclusions_prompt)] + review_plan + analyses
    model = ChatOpenAI(model="gpt-4o-mini")
    response = _make_api_call(model, messages)
    print(response)
    print()
    return {"conclusion": [response]}


def write_references(state: AgentState):
    """Write References.

Args:
    state: [TODO: Add description]
"""
    print("WRITE REFERENCES")
    review_plan = state["systematic_review_outline"]
    analyses = state["analyses"]
    messages = [SystemMessage(content=references_prompt)] + review_plan + analyses
    model = ChatOpenAI(model="gpt-4o-mini")
    response = _make_api_call(model, messages)
    print(response)
    print()
    return {"references": [response]}


def aggregator(state: AgentState):
    """Aggregator.

Args:
    state: [TODO: Add description]
"""
    print("AGGREGATE")
    abstract = state["abstract"][-1].content
    introduction = state["introduction"][-1].content
    methods = state["methods"][-1].content
    results = state["results"][-1].content
    conclusion = state["conclusion"][-1].content
    references = state["references"][-1].content

    messages = [
        SystemMessage(
            content="Make a title for this systematic review based on the abstract. Write it in markdown."
        ),
        HumanMessage(content=abstract),
    ]
    title = model.invoke(messages, temperature=0.1).content

    draft = (
        title
        + "\n\n"
        + abstract
        + "\n\n"
        + introduction
        + "\n\n"
        + methods
        + "\n\n"
        + results
        + "\n\n"
        + conclusion
        + "\n\n"
        + references
    )

    return {"draft": [draft]}


def critique(state: AgentState):
    """Critique.

Args:
    state: [TODO: Add description]
"""
    print("CRITIQUE")
    draft = state["draft"]
    review_plan = state["systematic_review_outline"]

    messages = [SystemMessage(content=critique_draft_prompt)] + review_plan + draft
    response = model.invoke(messages, temperature=temperature)
    print(response)

    # every critique is a call for revision
    return {"messages": [response], "revision_num": state.get("revision_num", 1) + 1}


def paper_reviser(state: AgentState):
    """Paper Reviser.

Args:
    state: [TODO: Add description]
"""
    print("REVISE PAPER")
    critique = state["messages"][-1].content
    draft = state["draft"]

    messages = [SystemMessage(content=revise_draft_prompt)] + [critique] + draft
    response = model.invoke(messages, temperature=temperature)
    print(response)

    return {"draft": [response]}


def exists_action(state: AgentState):
    """
    Determines whether to continue revising, end, or search for more articles
    based on the critique and revision count
    """
    print("DECIDING WHETHER TO REVISE, END, or SEARCH AGAIN")

    if state["revision_num"] > state["max_revisions"]:
        return "final_draft"

    # # Get the latest critique
    critique = state["messages"][-1]
    print(critique)

    # Check if the critique response has any tool calls
    if hasattr(critique, "tool_calls") and critique.tool_calls:
        # The critique suggests we need more research
        return True
    else:
        # No more research needed, proceed with revision
        return "revise"


def final_draft(state: AgentState):
    """Final Draft.

Args:
    state: [TODO: Add description]
"""
    print("FINAL DRAFT")
    return {"draft": state["draft"]}
