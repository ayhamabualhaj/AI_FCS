from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from core.tools.main_llm import main_llm
from core.tools.image_tool import GenerateImageTool

@CrewBase
class ImageGenerationCrew:
    """Image Generation Crew for AI-FCS"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def art_director(self) -> Agent:
        return Agent(
            config=self.agents_config['art_director'],
            llm=main_llm,  # Reusing the shared LLM for the agent's "thinking"
            tools=[GenerateImageTool()], # Equipping the agent with your custom tool
            verbose=True
        )

    @task
    def generate_image_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_image_task'],
            agent=self.art_director()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )