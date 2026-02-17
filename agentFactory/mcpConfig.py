from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams

class McpConfig:
    def __init__(self):
        pass

    def get_mysql_workbench(self):
        mysql_server_params = StdioServerParams(
            command="uv",
            args=[
                "--directory", 
                "path/to/mysql_mcp_server",
                "run",
                "mysql_mcp_server"
            ],
            env={
                "MYSQL_HOST": "localhost",
                "MYSQL_PORT": "3306",
                "MYSQL_USER": "your_username",
                "MYSQL_PASSWORD": "your_password",
                "MYSQL_DATABASE": "your_database"
                }
        )
        return McpWorkbench(server_params=mysql_server_params)

    def get_rest_api_workbench(self):
        rest_api_server_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "dkmaker-mcp-rest-api"
            ],
            env={
                "REST_BASE_URL": "https://rahulshettyacademy.com",
                "HEADER_Accept": "application/json"
            }
        )
        return McpWorkbench(server_params=rest_api_server_params)

    def get_excel_workbench(self):
        excel_server_params = StdioServerParams (
            command="npx",
            args=["--yes", "@negokaz/excel-mcp-server"],
            env={
                "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
            },
            read_timeout_seconds=60
        )
        return McpWorkbench(server_params=excel_server_params)
    

    def get_filesystem_workbench(self):
        filesystem_server_params = StdioServerParams(
            command="npx",
            args= [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "/Users/souravbhattacharya/Documents/learning/agentic_ai"],
                read_timeout_seconds=60
        )
        return McpWorkbench(server_params=filesystem_server_params)

