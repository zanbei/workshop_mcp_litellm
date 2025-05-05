from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools import get_tools

tools = get_tools()
@CrewBase
class SimpleCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    llm = LLM(model="us.amazon.nova-lite-v1:0")


    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['assistant'],
            llm=self.llm,
            verbose=True,
            tools=tools
        )

    @agent
    def advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['advisor'],
            llm=self.llm,
            verbose=True,
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
            verbose=True
        )
