import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.schema import AIMessage
from langchain_aws import ChatBedrockConverse
import boto3

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

llm = ChatBedrockConverse(
    client=bedrock_client,
    model_id="us.amazon.nova-lite-v1:0",
)

async def main():
    city = "Beijing"  # specify city here

    async with MultiServerMCPClient(
        {
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(
            llm,
            client.get_tools()
        )
        try:
            # Step 1: Ask about weather in the city
            weather_prompt = {"messages": [{"role": "user", "content": f"what is the weather in {city}?"}]}
            weather_response = await agent.ainvoke(weather_prompt)

            # Extract weather answer text from AIMessage
            weather_text = ""
            for message in reversed(weather_response['messages']):
                if isinstance(message, AIMessage) and message.content:
                    weather_text = message.content
                    break
            print("Weather response:", weather_text)

            # Step 2: Ask for fashion advice based on city and weather
            fashion_prompt_text = (
                f"Given the city name {city}, weather: {weather_text}, and temperature information, "
                "what is your fashion advice?"
            )
            fashion_prompt = {"messages": [{"role": "user", "content": fashion_prompt_text}]}
            fashion_response = await agent.ainvoke(fashion_prompt)

            # Extract fashion advice
            fashion_advice = ""
            for message in reversed(fashion_response['messages']):
                if isinstance(message, AIMessage) and message.content:
                    fashion_advice = message.content
                    break
            print("Fashion advice:", fashion_advice)

        except Exception as e:
            print(f"Error during conversation: {e}")

if __name__ == "__main__":
    asyncio.run(main())
