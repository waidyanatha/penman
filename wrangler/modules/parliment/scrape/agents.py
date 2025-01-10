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

        conf_file_path = "/home/nuwan/workspace/penman/wrangler/modules/parliment/scrape/config/agents.yaml"
        with open(conf_file_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)

        ''' TOOLS '''
        from wrangler.modules.parliment.scrape import search_tool as tools
        tools = tools.SearchWorkLoads()
        self.search_tool = tools.duckduckgo()

    @agent
    def referrence_planner(self) -> Agent:
        return Agent(
            config = self.agents_config['referrence_planner'],
            llm = self.llm,
            allow_delegation=False,
            cache=True,
        )

    @agent
    def content_planner(self) -> Agent:

        return Agent(
            config = self.agents_config['content_planner'],
            llm = self.llm,
            allow_delegation=True,
            tools=[self.search_tool], # tools=[self.search_tool],
            cache=True,
        )