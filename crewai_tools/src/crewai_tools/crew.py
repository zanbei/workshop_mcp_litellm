from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from mcp_research.tools import get_simple_tools

# Get our simple demo tools.
simple_tools = get_simple_tools()

@CrewBase
class SimpleCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['assistant'],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True,
            tools=simple_tools  # Writer gets access to our simple MCP tool.
        )

    @task
    def greeting_task(self) -> Task:
        return Task(
            config=self.tasks_config['greeting_task']
        )

    @task
    def story_task(self) -> Task:
        return Task(
            config=self.tasks_config['story_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
