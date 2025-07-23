from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field

# https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/Weather_Disaster_Management_AI_AGENT.ipynb


class WeatherLocation(BaseModel):
    """The location to get weather data fo."""

    city: str = Field(..., descriptio="The city to get weather data for")
    country: str = Field(..., descriptio="The country to get weather data for")

    def __str__(self):
        return "{self.city}, {self.country}"


class WeatherState(WeatherLocation, BaseModel):
    weather_data: dict = Field(descriptio="The weather data for the city")
    disaster_type: str = Field(descriptio="The type of disaster to manage")
    severity: str = Field(descriptio="The severity of the disaster")
    response: str = Field(descriptio="The response to the disaster")
    messages: list[SystemMessage | HumanMessage | AIMessage] = Field(
        descriptio="The messages to send to the user"
    )
    alerts: list[str] = Field(descriptio="The alerts to send to the user")
    human_approved: bool = Field(
        descriptio="Whether the user has approved the response"
    )
