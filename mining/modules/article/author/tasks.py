#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import yaml
from crewai.project import task
from crewai import Task

class taskWorkLoads():

    def __init__(self) -> None:
        
        conf_file_path = "/home/nuwan/workspace/penman/mining/modules/article/author/config/tasks.yaml"
        with open(conf_file_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

        # from mining.modules.article.author import search_tools

    @task
    def load_outline_task(self,agent, **kwargs) -> Task:

        ''' TODO output_json=outlineJSONObj, '''
        return Task(
            config = self.tasks_config['load_outline_task'],
            agent = agent, #self.article_planner(),
            # tool_input=kwargs['tool_input'],
            async_execution=False,  # at least one must be false
            verbose=True,
            # tools=['retrieve_outline']
        )

    # @task
    # def load_research_task(self,agent) -> Task:
    #     return Task(
    #         config = self.tasks_config['load_research_task'],
    #         agent = agent, #self.topics_researcher(),
    #         async_execution =True,
    #         allow_delegation=True,
    #         # tools=['retrieve_research']
    #     )

    # @task
    # def author_article_task(self,agent) -> Task:
    #     return Task(
    #         config = self.tasks_config['author_article_task'],
    #         agent = agent, #self.topics_researcher(),
    #         async_execution =True,
    #         allow_delegation=True,
    #         # tools=['search_research']
    #     )

    # @task
    # def publish_draft_task(self,agent) -> Task:

    #     ''' TODO output_json=outlineJSONObj, '''
    #     return Task(
    #         config = self.tasks_config['publish_draft_task'],
    #         agent = agent, #self.article_planner(),
    #         async_execution=False,  # at least one must be false
    #     )
