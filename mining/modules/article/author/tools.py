#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# ''' Initialize with default environment variables '''
# __name__ = "load_files"
# __package__ = "author"
# __module__ = "article"
# __app__ = "mining"
# __ini_fname__ = "app.ini"
# __conf_fname__ = "app.cfg"

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
    from typing import List, Iterable, Dict, Tuple, Optional
    
    ''' LANGCHAIN CREW '''
    # from crewai import Task #, Crew, Agent, Process
    # from crewai.project import tool # CrewBase, agent, crew, task,
    from langchain.tools import BaseTool, Tool #, StructuredTool
    from langchain_core.tools import tool
    # from langchain_core.retrievers import BaseRetriever
    # from langchain.tools.file_management.toolkit import FileManagementToolkit
    # from langchain_community.agent_toolkits import FileManager
    # from langchain_community.agent_toolkits.file_management.utils import FileManager
    from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
# Importing crewAI tools # CANNOT because of poetry conflict
    from langchain_groq import ChatGroq

    print("All functional libraries imported successfully!")

except Exception as e:
    print("Some packages in load_files did not load properly %s",e)


class ReadFileTool(BaseTool):

    name = "read file content"
    description = "read outline from file"

    def __init__(
        self,
        desc : str="content retriever workloads", # identifier for the instances
    ) -> None:

        # super().__init__()

        # ''' Initialize with default environment variables '''
        print(__name__)
        # self.__name__ = "tools"
        # self.__package__ = "author"
        # self.__module__ = "article"
        # self.__app__ = "mining"
        __ini_fname__ = "app.ini"
        # self.__conf_fname__ = "app.cfg"
        # self.__desc__ = desc

        # __s_fn_id__ = f"{self.__name__} function <__init__>"

        __def_job_id__="def_job123"

        ''' initilize class parameters '''
        # self._dbRoot = None   # defined after invoking the configparser
        ''' globally used class objects '''
        global logger
        global pkgConf
        global appConf
        global clsVDB
        
        try:
            cwd=os.path.dirname(__file__)
            pkgConf = configparser.ConfigParser()
            pkgConf.read(os.path.join(cwd,__ini_fname__))

            projHome = pkgConf.get("CWDS","PROJECT")
            sys.path.insert(1,projHome)
            _dbRoot = os.path.join(pkgConf.get("CWDS","DATA"))

            # ''' innitialize the logger '''
            # from rezaware.utils import Logger as logs
            # logger = logs.get_logger(
            #     cwd=self.projHome,
            #     app=self.__app__, 
            #     module=self.__module__,
            #     package=self.__package__,
            #     ini_file=self.__ini_fname__)
            # ''' set a new logger section '''
            # logger.info('########################################################')
            # logger.info("%s %s",self.__name__,self.__package__)

        except Exception as err:
            # logger.error("%s %s \n",__s_fn_id__, err)
            # logger.debug(traceback.format_exc())
            print("[Error] ", err)

        return None

    # @tool
    # def read_outline(
    def _run(
        self,
        fname:str=None,
    )-> str:
        """
        read the topic outline file
        """

        # name="read outline tool"
        # description="read the outline from the specified dir location"

        # __s_fn_id__ = f"{self.__name__} @tool <read_outline>"

        __def_outline_fname__="topic_outline.txt"

        try:
            if fname is None or "".join(fname.split())=="":
                fname=__def_outline_fname__
                # logger.debug("%s fname %s undefined using default %s",
                #              __s_fn_id__,fname.upper())
            from rezaware.modules.etl.loader import sparkFile as file
            # _store_root = os.path.join(os.path.join(pkgConf.get("CWDS","DATA")),"article/author/")
            _store_root = os.path.join(pkgConf.get("CWDS","DATA"))
            _folder_path= "def_job123"
            clsFile=file.dataWorkLoads(
                store_mode='local-fs',
                store_root=_store_root
            )
            # # file_content = self.file_manager.read_file(fname)
            # readTool = FileManagementToolkit(
            #     root_dir=self._dbRoot, # dir for each job
            #     selected_tools=["read_file"],
            # ).get_tools()
            # if not isinstance(readTool,list) or len(readTool)<=0:
            #     raise AttributeError("Invalid %s tool" % type(readTool))

        except Exception as err:
            # logger.error("%s %s \n",__s_fn_id__, err)
            # logger.debug(traceback.format_exc())
            print("[Error] ", err)
            return None

        finally:
            return clsFile.read_files_to_dtype(
                as_type='str',
                folder_path=_folder_path,
                file_name=fname,
                file_type=None,
            )
    async def _arun(self, fname: str) -> str:
        """Asynchronous version of _run."""
        raise NotImplementedError("This tool does not support async")

    def retrieve_outline(
        self,
    )-> Tool:
        """
        read the outline from the file
        """
        fpath = "/home/nuwan/workspace/penman/wrangler/data/topic/scrape/def_job123/topic_outline.txt"
        fname = "topic_outline.txt"
        return Tool(
            name="read outline file content",
            func=self._run(fname), # raw outline,
            description="execute the function to read the topic outline content",
            verbose=True,
        )
