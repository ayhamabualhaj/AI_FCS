from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from core.tools.main_llm import main_llm

@CrewBase
class PostWriterCrew:

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def facebook_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['facebook_copywriter'],
            llm=main_llm,
            verbose=True
        )

    @task
    def write_post_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_post_task'],
            agent=self.facebook_copywriter() # Assign the task to the agent
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )