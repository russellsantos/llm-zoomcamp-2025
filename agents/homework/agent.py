import random
from openai import OpenAI
import os
from chat_assistant import ChatAssistant, ChatInterface, Tools

known_weather_data = {
    'berlin': 20.0
}

def get_weather(city: str) -> float:
    city = city.strip().lower()

    if city in known_weather_data:
        return known_weather_data[city]

    return round(random.uniform(-5, 35), 1)

def set_weather(city: str, temp: float) -> None:
    city = city.strip().lower()
    known_weather_data[city] = temp
    return 'OK'

get_weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "A function that returns the weather given a city name.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city that we want to get weather for."
            }
        },
        "required": ["city"],
        "additionalProperties": False,
    },
}

set_weather_tool = {
    "type": "function",
    "name": "set_weather",
    "description": "A function that sets the weather for a given city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city that we want to set the weather for."
            },
            "temp": {
                "type": "number",
                "description": "The temperature to set for the city."
            }
        },
        "required": ["city", "temp"],
        "additionalProperties": False,
    },
}


def create_openai_client(api_key: str = None) -> OpenAI:
    if not api_key: 
        api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    return client

class WeatherAgent():
    DEVELOPER_PROMPT = """
    You are a helpful assistant that provides weather data. Use the appropriate tools when the user asks a question about the weather. 
    If they ask for the weather for a country instead of a city, retrieve the weather for the capital city of that country. Then tell them the weather for that city.
    Then provide the weather for the capital city of that country.
    If the location they provide is neither a city nor a country, inform them that you can only provide weather data for cities.
    """.strip()


    @staticmethod
    def create_tools() -> Tools:
        tools = Tools()
        tools.add_tool(get_weather, get_weather_tool)
        tools.add_tool(set_weather, set_weather_tool)
        return tools


    def __init__(self, client: OpenAI):
        tools = self.create_tools()
        chat_interface = ChatInterface()
        self.chat = ChatAssistant(
            tools=tools,
            developer_prompt=self.DEVELOPER_PROMPT,
            chat_interface=chat_interface,
            client=client
        )

    def run(self):
        self.chat.run()
    


def main():
    chat = WeatherAgent(create_openai_client())
    chat.run()

if __name__ == "__main__":
    main()