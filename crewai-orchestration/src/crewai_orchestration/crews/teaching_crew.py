from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
import yaml

@CrewBase
class TeachingCrew:

    agent_config = "src/crewai_orchestration/crews/config/agents.yaml"
    task_config  = "src/crewai_orchestration/crews/config/tasks.yaml"


    with open(agent_config, "r") as f:
        agent_config = yaml.safe_load(f)
    
    with open(task_config, "r") as f:
        task_config = yaml.safe_load(f)
    


    @agent
    def teacher(self) -> Agent:
        return Agent(
            config = self.agent_config["teacher"]
        )
    
    @task
    def description_topic(self) -> Task:
        return Task(
            config = self.task_config["describe_topic"]
        )
    
    @crew
    def crew(self)-> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )