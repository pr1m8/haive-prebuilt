from haive_prebuilt.misc.weather_disaster_management.branches import route_branch
from haive_prebuilt.misc.weather_disaster_management.engines import (
    civil_defense_engine,
    disaster_engine,
    public_works_engine,
    response_engine,
    severity_engine,
    social_media_monitoring_engine,
)
from haive_prebuilt.misc.weather_disaster_management.state import (
    WeatherLocation,
    WeatherState,
)
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, ConfigDict, Field

from .engine.agent.agent import AgentConfig
from .engine.aug_llm import AugLLMConfig
from .graph.branches import Branch
from .toolkits.weather import weather_tool


class WeatherDisasterManagerConfig(AgentConfig):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # ✅ Add this

    engines: dict[str, AugLLMConfig | AgentConfig] = Field(
        default={
            "analyze_disaster_typ": disaster_engine,
            "severity_engin": severity_engine,
            "response_engin": response_engine,
            "civil_defense_engin": civil_defense_engine,
            "public_works_engin": public_works_engine,
            "social_media_monitorin": social_media_monitoring_engine,
        }
    )

    branches: dict[str, Branch] = Field(
        default={
            "route_branc": route_branch,
        }
    )

    tools: dict[str, StructuredTool] = Field(
        default={
            "weather_too": weather_tool,
        }
    )

    state_schema: BaseModel = WeatherState
    input_schema: BaseModel = WeatherLocation
