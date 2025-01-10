#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

''' Initialize with default environment variables '''
__name__ = "search_tool"
__package__ = "author"
__module__ = "article"
__app__ = "mining"
__ini_fname__ = "app.ini"
__conf_fname__ = "app.cfg"

''' Load necessary and sufficient python librairies that are used throughout the class'''
try:
    import os
    import sys
    import configparser    
    import logging
    import functools
    import traceback
    # import requests, os
    # from langchain_community.embeddings import HuggingFaceEmbeddings
    from crewai.project import tool
    from crewai.tools import BaseTool
    from langchain.tools import Tool
    # from langchain_community.document_loaders import WebBaseLoader
    # from langchain.text_splitter import CharacterTextSplitter
    from langchain_core.retrievers import BaseRetriever
    # from langchain_openai import OpenAIEmbeddings
    # from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_chroma.vectorstores import Chroma
    # from langchain_community.tools import DuckDuckGoSearchRun
    # from langchain.utilities import DuckDuckGoSearchAPIWrapper
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.document_loaders import TextLoader
    # from langchain.tools import BaseTool
    # from langchain_core.tools import tool

    print("All functional %s-libraries in %s-package of %s-module imported successfully!"
          % (__name__.upper(),__package__.upper(),__module__.upper()))

except Exception as e:
    print("Some packages in {0} module {1} package for {2} function did not load\n{3}"\
          .format(__module__.upper(),__package__.upper(),__name__.upper(),e))

class toolWorkLoads(BaseTool):

    name = "write_article"
    description = "Gets the current price of a stock."

    def __init__(
        self,
        desc : str="vector search workloads", # identifier for the instances
        job_id:str=None, # unique identifier associated with the author processes
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

        ''' initilize class parameters '''
        self._dbType = "chromadb"
        self._dbRoot = None   # defined after invoking the configparser
        if job_id is None or "".join(job_id.split())=="":
            self._job_id = __def_job_id__
        else:
            self._job_id = job_id
        ''' globally used class objects '''
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

            self._dbRoot = os.path.join([pkgConf.get("CWDS","DATA"),self._job_id])

            ''' VECTORDB '''
            from rezaware.modules.etl.loader import vectorDB
            clsVDB = vectorDB.dataWorkLoads(
                db_type='chromadb', 
                db_root=self._dbRoot, 
                db_name="research")

            ''' innitialize the logger '''
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

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return None

    @tool
    def retrieve_outline(
        self,
    )-> Tool:

        __s_fn_id__ = f"{self.__name__} function <retrieve_outline>"
        try:
            # Initialize file reader
            loader = TextLoader(fpath)
            documents = loader.load()
            for doc in documents:
                outline+=doc.page_content
            # search = load_pdf()
        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)
            return None

        finally:
            return Tool(
                name="read stored text from file",
                func=clsVDB.read_vectors(
                    db_name=None,
                    collection=None,
                    embedding_fn=None,
                    **kwargs,
                    ),
                description="specifically for reading the outline of an article."            
            ) # return langchain vectorstore to invoke a retriever

    @tool
    def retrieve_research(self, topic)-> Tool:

        try:

            __s_fn_id__ = f"{self.__name__} @tool <retrieve_research>"
            # __db_type__ = "chromadb"
            __db_name__ = "research"
            # __chromadb_dir__ = "/home/nuwan/workspace/penman/wrangler/data/article/stock/"
            __collection__= "topic_research_results"
            _embedding_fn = OllamaEmbeddings(model='nomic-embed-text')
            
            if __collection__ not in [x.name for x in clsVDB.get_collections(db_name = __db_name__)]:
                logger.debug("%s did you mean one of the following:\n", 
                             __s_fn_id__, clsVDB.get_collections(db_name = __db_name__))
                raise AttributeError("First run wrangler scrape to create the collection %s with embeddings"
                                     % __collection__.upper())
    
            else:
                logger.debug("%s collection %s exists; reading documents", 
                             __s_fn_id__, __collection__.upper())
                vectorstore=None
                clsVDB._dbRoot="/home/nuwan/workspace/penman/wrangler/data/topic/scrape/def_job123/"

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        finally:
            return Tool(
                name="stored research ebeddings",
                func=clsVDB.read_vectors(
                    db_name = __db_name__,
                    collection = __collection__,
                    embedding_fn=_embedding_fn,        
                ),
                description="Useful for searching vectore store for topic information."
            ) # return vectorestore to construct a langchain retriever


#     @tool("Topic content read and write Tool")
#     def topics_search(query: str):
#         """Fetch topic specific content and process them."""
# #         API_KEY = os.getenv('NEWSAPI_KEY')  # Fetch API key from environment variable
# #         base_url = "https://newsapi.org/v2/everything"
        
#         params = {
#             'q': query,
# #             'sortBy': 'publishedAt',
# #             'apiKey': API_KEY,
#             'language': 'en',
#             'pageSize': 5,
#         }
        
#         response = requests.get(base_url, params=params)
#         if response.status_code != 200:
#             return "Failed to retrieve topic content."
        
#         articles = response.json().get('articles', [])
#         all_splits = []
#         for article in articles:
#             # Assuming WebBaseLoader can handle a list of URLs
#             loader = WebBaseLoader(article['url'])
#             docs = loader.load()

#             text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#             splits = text_splitter.split_documents(docs)
#             all_splits.extend(splits)  # Accumulate splits from all articles

#         # Index the accumulated content splits if there are any
#         if all_splits:
#             vectorstore = Chroma.from_documents(all_splits, 
#                                                 embedding=embedding_function, 
#                                                 persist_directory="./chroma_db")
#             retriever = vectorstore.similarity_search(query)
#             return retriever
#         else:
#             return "No content available for processing."
