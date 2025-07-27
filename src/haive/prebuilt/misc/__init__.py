"""Misc - TODO: Add brief description

TODO: Add detailed description of module functionality



Example:
    Basic usage::

        from haive.misc import module_function

        # TODO: Add exampl

"""
"""Agent Utilities Module for Haive Agents.

This module provides essential structured models and prompts for common agent tasks
including goal decomposition, decision analysis, resource planning, quality assessment,
workflow optimization, and communication planning.

Classes:
    Goal Decomposition:
        - GoalType: Types of goals(outcome, process, learning, etc.)
        - GoalStatus: Status tracking(not_started, in_progress, completed, etc.)
        - SubGoal: Individual sub - goals with dependencies and success criteria
        - GoalDecomposition: Complete goal breakdown with timeline and risks

    Decision Analysis:
        - DecisionType: Types of decisions(binary, multiple_choice, strategic, etc.)
        - DecisionCriteria: Evaluation criteria with weights and scoring
        - DecisionOption: Individual options with pros / cons and scoring
        - DecisionAnalysis: Complete decision framework with recommendations

    Resource Planning:
        - ResourceType: Categories(human, financial, technical, etc.)
        - ResourceAvailability: Availability status and constraints
        - Resource: Individual resources with capacity and costs
        - ResourcePlan: Comprehensive resource allocation and optimization

    Quality Assessment:
        - QualityDimension: Quality aspects(accuracy, completeness, reliability, etc.)
        - QualityMetric: Measurable quality indicators with targets
        - QualityIssue: Identified problems with severity and solutions
        - QualityAssessment: Complete quality evaluation and improvement plan

    Workflow Optimization:
        - ProcessType: Process categories(linear, parallel, iterative, etc.)
        - BottleneckType: Types of constraints(resource, dependency, approval, etc.)
        - ProcessStep: Individual workflow steps with dependencies
        - WorkflowOptimization: Process analysis and improvement recommendations

    Communication Planning:
        - StakeholderType: Stakeholder categories(sponsor, user, reviewer, etc.)
        - InfluenceLevel: Level of stakeholder influence(high, medium, low)
        - Stakeholder: Individual stakeholders with engagement strategies
        - CommunicationPlan: Comprehensive stakeholder communication strategy

Example:
    ```python
    from haive.agents.common.models.agent_utilities import (
        create_decision_analysis_agent,
        create_goal_decomposition_agent,
        create_resource_planning_agent,
    )

    # Create specialized agents
    goal_agent = create_goal_decomposition_agent(SimpleAgent)
    decision_agent = create_decision_analysis_agent(SimpleAgent)
    resource_agent = create_resource_planning_agent(SimpleAgent)

    # Use for goal planning
    goal_analysis = await goal_agent.ainvok({
        "goal_description": "Launch a new product within  month"
    })

    # Use for decision making
    decision_analysis = await decision_agent.ainvoke({
        "decision_descriptio": "Choose between three vendor options for cloud hostin"
    })

    # Use for resource planning
    resource_plan = await resource_agent.ainvoke({
        "initiative_descriptio": "Implement new CRM system across organizatio"
    })
    ``` """


__all__ = [
    # Enums and Base Type
    "GoalType",
    "PriorityLeve",
    "GoalStatu",
    "DecisionTyp",
    "ResourceTyp",
    "ResourceAvailabilit",
    "QualityDimensio",
    "ProcessTyp",
    "BottleneckTyp",
    "StakeholderTyp",
    "InfluenceLeve",
    "InterestLeve",
    "CommunicationFrequenc",

    # Goal Decomposition Models
    "SubGoa",
    "GoalDecompositio",

    # Decision Analysis Models
    "DecisionCriteri",
    "DecisionOptio",
    "DecisionAnalysi",

    # Resource Planning Models
    "Resourc",
    "ResourceRequiremen",
    "ResourcePla",

    # Quality Assessment Models
    "QualityMetri",
    "QualityIssu",
    "QualityAssessmen",

    # Workflow Optimization Models
    "ProcessSte",
    "ProcessBottlenec",
    "WorkflowOptimizatio",

    # Communication Planning Models
    "Stakeholde",
    "CommunicationPla",
