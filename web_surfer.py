import asyncio
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.ui import Console

# Load .env that sits next to this file
load_dotenv()

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    web_surfer = MultimodalWebSurfer(
        name="WebSurfer",
        model_client=openai_model_client,
        headless=False,
        animate_actions=True
    )

    team = RoundRobinGroupChat(
        participants=[web_surfer], 
        max_turns=3
    )

    await Console(team.run_stream(task="Navigate to google and search for Autogen framework python. Then summarize it and share what you find"))

    await openai_model_client.close()
    await web_surfer.close()

if __name__ == "__main__":
    asyncio.run(main())