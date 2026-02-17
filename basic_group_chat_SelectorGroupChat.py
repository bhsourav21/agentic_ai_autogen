import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console

# Load .env that sits next to this file
load_dotenv()

async def main():
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    #create first assistant agent
    researcher = AssistantAgent(
        name="ResearchAgent", 
        model_client=openai_model_client, 
        system_message="You are a researcher. Your role is to gather information and provide research findings oNLY. \
        Do not write articles or create content - just provide research data and facts."
    )

    #create second assistant agent
    writer = AssistantAgent(
        name="WriterAgent", 
        model_client=openai_model_client, 
        system_message="You are a writer. Your role is to take research information and create well-written document. \
            Wait for research to be provided, then write the content"
    )
    
    #create third assistant agent
    critic = AssistantAgent(
        name="CriticAgent", 
        model_client=openai_model_client, 
        system_message="You are a critic. Review written content and provide feedback. \
        Say 'TERMINATE' when satisfied with the final result."
    )

    text_termination = TextMentionTermination("TERMINATE")
    max_msg_termination = MaxMessageTermination(max_messages=8)
    termination = text_termination | max_msg_termination

    # create a round-robin group chat team
    team = SelectorGroupChat(
        participants=[critic, writer, researcher], 
        model_client=openai_model_client, # needed because the class SelectorGroupChat decides which agent to run when, so it needs the brain/intelligence. This is costlier than round robin as there the sequence is predefined, so LLM intelligent is not needed.
        allow_repeated_speaker=True,
        termination_condition=termination
    )
    
    await Console(team.run_stream(task="Research on renewable enrgy trends and write a brief article abbout the future of solar power.")) 

    await openai_model_client.close()
    await researcher.close()
    await writer.close()
    await critic.close()

if __name__ == "__main__":
    asyncio.run(main())