"""Misc - TODO: Add brief description

TODO: Add detailed description of module functionality



Example:
    Basic usage::

        from haive.misc import module_function
        
        # TODO: Add example


"""

"""Agent Utilities Module for Haive Agents.

This module provides essential structured models and prompts for common agent tasks
including goal decomposition, decision analysis, resource planning, quality assessment,
workflow optimization, and communication planning.

Classes:
    Goal Decomposition:
        - GoalType: Types of goals (outcome, process, learning, etc.)
        - GoalStatus: Status tracking (not_started, in_progress, completed, etc.)
        - SubGoal: Individual sub-goals with dependencies and success criteria
        - GoalDecomposition: Complete goal breakdown with timeline and risks

    Decision Analysis:
        - DecisionType: Types of decisions (binary, multiple_choice, strategic, etc.)
        - DecisionCriteria: Evaluation criteria with weights and scoring
        - DecisionOption: Individual options with pros/cons and scoring
        - DecisionAnalysis: Complete decision framework with recommendations

    Resource Planning:
        - ResourceType: Categories (human, financial, technical, etc.)
        - ResourceAvailability: Availability status and constraints
        - Resource: Individual resources with capacity and costs
        - ResourcePlan: Comprehensive resource allocation and optimization

    Quality Assessment:
        - QualityDimension: Quality aspects (accuracy, completeness, reliability, etc.)
        - QualityMetric: Measurable quality indicators with targets
        - QualityIssue: Identified problems with severity and solutions
        - QualityAssessment: Complete quality evaluation and improvement plan

    Workflow Optimization:
        - ProcessType: Process categories (linear, parallel, iterative, etc.)
        - BottleneckType: Types of constraints (resource, dependency, approval, etc.)
        - ProcessStep: Individual workflow steps with dependencies
        - WorkflowOptimization: Process analysis and improvement recommendations

    Communication Planning:
        - StakeholderType: Stakeholder categories (sponsor, user, reviewer, etc.)
        - InfluenceLevel: Level of stakeholder influence (high, medium, low)
        - Stakeholder: Individual stakeholders with engagement strategies
        - CommunicationPlan: Comprehensive stakeholder communication strategy

Example:
    ```python
    from haive.agents.common.models.agent_utilities import (
        create_goal_decomposition_agent,
        create_decision_analysis_agent,
        create_resource_planning_agent
    )
    
    # Create specialized agents
    goal_agent = create_goal_decomposition_agent(SimpleAgent)
    decision_agent = create_decision_analysis_agent(SimpleAgent)
    resource_agent = create_resource_planning_agent(SimpleAgent)
    
    # Use for goal planning
    goal_analysis = await goal_agent.ainvoke({
        "goal_description": "Launch a new product within 6 months"
    })
    
    # Use for decision making
    decision_analysis = await decision_agent.ainvoke({
        "decision_description": "Choose between three vendor options for cloud hosting"
    })
    
    # Use for resource planning
    resource_plan = await resource_agent.ainvoke({
        "initiative_description": "Implement new CRM system across organization"
    })
    ```
"""

from haive.prebuilt.misc.agent_utilities_models import (  # Goal Decomposition; Decision Analysis; Resource Planning; Quality Assessment; Workflow Optimization; Communication Planning
    BottleneckType,
    CommunicationFrequency,
    CommunicationPlan,
    DecisionAnalysis,
    DecisionCriteria,
    DecisionOption,
    DecisionType,
    GoalDecomposition,
    GoalStatus,
    GoalType,
    InfluenceLevel,
    InterestLevel,
    PriorityLevel,
    ProcessBottleneck,
    ProcessStep,
    ProcessType,
    QualityAssessment,
    QualityDimension,
    QualityIssue,
    QualityMetric,
    Resource,
    ResourceAvailability,
    ResourcePlan,
    ResourceRequirement,
    ResourceType,
    Stakeholder,
    StakeholderType,
    SubGoal,
    WorkflowOptimization,
)
from haive.prebuilt.misc.agent_utilities_prompts import (  # Prompt Templates; Agent Creation Functions
    AgentUtilitiesPrompts,
    create_communication_planning_agent,
    create_decision_analysis_agent,
    create_goal_decomposition_agent,
    create_quality_assessment_agent,
    create_resource_planning_agent,
    create_workflow_optimization_agent,
)

__all__ = [
    # Enums and Base Types
    "GoalType",
    "PriorityLevel",
    "GoalStatus",
    "DecisionType",
    "ResourceType",
    "ResourceAvailability",
    "QualityDimension",
    "ProcessType",
    "BottleneckType",
    "StakeholderType",
    "InfluenceLevel",
    "InterestLevel",
    "CommunicationFrequency",
    
    # Goal Decomposition Models
    "SubGoal",
    "GoalDecomposition",
    
    # Decision Analysis Models
    "DecisionCriteria",
    "DecisionOption",
    "DecisionAnalysis",
    
    # Resource Planning Models
    "Resource",
    "ResourceRequirement",
    "ResourcePlan",
    
    # Quality Assessment Models
    "QualityMetric",
    "QualityIssue",
    "QualityAssessment",
    
    # Workflow Optimization Models
    "ProcessStep",
    "ProcessBottleneck",
    "WorkflowOptimization",
    
    # Communication Planning Models
    "Stakeholder",
    "CommunicationPlan",