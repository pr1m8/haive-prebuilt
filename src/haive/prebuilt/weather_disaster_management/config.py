
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, ConfigDict, Field

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm.base import AugLLMConfig
from haive.core.graph.branches import Branch
from haive.prebuilt.misc.weather_disaster_management.branches import route_branch
from haive.prebuilt.misc.weather_disaster_management.engines import (
    civil_defense_engine,
    disaster_engine,
    public_works_engine,
    response_engine,
    severity_engine,
    social_media_monitoring_engine,
)
from haive.prebuilt.misc.weather_disaster_management.state import WeatherLocation, WeatherState
from src.haive.toolkits.weather import weather_tool


class WeatherDisasterManagerConfig(AgentConfig):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # ✅ Add this

    engines: dict[str, AugLLMConfig | AgentConfig] = Field(default={
        "analyze_disaster_type": disaster_engine,
        "severity_engine": severity_engine,
        "response_engine": response_engine,
        "civil_defense_engine": civil_defense_engine,
        "public_works_engine": public_works_engine,
        "social_media_monitoring": social_media_monitoring_engine,
    })

    branches: dict[str, Branch] = Field(default={
        "route_branch": route_branch,
    })

    tools: dict[str, StructuredTool] = Field(default={
        "weather_tool": weather_tool,
    })

    state_schema: BaseModel = WeatherState
    input_schema: BaseModel = WeatherLocation
