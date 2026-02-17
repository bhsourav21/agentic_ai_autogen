import asyncio
from autogen_core import Image
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console


# Load .env that sits next to this file
load_dotenv()

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    image = Image.from_file("/Users/souravbhattacharya/Documents/Screenshot_2025-07-05.png")

    multimodal_message = MultiModalMessage(
        content=["What do you see in this image?", image], source="user"
    )
    
    assistant = AssistantAgent(name="multimodal_assistant", model_client=openai_model_client)

    await Console(assistant.run_stream(task=multimodal_message))

    await openai_model_client.close()
    await assistant.close()

if __name__ == "__main__":
    asyncio.run(main())