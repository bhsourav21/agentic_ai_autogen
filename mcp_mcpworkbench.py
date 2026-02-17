import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from autogen_agentchat.ui import Console

# Load .env that sits next to this file
load_dotenv()

async def main():
    filesystem_server_params = StdioServerParams(
        command="npx",
        args= [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/Users/souravbhattacharya/Documents/learning/agentic_ai"],
            read_timeout_seconds=60
    )

    fs_workbench = McpWorkbench(filesystem_server_params)

    async with fs_workbench as fs_wb:
        openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

        #create first assistant agent
        agent_teacher = AssistantAgent(
            name="MathTeacher", 
            workbench=fs_wb,
            model_client=openai_model_client, 
            system_message="You are a helpful math teacher. Help the user solve match problems step by step. \
            You have access to file system. Feel free to create files to help students refer later. \
            When the user says 'THANKS DONE' or similar, acknowledge and say 'LESSON COMPLETE' and end the session."
        )

        user_proxy = UserProxyAgent(
            name="Student"
        )
    
        # create a round-robin group chat team
        team = RoundRobinGroupChat(
            participants=[agent_teacher, user_proxy], 
            termination_condition=TextMentionTermination("LESSON COMPLETE")
        )
    
        await Console(team.run_stream(task="I need help with Algebra problems. Feel free to create files to help with student learning"))

        await openai_model_client.close()
        await agent_teacher.close()
        await user_proxy.close()

if __name__ == "__main__":
    asyncio.run(main())