from autogen_agentchat.agents import AssistantAgent
from mcpConfig import McpConfig
import asyncio


class AgentFactory:

    def __init__(self, openai_model_client) -> None:
        self.openai_model_client = openai_model_client
        self.mcp_config = McpConfig()
        
    # Generic database agent
    def create_database_agent(self, system_message):
        db_agent = AssistantAgent(
            name="DatabaseAgent", 
            workbench=self.mcp_config.get_mysql_workbench(),
            model_client=self.openai_model_client,
            system_message=system_message
            )
        return db_agent

    # check how two tools are passed to an agent
    def create_rest_api_agent(self, system_message):
        rest_api_agent = AssistantAgent(
            name="RestApiAgent", 
            workbench=[
                self.mcp_config.get_rest_api_workbench(),
                self.mcp_config.get_filesystem_workbench()
            ]
            model_client=self.openai_model_client,
            system_message=system_message
            )
        return rest_api_agent
    
    def create_excel_agent(self, system_message):
        excel_agent = AssistantAgent(
            name="ExcelAgent", 
            workbench=self.mcp_config.get_excel_workbench(),
            model_client=self.openai_model_client,
            system_message=system_message
            )
    
    def ceate_filesystem_agent(self, system_message):
        filesystem_agent = AssistantAgent(
            name="FileSytemAgent", 
            workbench=self.mcp_config.get_filesystem_workbench(),
            model_client=self.openai_model_client,
            system_message=system_message
            )

    