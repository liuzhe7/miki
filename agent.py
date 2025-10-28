import model, memory, output_structure, tools
from langchain.agents import create_agent

SYSTEM_PROMPT = """
You are a helpful AI assistant that can answer questions and help users with various tasks.

You have access to the following tools:
- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

Please provide clear, helpful responses to user questions.
"""

agent = create_agent(
    model=model.model,
    system_prompt=SYSTEM_PROMPT,
    tools=[tools.get_user_location, tools.get_weather_for_location],
    context_schema=tools.Context,
    response_format=output_structure.ResponseFormat,
    checkpointer=memory.checkpointer,
)
