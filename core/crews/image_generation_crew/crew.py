from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from core.tools.main_llm import main_llm

@CrewBase
class ImageGenerationCrew:
    """Image Generation Crew — only refines prompts"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def art_director(self) -> Agent:
        return Agent(
            config=self.agents_config['art_director'],
            llm=main_llm,
            verbose=True,
            allow_delegation=False,
        )

    @task
    def generate_image_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_image_task'],
            agent=self.art_director(),
            output_json=True,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )