import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

# Load .env that sits next to this file
load_dotenv()

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    #create first assistant agent
    agent1 = AssistantAgent(
        name="MathTeacher", 
        model_client=openai_model_client, 
        system_message="You are a math teacher. Explain concepts clearly and ask followup questions."
    )

    #create second assistant agent
    agent2 = AssistantAgent(
        name="Student", 
        model_client=openai_model_client, 
        system_message="You are a curious student. Ask questions and show your thinking process."
    )
    
    # create a round-robin group chat team
    team = RoundRobinGroupChat(
        # participants=[agent1, agent2], 
        participants=[agent2, agent1], 
        termination_condition=MaxMessageTermination(max_messages=4)
    )
    
    await Console(team.run_stream(task="Lets discuss what is multiplication and how it works"))

    await openai_model_client.close()
    await agent1.close()
    await agent2.close()

if __name__ == "__main__":
    asyncio.run(main())