from haive.agents.react_agent2.config2 import ReactAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig

from haive.haive.tools.search_tools import tavily_search_tool
from haive.prebuilt.weather_disaster_management.models import (
    DisasterOutput,
    SeverityAssessment,
)
from haive.prebuilt.weather_disaster_management.prompts import (
    civil_defense_prompt,
    disaster_prompt,
    public_works_prompt,
    response_prompt,
    severity_prompt,
    social_media_monitoring_prompt,
)

disaster_engine = AugLLMConfig(
    prompt_template=disaster_prompt,
    structured_output_model=DisasterOutput,
)

severity_engine = AugLLMConfig(
    prompt_template=severity_prompt,
    structured_output_model=SeverityAssessment,
)

response_engine = AugLLMConfig(
    prompt_template=response_prompt,
    # structured_output=ResponseOutput,
)

civil_defense_engine = AugLLMConfig(
    prompt_template=civil_defense_prompt,
    # structured_output=CivilDefenseOutput,
)

public_works_engine = AugLLMConfig(
    prompt_template=public_works_prompt,
    # structured_output=PublicWorksOutput,
)

social_media_monitoring_engine = ReactAgentConfig(
    prompt_template=social_media_monitoring_prompt,
    tools=[tavily_search_tool],
    # structured_output=SocialMediaMonitoringOutput,
)
