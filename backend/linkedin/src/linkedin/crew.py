import os
from typing import List
from dotenv import load_dotenv
from datetime import datetime 
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from langchain_ollama import OllamaLLM    

load_dotenv()

llm = OllamaLLM(model=os.getenv("OLLAMA_MODEL", "mistral:latest"))

@CrewBase
class LinkedInPoster:

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trend_agent(self) -> Agent:
        return Agent(config=self.agents_config['trend_agent'], llm=llm)

    @agent
    def search_agent(self) -> Agent:
        return Agent(config=self.agents_config['search_agent'], llm=llm)

    @agent
    def planner_agent(self) -> Agent:
        return Agent(config=self.agents_config['planner_agent'], llm=llm)

    @agent
    def writer_agent(self) -> Agent:
        return Agent(config=self.agents_config['writer_agent'], llm=llm)

    @agent
    def seo_agent(self) -> Agent:
        return Agent(config=self.agents_config['seo_agent'], llm=llm)

    @agent
    def reviewer_agent(self) -> Agent:
        return Agent(config=self.agents_config['reviewer_agent'], llm=llm)

    @agent
    def exporter_agent(self) -> Agent:
        return Agent(config=self.agents_config['exporter_agent'], llm=llm)

    @agent
    def publisher_agent(self) -> Agent:
        return Agent(config=self.agents_config['publisher_agent'], llm=llm)

    @task
    def trend_task(self) -> Task:
        return Task(config=self.tasks_config['trend_task'])

    @task
    def search_task(self) -> Task:
        return Task(config=self.tasks_config['search_task'])

    @task
    def plan_task(self) -> Task:
        return Task(config=self.tasks_config['plan_task'])

    @task
    def write_task(self) -> Task:
        return Task(config=self.tasks_config['write_task'])

    @task
    def seo_task(self) -> Task:
        return Task(config=self.tasks_config['seo_task'])

    @task
    def review_task(self) -> Task:
        return Task(config=self.tasks_config['review_task'])

    @task
    def export_task(self) -> Task:
        tpl = self.tasks_config['export_task']['output_file']
        filename = tpl.format(timestamp=datetime.now().strftime("%Y%m%dT%H%M%S"))
        return Task(
            config=self.tasks_config['export_task'],
            output_file=filename
        )

    @task
    def publish_task(self) -> Task:
        return Task(config=self.tasks_config['publish_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
