#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from crewai import Crew, Agent, Task, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq

print("import complete")

@CrewBase
class aiWorkLoads():
    agents_config= "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:

        self.groq_llm = ChatGroq(temperature=0, model_name="groq/mixtral-8x7b-32768")

    @agent
    def topics_researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['topics_researcher'],
            llm = self.groq_llm
        )

    @task
    def content_research_task(self) -> Task:
        return Task(
            config = self.tasks_config['research_content_task'],
            agent = self.topics_researcher()
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents= self.agents,
            tasks = self.tasks,
            process=Process.sequential,
            full_output = True,
            verbose = True
        )