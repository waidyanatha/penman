#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import yaml
from crewai.project import agent
from crewai import Agent
# from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool

class ScraperAgents():

    def __init__(self, llm) -> None:

        self.llm = llm
#         self.search_tool = DuckDuckGoSearchRun()

        conf_file_path = "/home/nuwan/workspace/penman/wrangler/modules/topic/scrape/config/agents.yaml"
        with open(conf_file_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)

        ''' TOOLS '''
        from wrangler.modules.topic.scrape import search_tool as tools
        tools = tools.SearchWorkLoads()
        self.search_tool = tools.duckduckgo()


    @agent
    def article_planner(self) -> Agent:
        return Agent(
            config = self.agents_config['article_planner'],
            llm = self.llm,
            allow_delegation=True,
            cache=True,
        )

    @agent
    def topics_researcher(self) -> Agent:

        return Agent(
            config = self.agents_config['topics_researcher'],
            llm = self.llm,
            allow_delegation=False,
            tools=[self.search_tool], # tools=[self.search_tool],
            cache=True,
        )