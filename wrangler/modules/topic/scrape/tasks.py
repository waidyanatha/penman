#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import yaml
from crewai.project import task
from crewai import Task

class ScraperTask():

    def __init__(self) -> None:
        
        conf_file_path = "/home/nuwan/workspace/penman/wrangler/modules/topic/scrape/config/tasks.yaml"
        with open(conf_file_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

#     @task
#     def plan_outline_task(self,agent,context) -> Task:

#         return Task(
#             config = self.tasks_config['plan_outline_task'],
#             agent = agent, #self.article_planner(),
#             async_execution=False,  # at least one must be false
#             context=context
#         )
    @task
    def plan_outline_task(self,agent) -> Task:

        ''' TODO output_json=outlineJSONObj, '''
        return Task(
            config = self.tasks_config['plan_outline_task'],
            agent = agent, #self.article_planner(),
            async_execution=False,  # at least one must be false
        )

    @task
    def research_content_task(self,agent) -> Task:
        return Task(
            config = self.tasks_config['research_content_task'],
            agent = agent, #self.topics_researcher(),
            async_execution=True,
            allow_delegation=True,
        )

