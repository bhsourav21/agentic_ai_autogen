import json
import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

# Load .env that sits next to this file
load_dotenv()

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    #create first assistant agent
    agent1 = AssistantAgent(
        name="Helper", 
        model_client=openai_model_client
    )

    agent2 = AssistantAgent(
        name="BackupHelper", 
        model_client=openai_model_client
    )
    
    await Console(agent1.run_stream(task="My favourite color is blue"))
    state = await agent1.save_state()

    with open("memory.json", "w") as f:
        json.dump(state, f, default=str)

    with open("memory.json", "r") as f:
        saved_state = json.load(f)

    await agent2.load_state(saved_state)

    await Console(agent2.run_stream(task="What is my favourite color?"))

    await openai_model_client.close()
    await agent1.close()
    await agent2.close()

if __name__ == "__main__":
    asyncio.run(main())