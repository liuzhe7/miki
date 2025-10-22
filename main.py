from langchain_core.runnables.config import RunnableConfig

import tools

from agent import agent


def main():
    # `thread_id` is a unique identifier for a given conversation.
    config: RunnableConfig = {"configurable": {"thread_id": "1"}}

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
        config=config,
        context=tools.Context(user_id="1"),
    )

    print(response["structured_response"])
    # ResponseFormat(
    #     punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",
    #     weather_conditions="It's always sunny in Florida!"
    # )


if __name__ == "__main__":
    main()
