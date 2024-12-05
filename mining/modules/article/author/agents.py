#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

''' Initialize with default environment variables '''
__name__ = "agents"
__package__ = "author"
__module__ = "article"
__app__ = "mining"
__ini_fname__ = "app.ini"
__conf_fname__ = "app.cfg"

try:
    import os
    import sys
    import configparser    
    import logging
    import functools
    import traceback
    import yaml
    from crewai.project import agent
    from crewai import Agent
    # from langchain_community.tools import DuckDuckGoSearchRun
    from langchain.tools import Tool
    # from langchain.tools.file_management.utils import FileManager
    # from langchain.tools.file_management.toolkit import FileManagementToolkit

    print("All functional %s-libraries in %s-package of %s-module imported successfully!"
          % (__name__.upper(),__package__.upper(),__module__.upper()))

except Exception as e:
    print("Some packages in {0} module {1} package for {2} function didn't load\n{3}"\
          .format(__module__.upper(),__package__.upper(),__name__.upper(),e))

class agentWorkLoads():

    def __init__(self, llm) -> None:

        global clsTools

        self.llm = llm
#         self.search_tool = DuckDuckGoSearchRun()

        conf_file_path = "/home/nuwan/workspace/penman/mining/modules/article/author/config/agents.yaml"
        with open(conf_file_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)

        # ''' TOOLS '''
        # from mining.modules.article.author import writer_tools as tools
        from mining.modules.article.author import tools
        clsTools = tools.ReadFileTool()
        # clsTools = tools.toolWorkLoads()
        # file_management_toolkit = FileManagementToolkit(root_dir=db_root)

    @agent
    def outline_retriever(self) -> Agent:
        """
        fetches the outline content from the file using tools
        """
        # from mining.modules.article.author import read_file_tool as rft
        # readTool = rft.ReadFileTool()

        # print(type(clsTools.retrieve_outline), clsTools.retrieve_outline)
        # self.search_tool = tools.retrieve_outline()
        # _tools = [retrieve_outline] + file_management_toolkit.get_tools()

        return Agent(
            config = self.agents_config['outline_retriever'],
            # llm = self.llm,
            allow_delegation=False,
            tools=[clsTools.retrieve_outline()], 
            # tools=[rft.ReadFileTool()],
            cache = True,
            verbose=True,
        )

    # @agent
    # def research_retriever(self) -> Agent:

    #     # self.search_tool = tools.retrieve_research()
    #     return Agent(
    #         config = self.agents_config['research_retriever'],
    #         llm = self.llm,
    #         allow_delegation=False,
    #         # tools=[self.search_tool], # tools=[self.search_tool],
    #         cache=True,
    #         verbose=True,
    #     )

    # @agent
    # def article_author(self) -> Agent:

    #     return Agent(
    #         config = self.agents_config['article_author'],
    #         llm = self.llm,
    #         allow_delegation=True,
    #         cache=True,
    #         verbose=True,
    #     )

    # @agent
    # def draft_publisher(self) -> Agent:

    #     # self.pub_tool = tools.write_2_pdf()
    #     return Agent(
    #         config = self.agents_config['draft_publisher'],
    #         llm = self.llm,
    #         allow_delegation=True,
    #         # tools=[self.pub_tool],
    #         cache=True,
    #         verbose=True,
    #     )