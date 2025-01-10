#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

''' Initialize with default environment variables '''
__name__ = "writer_crew"
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
    import requests
    from dotenv import load_dotenv
    load_dotenv()
    from typing import List, Iterable, Dict, Tuple
    
    ''' LANGCHAIN CREW '''
    from crewai import Crew, Agent, Task, Process
    from crewai.project import CrewBase, agent, crew, task
    from langchain_groq import ChatGroq
    from langchain_core.retrievers import BaseRetriever

    print("All functional %s-libraries in %s-package of %s-module imported successfully!"
          % (__name__.upper(),__package__.upper(),__module__.upper()))

except Exception as e:
    print("Some packages in {0} module {1} package for {2} function didn't load\n{3}"\
          .format(__module__.upper(),__package__.upper(),__name__.upper(),e))


# @CrewBase
class aiWorkLoads():
    # name = "writer_crew"
    agents_config= "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
#     output_file= "mining/data/article/author/article.txt"
    # input_file= "/home/nuwan/workspace/penman/wrangler/data/topic/scrape/topic_research.txt"
    # chroma_db = "/home/nuwan/workspace/penman/wrangler/data/topic/scrape/"

    def __init__(
        self,
        desc : str="vector search workloads", # identifier for the instances
        job_id:str=None # unique identifier associated with the author processes
        ) -> None:

        self.__name__ = __name__
        self.__package__ = __package__
        self.__module__ = __module__
        self.__app__ = __app__
        self.__ini_fname__ = __ini_fname__
        self.__conf_fname__ = __conf_fname__
        self.__desc__ = desc

        __s_fn_id__ = f"{self.__name__} function <__init__>"

        __def_job_id__="def_job123"

        if job_id is None or "".join(job_id.split())=="":
            self._job_id = __def_job_id__
        else:
            self._job_id = job_id

        global logger
        global pkgConf
        global appConf
        global clsVDB

        try:
            self.cwd=os.path.dirname(__file__)
            pkgConf = configparser.ConfigParser()
            pkgConf.read(os.path.join(self.cwd,__ini_fname__))

            self.projHome = pkgConf.get("CWDS","PROJECT")
            sys.path.insert(1,self.projHome)

            self._dbRoot = os.path.join(pkgConf.get("CWDS","DATA"),self._job_id)

            # ''' VECTORDB '''
            # from rezaware.modules.etl.loader import vectorDB
            # clsVDB = vectorDB.dataWorkLoads(
            #     db_type='chromadb', 
            #     db_root=self._dbRoot, 
            #     db_name="research")

            ''' initialize the logger '''
            from rezaware.utils import Logger as logs
            logger = logs.get_logger(
                cwd=self.projHome,
                app=self.__app__, 
                module=self.__module__,
                package=self.__package__,
                ini_file=self.__ini_fname__)
            ''' set a new logger section '''
            logger.info('########################################################')
            logger.info("%s %s",self.__name__,self.__package__)

            self.groq_llm = ChatGroq(
                name='groq',
                groq_api_key=os.environ.get("GROQ_API_KEY"),
                temperature=0.3,
                max_tokens =300,
                max_retries=0,
                model_name="groq/mixtral-8x7b-32768")

            ''' AGENTS '''
            from mining.modules.article.author import agents
            agents = agents.agentWorkLoads(llm=self.groq_llm)
            logger.debug("%s Instantiated Agents with llm: %s model:%s", 
                         __s_fn_id__, self.groq_llm.name.upper(), 
                         self.groq_llm.model_name.upper())
            self.outline_retriever=agents.outline_retriever()
            logger.debug("%s loaded %s with tools: %s", __s_fn_id__,
                         type(self.outline_retriever),
                         str(self.outline_retriever.tools).upper())
            # self.research_retriever = agents.research_retriever() 
            # self.article_author = agents.article_author() 
            # self.draft_publisher = agents.draft_publisher()
            ''' TASKS '''
            from mining.modules.article.author import tasks
            tasks = tasks.taskWorkLoads()
            self.load_outline_task=tasks.load_outline_task(agent=self.outline_retriever)
            logger.debug("%s loaded %s %s with expected output %s", __s_fn_id__,
                         type(self.load_outline_task),
                         self.load_outline_task.name.upper(),
                         self.load_outline_task.expected_output.upper())
            # self.load_research_task=tasks.load_research_task(agent=self.research_retriever)
            # self.author_article_task=tasks.author_article_task(agent=self.article_author)
            # self.publish_draft_task=tasks.publish_draft_task(agent=self.article_author)
            # self.draft_publisher=tasks.draft_publisher(agent=self.article_author)
            # self.tool.search = DuckDuckGoSearchAPIWrapper()

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return None


    @crew
    def crew(self) -> Crew:

        try:
            log_file = "/home/nuwan/workspace/penman/mining/logs/article/author/writer_crew_output.log"

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)
            return None

        finally:
            return Crew(
                agents= [self.outline_retriever],
                tasks = [self.load_outline_task],
                process=Process.sequential,
                output_log_file = log_file,
                full_output = True,
                verbose = True
            )

    ''' Run the crew '''
    def _run(self, inputs):

        result = self.crew().kickoff(inputs=inputs)
        # Process task content
        print(type(self.load_outline_task.output.raw),self.load_outline_task.output.raw)
        print("\nCrew _run complete.")

        return result #, search_results

        # self.groq_llm = ChatGroq(temperature=0, model_name="groq/mixtral-8x7b-32768")        

#     @agent
#     def outline_retriever(self) -> Agent:
#         return Agent(
#             config = self.agents_config['outline_retriever'],
#             llm = self.groq_llm
#         )

#     @task
#     def retrieve_outline(self) -> Task:
#         return Task(
#             config = self.tasks_config['load_outline_task'],
# #             output_file=self.output_file,
#             input_file =self.input_file,
#             agent = self.outline_retriever()
#         )

#     @agent
#     def research_retriever(self) -> Agent:
#         return Agent(
#             config = self.agents_config['research_retriever'],
#             llm = self.groq_llm
#         )

#     @task
#     def retrieve_research(self) -> Task:
#         return Task(
#             config = self.tasks_config['load_research_task'],
# #             output_file=self.output_file,
#             input_file =self.input_file,
#             agent = self.research_retriever()
#         )

#     @agent
#     def article_author(self) -> Agent:
#         return Agent(
#             config = self.agents_config['article_author'],
#             llm = self.groq_llm
#         )

#     @task
#     def author_article_task(self) -> Task:
#         return Task(
#             config = self.tasks_config['author_article_task'],
# #             output_file=self.output_file,
#             input_file =self.input_file,
#             agent = self.article_author()
#         )

#     @agent
#     def draft_publisher(self) -> Agent:
#         return Agent(
#             config = self.agents_config['draft_publisher'],
#             llm = self.groq_llm
#         )

#     @task
#     def publish_draft_task(self) -> Task:

#         return Task(
#             config = self.tasks_config['publish_draft_task'],
#             output_file =self.output_file,
#             agent = self.draft_publisher()
#         )

