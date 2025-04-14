from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from mcpwhs.tools.mcp_tools import get_mcprun_tools
import os

class PIAIC():
    """PIAIC crew powered by Gemini API integration"""

    def __init__(self, session_id=None):
        """Initialize PIAIC with optional session_id."""
        self.session_id = session_id or os.getenv("MCPX_SESSION_ID")
        if not self.session_id:
            raise ValueError("Please provide a session_id parameter or set MCPX_SESSION_ID in your environment variables.")
        self.mcpx_tools = get_mcprun_tools(session_id=self.session_id)

    # Paths to your YAML configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def zookeeper(self) -> Agent:
        return Agent(
            config=self.agents_config['zookeeper'],
            verbose=True
        )
    
    @agent
    def social_media_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_manager'],
            verbose=True,
            tools=self.mcpx_tools  # Agent gets access to mcp.run (Gemini-powered) tools
        )

    @task
    def write_interesting_stories_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_interesting_stories_task']
        )

    @task
    def publish_blog_posts_task(self) -> Task:
        return Task(
            config=self.tasks_config['publish_blog_posts_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PIAIC crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )