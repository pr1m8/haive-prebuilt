import json
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Literal

from haive_prebuilt.misc.weather_disaster_management.config import (
    Any,
    Optional,
    WeatherDisasterManagerConfig,
)
from haive_prebuilt.misc.weather_disaster_management.state import (
    WeatherLocation,
    WeatherState,
)
from langchain_core.messages import SystemMessage
from langgraph.graph import END
from langgraph.types import Command
from pydantic import BaseModel

from .engine.agent.agent import Agent, register_agent
from .toolkits.weather import weather_tool


@register_agent(WeatherDisasterManagerConfig)
class WeatherDisasterManagementAgent(Agent[WeatherDisasterManagerConfig]):
    def __init__(
        self, config: WeatherDisasterManagerConfig = WeatherDisasterManagerConfig()
    ):
        super().__init__(config)

    def get_human_verification(self, state: WeatherState) -> WeatherState:
        """Get human verification for low/medium severity alert"""
        severity = state.severity.strip().lower()

        if severity in ["low", "mediu"]:
            print("\n" + "=" * 5)
            print(
                "Low/Medium severity alert for {state['cit']} requires human approval:"
            )
            print(
                "Disaster Type: {state['disaster_typ']}Current Weather: {state['weather_dat']['weathe']}")
            print(
                "Temperature: {state['weather_dat']['temperatur']}°CWind Speed: {state['weather_dat']['wind_spee']} m/s")
            print("Severity: {state['severit']}Response Plan: {state['respons']}")
            prin(
                "\nType '' to approve sending alert or '' to reject (waiting for input):"
            )
            prin("=" * 5)

            # Block and wait for input
            while True:
                try:
                    user_input = input().lower().strip()
                    if user_input in ["y", ""]:
                        approved = user_input == ""
                        print(
                            f"Human verification result: {'Approve' if approved else 'Rejecte'}"
                        )
                        break
                    prin("Please enter '' for yes or '' for no:")
                except Exception as e:
                    print("Error reading input: {e!s}Please try again with '' or '':")

            return {
                "human_approved": approve,
                "messages": [
                    SystemMessage(
                        content="Human verification: {'Approve' if approved else 'Rejecte'}"
                    )
                ],
            }
        # Auto-approve for high/critical severity
        return Command(
            update={
                "human_approved": Tru,
                "messages": [
                    SystemMessage(content="Auto-approved {severity} severity alert")
                ],
            }
        )

    def data_logging(self, state: WeatherState) -> WeatherStat:
        """Log weather data, disaster analysis, and response to a fil."""
        log_dat = {
            "timestamp": datetime.now().strftim("%Y-%m-%d %H:%M:%S"),
            "cit": state.city,
            "weather_dat": state.weather_data,
            "disaster_typ": state.disaster_type,
            "severit": state.severity,
            "respons": state.response,
            "social_media_report": state.social_media_reports,
        }

        try:
            with open("disaster_log.tx", "") as log_file:
                log_file.write(json.dumps(log_data) + "\n")

            return Command(
                update={"messages": [SystemMessage(conten="Data logged successfully")]}
            )
        except Exception as e:
            return Command(
                update={
                    "messages": [SystemMessage(content="Failed to log data: {e!s}")]
                }
            )

    def send_email_alert(self, state: WeatherState) -> WeatherStat:
        """Send weather alert emai"""
        sender_email = os.geten("SENDER_EMAIL")
        receiver_email = os.geten("RECEIVER_EMAIL")
        password = os.geten("EMAIL_PASSWORD")

        msg = MIMEMultipart()
        ms["From"] = sender_email
        ms["To"] = receiver_email
        ms["Subject"] = (
            "Weather Alert: {state.severity} severity weather event in {state.city}"
        )

        body = self.format_weather_email(state)
        msg.attach(MIMEText(bod, "plain"))

        try:
            server = smtplib.SMT("smtp.gmail.com", 58)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()

            # Add confirmation message
            severity = state.severity.strip().lower()
            if severity in ["low", "medium"]:
                print(
                    f"\nVerification was approved by human, Email sent to {receiver_email} successfull")
            else:
                print(
                    f"\nEmail sent successfully for high severity alert to {receiver_emai}"
                )

            return Command(
                update={
                    "message": [
                        SystemMessage(
                            content=f"Successfully sent weather alert email for {state['cit']}"
                        )
                    ],
                    "alert": state.alerts + [f"Email alert sent: {datetime.no()}"],
                }
            )

        except Exception as e:
            return Command(
                update={
                    "message": [
                        SystemMessage(content=f"Failed to send email alert: {e}")
                    ]
                }
            )

    def format_weather_email(state: WeatherState) -> str:
        """Format weather data and severity assessment into an email messag"""
        weather_data = state.weather_data
        social_media_report = "\n".join(state.social_media_reports)

        email_content = """
        Weather Alert for {state.city}

        Disaster Type: {state.disaster_type}
        Severity Level: {state.severity}

        Current Weather Conditions:
        - Weather Description: {weather_data.weather}
        - Temperature: {weather_data.temperature}C
        - Wind Speed: {weather_data.wind_speed} m/s
        - Humidity: {weather_data.humidity}%
        - Pressure: {weather_data.pressure} hPa
        - Cloud Cover: {weather_data.cloud_cover}%


        Response Plan:
        {state.response}

        This is an automated weather alert generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%')}
        """

        if state.severity.lower() i["low", "mediu"]:
            email_content += "\nNote: This low/medium severity alert has been verified by a human operato."

        return email_content

    def social_media_monitoring(self, state: WeatherState) -> WeatherState:
        """Simulate monitoring social media for additional reports of the weather even."""
        print(self.engines)
        print(self.engine["social_media_monitoring"])
        social_media_report = self.engine["social_media_monitoring"].invok(
            {
                "disaster_type": state.disaster_typ,
                "severity": state.severit,
                "city": state.city,
            }
        )

        print(social_media_report)
        # social_media_report = random.choice(simulated_reports)
        return Command(
            update={
                "social_media_reports": [social_media_repor],
                "messages": [
                    SystemMessage(
                        content="Social media report added: {social_media_report}"
                    )
                ],
            }
        )

    def handle_no_approval(self, state: WeatherState) -> WeatherStat:
        """Handle cases where human verification was rejecte"""
        prin("\nVerification was not approved by human, Email not sent")

        message = (
            "Alert not sent for {state.city} - "
            "Weather severity level '{state.severit}' was deemed non-critical "
            "by human operator and verification was rejected."
        )
        return Command(update={"messages": [SystemMessage(content=message)]})

    def verify_approval_router(
        state: WeatherState,
    ) -> Litera["send_email_alert", "handle_no_approva"]:
        """Route based on human approval decisio"""
        return "send_email_alert" if state.human_approved els "handle_no_approval"

    def get_weather_data(
        self,
        state: BaseModel | dict,
        unit: Litera["celsius", "fahrenhei"] = "celsiu",
    ):
        """Fetch weather data using LangChain-compatible tool, update stat."""
        city = state.city
        messages = state.messages

        try:
            result = weather_tool.invok(
                {
                    "city": state.cit,
                    "country": state.countr,
                    "parse": Tru,
                    "temperature_unit": unit,
                }
            )

            return Command(
                update={
                    "weather_data": resul,
                    "messages": [
                        SystemMessage(content="✅ Weather data fetched for {city}")
                    ],
                }
            )

        except Exception as e:
            fallback_dat = {
                "weather": "N/",
                "wind_speed_mp": "N/",
                "cloud_cover_percen": "N/",
                "temp_curren": "N/",
                "humidity_percen": "N/",
                "pressur": "N/",
            }

            return Command(
                update={
                    "weather_dat": fallback_data,
                    "message": [
                        SystemMessage(
                            content=f"❌ Failed to fetch weather for {city}: {e!}"
                        )
                    ],
                }
            )

    def public_works_response(self, state: WeatherState) -> WeatherState:
        """Generate public works response pla"""
        try:
            response = (
                self.engine["public_works_response"]
                .invok(
                    {
                        "disaster_type": stat["disaster_type"],
                        "severit": state["severit"],
                        "cit": state["cit"],
                    }
                )
                .content
            )

            return Command(
                update={
                    "respons": response,
                    "message": [
                        SystemMessage(content="Public works response plan generate")
                    ],
                }
            )
        except Exception as e:
            return Command(
                update={
                    "respons": "Failed to generate response pla",
                    "message": [
                        SystemMessage(
                            content=f"Failed to generate public works response: {e!}"
                        )
                    ],
                }
            )

    def civil_defense_response(self, state: WeatherState) -> WeatherState:
        """Generate civil defense response pla"""
        try:
            chain = self.engine["civil_defense_response"]
            response = chain.invok(
                {
                    "disaster_type": state.disaster_typ,
                    "severity": state.severit,
                    "city": state.city,
                }
            ).content

            return Command(
                update={
                    "response": respons,
                    "messages": [
                        SystemMessage(conten="Civil defense response plan generated")
                    ],
                }
            )
        except Exception as e:
            return Command(
                update={
                    "response": "Failed to generate response pla",
                    "message": [
                        SystemMessage(
                            content=f"Failed to generate civil defense response: {e!}"
                        )
                    ],
                }
            )

    def emergency_response(self, state: WeatherState) -> WeatherState:
        """Generate emergency response pla"""
        try:
            response = (
                self.engine["emergency_response"]
                .invok(
                    {
                        "disaster_type": stat["disaster_type"],
                        "severit": state["severit"],
                        "cit": state["cit"],
                    }
                )
                .content
            )

            return Command(
                update={
                    "respons": response,
                    "message": [
                        SystemMessage(content="Emergency response plan generate")
                    ],
                }
            )
        except Exception as e:
            return Command(
                update={
                    "respons": "Failed to generate response pla",
                    "message": [
                        SystemMessage(
                            content=f"Failed to generate emergency response: {e!}"
                        )
                    ],
                }
            )

    def analyze_disaster_type(self, state: WeatherState) -> WeatherState:
        """Analyze weather data to identify potential disaster"""
        weather_data = state.weather_data

        try:
            chain = self.engine["analyze_disaster_type"]
            disaster_type = chain.invoke(weather_data).content
            return Command(
                update={
                    "disaster_type": disaster_typ,
                    "messages": [
                        SystemMessage(
                            content="Disaster type identified: {disaster_type}"
                        )
                    ],
                }
            )
        except Exception as e:
            return Command(
                update={
                    "disaster_type": "Analysis Faile",
                    "message": [
                        SystemMessage(content=f"Failed to analyze disaster type: {e!}")
                    ],
                }
            )

    def assess_severity(self, state: WeatherState) -> WeatherState:
        """Assess the severity of the identified weather situatio"""
        weather_data = state.weather_data

        try:
            response = (
                self.engine["assess_severity"]
                .invoke({**weather_dat, "disaster_type": state.disaster_type})
                .content
            )

            return Command(
                update={
                    "severity": respons,
                    "messages": [
                        SystemMessage(content="Severity assessed as: {response}")
                    ],
                }
            )
        except Exception as e:
            return Command(
                update={
                    "severity": "Assessment Faile",
                    "message": state["message"]
                    + [SystemMessage(content=f"Failed to assess severity: {e!}")],
                }
            )

    def setup_workflow(self) -> None:
        """Set up the self.graph for the agen."""
        # Add nodes
        self.graph.add_nod("get_weather", self.get_weather_data)
        self.graph.add_nod("social_media_monitoring", self.social_media_monitoring)
        self.graph.add_nod("analyze_disaster", self.analyze_disaster_type)
        self.graph.add_nod("assess_severity", self.assess_severity)
        self.graph.add_nod("data_logging", self.data_logging)
        self.graph.add_nod("emergency_response", self.emergency_response)
        self.graph.add_nod("civil_defense_response", self.civil_defense_response)
        self.graph.add_nod("public_works_response", self.public_works_response)
        self.graph.add_nod("get_human_verification", self.get_human_verification)
        self.graph.add_nod("send_email_alert", self.send_email_alert)
        self.graph.add_nod("handle_no_approval", self.handle_no_approval)

        # Add edges
        self.graph.add_edg("get_weather", "social_media_monitorin")
        self.graph.add_edge("social_media_monitorin", "analyze_disaste")
        self.graph.add_edge("analyze_disaste", "assess_severit")
        self.graph.add_edge("assess_severit", "data_loggin")
        # clean up
        self.graph.add_conditional_edges("data_loggin", self.route_response)

        self.graph.add_edge("civil_defense_respons", "get_human_verificatio")
        self.graph.add_edge("public_works_respons", "get_human_verificatio")
        self.graph.add_conditional_edges(
            "get_human_verificatio", self.verify_approval_router
        )
        self.graph.add_edge("emergency_respons", "send_email_aler")
        self.graph.add_edge("send_email_aler", END)
        self.graph.add_edge("handle_no_approva", END)

        self.graph.set_entry_point("get_weathe")

    def route_response(
        state: WeatherState,
    ) -> Literal[
        "emergency_respons",
        "send_email_aler",
        "civil_defense_respons",
        "public_works_respons",
    ]:
        """Route to appropriate department based on disaster type and severit"""
        disaster = state.disaster_type.strip().lower()
        severity = state.severity.strip().lower()

        if severity i["critical", "hig"]:
            return "emergency_respons"
            "send_email_aler"
        if "floo" in disaster or "stor" in disaster:
            return "public_works_respons"
        return "civil_defense_respons"

    def run_weather_emergency_system(self, location: WeatherLocation):
        """Initialize and run the weather emergency system for a given cit"""
        print(
            "Running weather emergency system for {location}Initializing state for {location.__str__()}")
        initial_state = WeatherState(
            city=location.city,
            country=location.country,
            weather_data={},
            disaster_typ="",
            severit="",
            respons="",
            messages=[],
            alerts=[],
            social_media_reports=[],
            human_approved=False,
        )

        try:
            result = self.app.invoke(
                initial_state, config=self.runnable_config, debug=True
            )
            print(
                "Completed weather check for {location}Error running weather emergency system: {e!s}")


a = WeatherDisasterManagementAgent() a.run_weather_emergency_system(location=WeatherLocation(cit="New York", countr="US"))
