import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console


# Load .env that sits next to this file
load_dotenv()

async def main():
    print("hello world")

    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )

    assistant = AssistantAgent(name="assistant", model_client=openai_model_client)
    await Console(assistant.run_stream(task="What is 25 * 8"))

    await openai_model_client.close()
    await assistant.close()

if __name__ == "__main__":
    asyncio.run(main())