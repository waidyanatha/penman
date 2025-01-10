#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests, os
from dotenv import load_dotenv
load_dotenv()
from crewai import Crew, Process #BaseAgent
# from crewai import Crew, Agent, Task, Process, BaseAgent
from crewai.project import CrewBase, crew
# ''' caching '''
# from langchain_core.globals import set_llm_cache
# from langchain_core.caches import InMemoryCache
''' LANGCHAIN '''
# from langchain.tools import Tool
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.retrievers import BaseRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
# from langchain.agents import load_tools
# ''' RAG '''
# from langchain_community.vectorstores import Chroma
# from langchain_community.tools import DuckDuckGoSearchRun

print("import complete")

@CrewBase
class aiWorkLoads():

    def __init__(self) -> None:

        ''' TODO add param groq_api_key=gsk_XXXX '''
        self.groq_llm = ChatGroq(temperature=0, 
                                 max_tokens =3000,
                                 model_name="groq/mixtral-8x7b-32768")

#         ''' TOOLS '''
#         from wrangler.modules.topic.scrape import search_tool as tools
#         tools = tools.SearchWorkLoads()
#         self.search_tool = tools.duckduckgo()
        ''' AGENTS '''
        from wrangler.modules.parliment.scrape import agents
        agents = agents.ScraperAgents(llm=self.groq_llm)
        self.researcher=agents.content_planner()
        self.planner = agents.referrence_planner() 
        ''' TASKS '''
        from wrangler.modules.parliment.scrape import tasks
        tasks = tasks.ScraperTask()
        self.research_topic=tasks.store_content_task(agent=self.researcher)
#         self.plan_outline=tasks.plan_outline_task(agent=self.planner, context=[self.research_topic])
        self.plan_outline=tasks.plan_referrences_task(agent=self.planner)

        self.search = DuckDuckGoSearchAPIWrapper()

    @crew
    def crew(self) -> Crew:

        log_file = "/home/nuwan/workspace/penman/wrangler/logs/parliment/scrape/crew_full_output.log"
        return Crew(
            agents= [self.planner], #, self.researcher,
            tasks = [self.plan_outline], #self.research_topic, ,
            process=Process.sequential,
            manager_llm=self.groq_llm,
            output_log_file = log_file,
            full_output = True,
            verbose = True
        )

    # Function to load and process web content
    def load_and_process_url(self,url):
        loader = WebBaseLoader(url)
        data = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        return text_splitter.split_documents(data)

    # Function to store data in ChromaDB
    def store_in_chromadb(self,documents, collection_name):
        embeddings = HuggingFaceEmbeddings()
        db_path = f"/home/nuwan/workspace/penman/wrangler/db/chroma_db_{collection_name}"
        vectordb = Chroma.from_documents(
            documents,
            embeddings,
            persist_directory=db_path #f"./chroma_db_{collection_name}"
        )
        return vectordb

    ''' Run the crew '''
    def _run(self, inputs):

        result = self.crew().kickoff(inputs=inputs)

        # # Process and store the results
        # topic = ", ".join(inputs['topic']) # "artificial intelligence trends"
        # search_results = self.search.results(topic, max_results=10)  # Get top 10 results

        # all_documents = []
        # for item in search_results:
        #     url = item['link']
        #     try:
        #         documents = self.load_and_process_url(url)
        #         all_documents.extend(documents)
        #     except Exception as e:
        #         print(f"Error processing {url}: {e}")

        # # Store all documents in ChromaDB
        # _coll_name = "_".join(inputs['topic'][0].split())
        # print(f"all_documents... : {all_documents}")
        # vectordb = self.store_in_chromadb(documents=all_documents, collection_name=_coll_name)

        # print("Data has been successfully stored to %s in ChromaDB." % _coll_name)

        return result #, search_results