import asyncio
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.schema import AIMessage
from langchain_aws import ChatBedrockConverse
import boto3
import aioconsole

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

llm = ChatBedrockConverse(
    client=bedrock_client,
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0", #  anthropic.claude-3-5-sonnet-20241022-v2:0
) # us.amazon.nova-lite-v1:0

async def select_city():
    cities = ["Copenhagen", "Beijing", "Berlin", "Paris", "Phuket", "Shanghai"]
    print("\n🌍 请从列表中选择一个城市：")
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city}")
    while True:
        choice = await aioconsole.ainput("请输入你的选择编号（默认1）：") or "1"
        try:
            index = int(choice) - 1
            if 0 <= index < len(cities):
                return cities[index]
            else:
                print("无效的数字，请重试。")
        except ValueError:
            print("无效的输入，请输入一个数字。")

async def get_time():
    print("\n⏰ 你想获取哪个时间段的建议？")
    print("1. 上午 (6:00-12:00)")
    print("2. 下午 (12:00-18:00)")
    print("3. 晚上 (18:00-24:00)")
    print("4. 凌晨 (0:00-6:00)")
    while True:
        choice = await aioconsole.ainput("请输入你的选择编号（默认1）：") or "1"
        time_periods = {
            "1": "上午",
            "2": "下午",
            "3": "晚上",
            "4": "凌晨"
        }
        if choice in time_periods:
            return time_periods[choice]
        print("无效的选择，请重试。")

async def get_user_preferences():
    print("\n👤 请告诉我们你的偏好：")
    age = await aioconsole.ainput("你的年龄是？（默认18）：") or "18"
    
    print("\n👔 你喜欢什么样的穿衣风格？")
    print("1. 休闲")
    print("2. 商务")
    print("3. 优雅")
    print("4. 运动")
    
    while True:
        style_choice = await aioconsole.ainput("请输入你的风格选择编号（默认1）：") or "1"
        style_options = {
            "1": "休闲",
            "2": "商务",
            "3": "优雅",
            "4": "运动"
        }
        if style_choice in style_options:
            return {
                "age": age,
                "style": style_options[style_choice]
            }
        print("无效的选择，请重试。")

async def create_agent(client, tool_name: str):
    """Create an agent that uses a specific tool from the weather_fashion server"""
    tools = await client.get_tools(server_name="weather_fashion")
    return create_react_agent(llm, [tool for tool in tools if tool.name == tool_name])

async def get_weather(agent, city):
    weather_prompt = {"messages": [{"role": "user", "content": f"Use the get_weather tool to get weather information for {city}"}]}
    weather_response = await agent.ainvoke(weather_prompt)

    for message in reversed(weather_response['messages']):
        if isinstance(message, AIMessage) and message.content:
            try:
                return json.loads(message.content)
            except json.JSONDecodeError:
                return message.content
    return None

async def format_fashion_advice(advice):
    if isinstance(advice, str):
        # If it's already a string, just return it with proper line breaks
        return advice.replace('\\n', '\n')
    elif isinstance(advice, dict):
        # Format dictionary content with proper indentation and line breaks
        formatted = []
        for key, value in advice.items():
            if isinstance(value, dict):
                formatted.append(f"\n{key}:")
                for sub_key, sub_value in value.items():
                    formatted.append(f"  • {sub_key}: {sub_value}")
            else:
                formatted.append(f"{key}: {value}")
        return '\n'.join(formatted)
    return str(advice)

async def get_fashion_advice(agent, city, weather_data, user_prefs, time_period):
    if isinstance(weather_data, dict):
        temperature = weather_data.get('temperature', 'unknown')
        description = weather_data.get('description', 'unknown')
    else:
        temperature = 'unknown'
        description = weather_data
    messages = [{
            "role": "user", 
            "content": json.dumps({
                "location": city,
                "temperature": "18",
                "time_period": time_period,
                "age": user_prefs["age"],
                "style": user_prefs["style"]
            })
        }]

    # print(f"messages: {messages}")
    # 构造工具调用参数
    fashion_prompt = {
        "messages": messages
    }
    try:
        fashion_response = await agent.ainvoke(fashion_prompt)
    except Exception as e:
        print(f"❌ 对话过程中出现错误：{e}")
        return None
    # print(f"fashion_response: {fashion_response}")

    for message in reversed(fashion_response['messages']):
        if isinstance(message, AIMessage) and message.content:
            try:
                return json.loads(message.content)
            except json.JSONDecodeError:
                return message.content
    return None

async def main():
    print("👋 欢迎使用天气与穿搭助手！")
    
    # Step 1: Select city
    city = await select_city()
    print(f"\n✨ 已选择城市：{city}")

    # Step 2: Select time period
    time_period = await get_time()
    print(f"✨ 已选择时间：{time_period}")

    client = MultiServerMCPClient(
        {
            "weather_fashion": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    )

    try:
        # Create agents for weather and fashion
        weather_agent = await create_agent(client, "get_weather")
        fashion_agent = await create_agent(client, "get_fashion")

        # Step 3: Get weather information
        print("\n🌤️ 正在获取天气信息...")
        weather_data = await get_weather(weather_agent, city)
        print("\n天气信息：", json.dumps(weather_data, ensure_ascii=False, indent=2))

        # Step 4: Get user preferences
        user_prefs = await get_user_preferences()
        print(f"\n✨ 个人信息：{user_prefs['age']}岁，{user_prefs['style']}风格")

        # Step 5: Get personalized fashion advice
        print("\n👔 正在获取个性化穿搭建议...")
        fashion_advice = await get_fashion_advice(fashion_agent, city, weather_data, user_prefs, time_period)
        formatted_advice = await format_fashion_advice(fashion_advice)
        print("\n穿搭建议：\n", formatted_advice)

    except Exception as e:
        print(f"❌ 对话过程中出现错误：{e}")

if __name__ == "__main__":
    asyncio.run(main())
