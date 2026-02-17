from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agentFactory import AgentFactory
from autogen_agentchat.ui import Console
import asyncio


async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    factory = AgentFactory(openai_model_client)
    db_agent = factory.create_database_agent("You are a database specialist")
    rest_api_agent = factory.create_rest_api_agent("You are a rest api specialist")
    excel_agent = factory.create_excel_agent("You are an excel system specialist")
    filesystem_agent = factory.create_filesystem_agent("You are a file system specialist")

    team = RoundRobinGroupChat(
        participants=[db_agent, rest_api_agent, excel_agent],
        termination_condition=TextMentionTermination("REGISTRATION PROCESS COMPLETE")
    )

    test_result = await Console(team.run_stream(task=""))


if __name__ == "__main__":
    asyncio.run(main())
