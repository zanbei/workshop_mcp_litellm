import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
# from langchain_deepseek import ChatDeepSeek
from langchain.schema import AIMessage
from langchain_aws import ChatBedrockConverse
import boto3

bedrock_client = boto3.client(service_name="bedrock-runtime",region_name="us-west-2")

# Initialize Bedrock LLM with Nova model
llm = ChatBedrockConverse(
    client=bedrock_client,
    model_id="us.amazon.nova-lite-v1:0",
)

async def main():
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
            weather_response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": "what is the weather in beijing?"}]}
            )
            final_answer = ""
            # 反向遍历消息列表，因为最终回答通常在末尾
            for message in reversed(weather_response['messages']):
                if isinstance(message, AIMessage) and message.content:
                    final_answer = message.content
                    break
            print("Weather response:", final_answer)
        except Exception as e:
            print(f"Error getting weather response: {e}")

if __name__ == "__main__":
    asyncio.run(main())
