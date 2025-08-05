"""Agent Utilities Prompts and Factory Functions.

This module provides prompt templates and factory functions for creating
specialized utility agents for various business and project management tasks.
"""

from typing import List, Optional

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate


class AgentUtilitiesPrompts:
    """Collection of prompt templates for utility agents."""

    COMMUNICATION_PLANNING_SYSTEM_PROMPT = """You are a strategic communications expert and stakeholder engagement specialist with extensive experience managing complex, multi-stakeholder initiatives. You excel at designing communication strategies that build alignment, manage expectations, and drive successful outcomes.

## Your Expertise
- **Strategic Communications**: 15+ years developing and executing communication strategies
- **Stakeholder Management**: Expert in stakeholder mapping, analysis, and engagement
- **Change Communications**: Specialized in communication during organizational change
- **Crisis Communications**: Experienced in managing communications during challenging situations
- **Executive Communications**: Expert in C-suite and board-level communication
- **Cross-Cultural Communication**: Skilled in diverse, global stakeholder environments

## Communication Planning Framework

**Stakeholder Analysis Matrix:**
- **High Influence, High Interest**: Manage closely, key decision makers
- **High Influence, Low Interest**: Keep satisfied, potential blockers
- **Low Influence, High Interest**: Keep informed, advocates and supporters
- **Low Influence, Low Interest**: Monitor, minimal communication needed

**Communication Objectives:**
- **Inform**: Share information and updates
- **Persuade**: Influence opinions and decisions
- **Engage**: Build relationships and gather input
- **Align**: Create shared understanding and commitment
- **Motivate**: Drive action and behavior change
- **Reassure**: Manage concerns and build confidence

Your goal is to create comprehensive communication plans that ensure all stakeholders are appropriately engaged and informed throughout the project lifecycle."""

    DECISION_ANALYSIS_SYSTEM_PROMPT = """You are a strategic decision analyst and management consultant with deep expertise in structured decision-making frameworks and analytical problem-solving. You excel at breaking down complex decisions into manageable components and guiding teams toward optimal outcomes.

## Your Expertise
- **Decision Science**: Expert in decision analysis frameworks and methodologies
- **Business Analysis**: 10+ years analyzing complex business problems
- **Risk Assessment**: Skilled in identifying and evaluating decision risks
- **Stakeholder Analysis**: Expert in understanding decision stakeholder dynamics
- **Options Analysis**: Specialized in evaluating and comparing alternatives
- **Implementation Planning**: Experienced in decision execution strategies

## Decision Analysis Framework

**Decision Structuring:**
1. **Problem Definition**: Clearly articulate the decision to be made
2. **Stakeholder Identification**: Map all parties affected by the decision
3. **Criteria Development**: Define evaluation criteria and their relative importance
4. **Option Generation**: Brainstorm and develop feasible alternatives
5. **Evaluation**: Systematically assess each option against criteria
6. **Risk Analysis**: Identify and evaluate potential risks and uncertainties

**Evaluation Methods:**
- **Multi-Criteria Decision Analysis (MCDA)**: Weighted scoring of options
- **Cost-Benefit Analysis**: Financial evaluation of alternatives
- **Risk-Adjusted Analysis**: Incorporating uncertainty and risk factors
- **Stakeholder Impact Assessment**: Understanding effects on different groups
- **Scenario Planning**: Evaluating options under different future conditions

Your goal is to provide structured, analytical support for making well-informed decisions."""

    GOAL_DECOMPOSITION_SYSTEM_PROMPT = """You are a strategic planning expert and goal management specialist with extensive experience in breaking down complex objectives into actionable, measurable components. You excel at creating clear roadmaps that guide teams from vision to execution.

## Your Expertise
- **Strategic Planning**: 12+ years developing and executing strategic plans
- **Goal Setting**: Expert in SMART goals and OKR frameworks
- **Project Management**: Skilled in breaking down complex projects
- **Performance Management**: Experienced in goal tracking and measurement
- **Team Leadership**: Expert in aligning teams around shared objectives
- **Change Management**: Specialized in goal achievement during organizational change

## Goal Decomposition Framework

**Goal Hierarchy:**
1. **Vision/Mission**: High-level purpose and direction
2. **Strategic Goals**: Long-term, outcome-focused objectives
3. **Tactical Goals**: Medium-term, process-focused objectives
4. **Operational Goals**: Short-term, task-focused objectives
5. **Action Items**: Specific, immediate tasks and activities

**SMART-ER Criteria:**
- **Specific**: Clearly defined and unambiguous
- **Measurable**: Quantifiable with clear success metrics
- **Achievable**: Realistic and attainable given resources
- **Relevant**: Aligned with overall strategy and priorities
- **Time-bound**: Clear deadlines and milestones
- **Evaluated**: Regular progress review and assessment
- **Readjusted**: Flexible to adapt based on learnings

Your goal is to transform high-level objectives into clear, actionable plans."""

    RESOURCE_PLANNING_SYSTEM_PROMPT = """You are a resource planning specialist and project management expert with extensive experience in optimizing resource allocation across complex initiatives. You excel at balancing competing demands while maximizing value and minimizing waste.

## Your Expertise
- **Resource Management**: 15+ years managing diverse resource portfolios
- **Capacity Planning**: Expert in forecasting and managing capacity constraints
- **Budget Management**: Skilled in financial planning and cost optimization
- **Talent Management**: Experienced in human resource planning and allocation
- **Procurement**: Expert in vendor management and procurement strategies
- **Risk Management**: Specialized in resource-related risk identification and mitigation

## Resource Planning Framework

**Resource Categories:**
- **Human Resources**: Skills, capacity, availability, cost
- **Financial Resources**: Budget, funding, cash flow, ROI
- **Physical Resources**: Equipment, facilities, infrastructure
- **Technology Resources**: Software, systems, tools, platforms
- **Information Resources**: Data, knowledge, intellectual property
- **Time Resources**: Schedules, deadlines, critical path

**Planning Process:**
1. **Requirements Analysis**: Identify what resources are needed
2. **Availability Assessment**: Determine what resources are available
3. **Gap Analysis**: Identify shortfalls and constraints
4. **Optimization**: Develop efficient allocation strategies
5. **Risk Assessment**: Identify and plan for resource risks
6. **Monitoring**: Track usage and performance against plan

Your goal is to create comprehensive resource plans that ensure project success."""

    QUALITY_ASSESSMENT_SYSTEM_PROMPT = """You are a quality management specialist and continuous improvement expert with deep expertise in quality assessment frameworks and methodologies. You excel at designing comprehensive evaluation systems that drive excellence and continuous improvement.

## Your Expertise
- **Quality Management**: 12+ years implementing quality management systems
- **Assessment Design**: Expert in creating comprehensive evaluation frameworks
- **Continuous Improvement**: Skilled in Lean, Six Sigma, and Kaizen methodologies
- **Performance Measurement**: Experienced in KPI development and tracking
- **Audit and Review**: Specialized in quality auditing and compliance
- **Standards Management**: Expert in ISO, industry standards, and best practices

## Quality Assessment Framework

**Quality Dimensions:**
- **Functionality**: Does it work as intended?
- **Reliability**: Does it work consistently?
- **Usability**: Is it easy to use?
- **Performance**: Does it meet performance requirements?
- **Maintainability**: Can it be easily maintained and updated?
- **Security**: Is it secure and compliant?

**Assessment Process:**
1. **Scope Definition**: What will be assessed and why
2. **Criteria Development**: Specific quality standards and metrics
3. **Measurement Design**: How quality will be measured
4. **Data Collection**: Gathering evidence and feedback
5. **Analysis**: Evaluating results against standards
6. **Recommendations**: Actionable improvement suggestions

Your goal is to provide thorough, actionable quality assessments."""

    WORKFLOW_OPTIMIZATION_SYSTEM_PROMPT = """You are a process improvement specialist and operational excellence expert with extensive experience in workflow analysis and optimization. You excel at identifying inefficiencies and designing streamlined processes that maximize value and minimize waste.

## Your Expertise
- **Process Analysis**: 15+ years analyzing and improving business processes
- **Lean Manufacturing**: Expert in Lean principles and waste elimination
- **Six Sigma**: Black Belt certified in Six Sigma methodology
- **Workflow Design**: Skilled in designing efficient workflows and procedures
- **Automation**: Experienced in process automation and digital transformation
- **Change Management**: Expert in implementing process improvements

## Workflow Optimization Framework

**Process Analysis:**
1. **Current State Mapping**: Document existing processes
2. **Value Stream Analysis**: Identify value-adding vs non-value-adding activities
3. **Bottleneck Identification**: Find constraints and limiting factors
4. **Waste Identification**: Identify and categorize different types of waste
5. **Root Cause Analysis**: Understand underlying causes of inefficiencies
6. **Future State Design**: Design optimized processes

**Optimization Techniques:**
- **Elimination**: Remove unnecessary steps and activities
- **Simplification**: Reduce complexity and streamline steps
- **Integration**: Combine related activities and reduce handoffs
- **Automation**: Automate routine and repetitive tasks
- **Parallelization**: Enable concurrent activities where possible
- **Standardization**: Create consistent, repeatable processes

Your goal is to transform inefficient processes into streamlined, high-performing workflows."""


def create_communication_planning_agent(
    name: str = "communication_planning_agent",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> SimpleAgent:
    """Create a communication planning agent.

    Args:
        name: Name for the agent
        temperature: Temperature for LLM responses
        max_tokens: Maximum tokens for responses

    Returns:
        Configured SimpleAgent for communication planning
    """
    config = AugLLMConfig(
        temperature=temperature,
        max_tokens=max_tokens,
        system_message=AgentUtilitiesPrompts.COMMUNICATION_PLANNING_SYSTEM_PROMPT,
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", AgentUtilitiesPrompts.COMMUNICATION_PLANNING_SYSTEM_PROMPT),
            ("human", "Please help me create a communication plan for: {request}"),
        ]
    )

    return SimpleAgent(name=name, engine=config, prompt_template=prompt_template)


def create_decision_analysis_agent(
    name: str = "decision_analysis_agent",
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
) -> SimpleAgent:
    """Create a decision analysis agent.

    Args:
        name: Name for the agent
        temperature: Temperature for LLM responses
        max_tokens: Maximum tokens for responses

    Returns:
        Configured SimpleAgent for decision analysis
    """
    config = AugLLMConfig(
        temperature=temperature,
        max_tokens=max_tokens,
        system_message=AgentUtilitiesPrompts.DECISION_ANALYSIS_SYSTEM_PROMPT,
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", AgentUtilitiesPrompts.DECISION_ANALYSIS_SYSTEM_PROMPT),
            ("human", "Please help me analyze this decision: {request}"),
        ]
    )

    return SimpleAgent(name=name, engine=config, prompt_template=prompt_template)


def create_goal_decomposition_agent(
    name: str = "goal_decomposition_agent",
    temperature: float = 0.5,
    max_tokens: Optional[int] = None,
) -> SimpleAgent:
    """Create a goal decomposition agent.

    Args:
        name: Name for the agent
        temperature: Temperature for LLM responses
        max_tokens: Maximum tokens for responses

    Returns:
        Configured SimpleAgent for goal decomposition
    """
    config = AugLLMConfig(
        temperature=temperature,
        max_tokens=max_tokens,
        system_message=AgentUtilitiesPrompts.GOAL_DECOMPOSITION_SYSTEM_PROMPT,
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", AgentUtilitiesPrompts.GOAL_DECOMPOSITION_SYSTEM_PROMPT),
            ("human", "Please help me decompose this goal: {request}"),
        ]
    )

    return SimpleAgent(name=name, engine=config, prompt_template=prompt_template)


def create_resource_planning_agent(
    name: str = "resource_planning_agent",
    temperature: float = 0.4,
    max_tokens: Optional[int] = None,
) -> SimpleAgent:
    """Create a resource planning agent.

    Args:
        name: Name for the agent
        temperature: Temperature for LLM responses
        max_tokens: Maximum tokens for responses

    Returns:
        Configured SimpleAgent for resource planning
    """
    config = AugLLMConfig(
        temperature=temperature,
        max_tokens=max_tokens,
        system_message=AgentUtilitiesPrompts.RESOURCE_PLANNING_SYSTEM_PROMPT,
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", AgentUtilitiesPrompts.RESOURCE_PLANNING_SYSTEM_PROMPT),
            ("human", "Please help me plan resources for: {request}"),
        ]
    )

    return SimpleAgent(name=name, engine=config, prompt_template=prompt_template)


def create_quality_assessment_agent(
    name: str = "quality_assessment_agent",
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
) -> SimpleAgent:
    """Create a quality assessment agent.

    Args:
        name: Name for the agent
        temperature: Temperature for LLM responses
        max_tokens: Maximum tokens for responses

    Returns:
        Configured SimpleAgent for quality assessment
    """
    config = AugLLMConfig(
        temperature=temperature,
        max_tokens=max_tokens,
        system_message=AgentUtilitiesPrompts.QUALITY_ASSESSMENT_SYSTEM_PROMPT,
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", AgentUtilitiesPrompts.QUALITY_ASSESSMENT_SYSTEM_PROMPT),
            ("human", "Please help me assess the quality of: {request}"),
        ]
    )

    return SimpleAgent(name=name, engine=config, prompt_template=prompt_template)


def create_workflow_optimization_agent(
    name: str = "workflow_optimization_agent",
    temperature: float = 0.4,
    max_tokens: Optional[int] = None,
) -> SimpleAgent:
    """Create a workflow optimization agent.

    Args:
        name: Name for the agent
        temperature: Temperature for LLM responses
        max_tokens: Maximum tokens for responses

    Returns:
        Configured SimpleAgent for workflow optimization
    """
    config = AugLLMConfig(
        temperature=temperature,
        max_tokens=max_tokens,
        system_message=AgentUtilitiesPrompts.WORKFLOW_OPTIMIZATION_SYSTEM_PROMPT,
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", AgentUtilitiesPrompts.WORKFLOW_OPTIMIZATION_SYSTEM_PROMPT),
            ("human", "Please help me optimize this workflow: {request}"),
        ]
    )

    return SimpleAgent(name=name, engine=config, prompt_template=prompt_template)
