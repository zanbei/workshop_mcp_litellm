from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from mcpwhs.tools.mcp_tools import get_mcprun_tools
import os
import logging

logger = logging.getLogger(__name__)
logger.info("Logging is configured and working.")

if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

@CrewBase
class MCPCrew():
    def __init__(self, session_id=None):
        self.session_id = session_id or os.getenv("MCPX_SESSION_ID")
        if not self.session_id:
            raise ValueError("Please provide a session_id parameter or set MCPX_SESSION_ID in your environment variables.")
        self.mcpx_tools = get_mcprun_tools(session_id=self.session_id)
        logger.info(f"Initializing mcpx_tools: {self.mcpx_tools}")
        print(f"Loaded {self.mcpx_tools} tools from mcp.run")


        self.llm = LLM(model="us.amazon.nova-lite-v1:0")

    # Paths to your YAML configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['assistant'],
            llm=self.llm,
            verbose=True,
            tools=self.mcpx_tools
        )

    @agent
    def advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['advisor'],
            llm=self.llm,
            verbose=True,
            tools=self.mcpx_tools
        )

    @task
    def fashion_task(self) -> Task:
        return Task(
            config=self.tasks_config['fashion_task']
        )

    @task
    def weather_task(self) -> Task:
        return Task(
            config=self.tasks_config['weather_task']
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_log_file="crew_execution.log"
        )