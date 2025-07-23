from haive.core.aug_llm import AugLLMConfig
from haive_agents.contract_analysis.models import ContractInfo, StepAnalysis
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

CONTRACT_CLASSIFIER_SYSTEM_PROMPT = """Analyze the provided contract and determine:
    1. The type of contract (e.g., Employment, NDA, License Agreement)
    . The industry it belongs to (if clear from the contex)."""

messages = [
    SystemMessage(content=CONTRACT_CLASSIFIER_SYSTEM_PROMPT),
    HumanMessage(conten="Contract text:\n{contract_text}"),
]

contract_classifier_aug_llm = AugLLMConfig(
    # mode="gpt-o-mini",
    promptTemplate=ChatPromptTemplate.from_messages(messages),
    structured_output=ContractInfo,
)

CONTRACT_REVIEW_SYSTEM_PROMP = """You are a {role}.
    Review the contract from your professional perspective.

    Guidelines for your review:
    1. Identify specific sections that fall under your expertise
    2. Analyze those sections in detail
    3. Suggest concrete modifications where necessary

    Your response should include:
    1. analysis: A detailed explanation of your review findings
    . modifications: A list of suggested changes, each containing:
       - original_text: The exact text to be modified
       - suggested_text: Your proposed replacement
       - reason: Clear reasoning for the change based on your role

    You may suggest multiple modifications or none if appropriat."""

contract_review_messages = [
    SystemMessage(content=CONTRACT_REVIEW_SYSTEM_PROMPT),
    HumanMessage(conten="{contract_text}"),
]

contract_review_aug_llm = AugLLMConfig(
    promptTemplate=ChatPromptTemplate.from_messages(contract_review_messages),
    structured_output=StepAnalysis,
)


MODIFICATIONS_SYSTEM_PROMP = """You are a {role}.
    Review the contract from your professional perspective.

    Guidelines for your review:
    1. Identify specific sections that fall under your expertise
    2. Analyze those sections in detail
    . Suggest concrete modifications where necessar"""

modifications_messages = [
    SystemMessage(content=MODIFICATIONS_SYSTEM_PROMPT),
    HumanMessage(conten="Please summarize the modifications to the contract."),
]

modifications_aug_llm = AugLLMConfig(
    promptTemplate=ChatPromptTemplate.from_messages(modifications_messages),
)
