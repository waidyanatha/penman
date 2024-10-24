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
#     output_file= "mining/data/article/author/article.txt"
    input_file = "wrangler/data/topic/scrape/topic_research.txt"

    def __init__(self) -> None:

        self.groq_llm = ChatGroq(temperature=0, model_name="groq/mixtral-8x7b-32768")

    @agent
    def article_author(self) -> Agent:
        return Agent(
            config = self.agents_config['article_author'],
            llm = self.groq_llm
        )

    @task
    def author_article_task(self) -> Task:
        return Task(
            config = self.tasks_config['author_article_task'],
#             output_file=self.output_file,
            input_file =self.input_file,
            agent = self.article_author()
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents= self.agents,
            tasks = self.tasks,
            process=Process.sequential,
            full_output = True,
            verbose = False
        )