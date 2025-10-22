import model, memory, output_structure, tools
from langchain.agents import create_agent

SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""

agent = create_agent(
    model=model.model,
    system_prompt=SYSTEM_PROMPT,
    tools=[tools.get_user_location, tools.get_weather_for_location],
    context_schema=tools.Context,
    response_format=output_structure.ResponseFormat,
    checkpointer=memory.checkpointer,
)
