#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

''' Initialize with default environment variables '''
__name__ = "vectorize_pdf"
__package__ = "stock"
__module__ = "article"
__app__ = "wrangler"
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

    import findspark
    findspark.init()
    from pyspark.sql import functions as F
    from pyspark.sql import DataFrame
    from typing import List, Iterable, Dict, Tuple
    ''' langchain '''
    # from langchain_community.document_loaders import TextLoader, PyPDFDirectoryLoader
    from langchain.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community import embeddings
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.chains import create_retrieval_chain
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser
    ''' fixes the problem with sqllite warning '''
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

    # from rezaware.modules.etl.loader import __propAttr__ as attr

    print("All functional %s-libraries in %s-package of %s-module imported successfully!"
          % (__name__.upper(),__package__.upper(),__module__.upper()))

except Exception as e:
    print("Some packages in {0} module {1} package for {2} function didn't load\n{3}"\
          .format(__module__.upper(),__package__.upper(),__name__.upper(),e))

'''
    Class to read pdf files from folder and upload embeddings into vector DB
        Current working vector databases: 
        * Chroma

    Contributors:
        * samana.thetha@gmail.com
        * farmraider@protonmail.com

    Resources:
        * Notebooks
            * Upsert function evaluation use utils/notebooks/etl/load/sparkDBwls.ipynb
        * Installation guide
            * https://computingforgeeks.com/how-to-install-apache-spark-on-ubuntu-debian/
        * Acknowledgement
            * 
'''
# class dataWorkLoads(attr.properties):
class dataWorkLoads():

    def __init__(
        self, 
        desc : str="vector data workloads", # identifier for the instances
        db_type : str = None, # database type one of self._dbTypeList
    )->None:
        """
        Description:
            Initializes the dataWorkLoads: class property attributes, app configurations, 
                logger function, data store directory paths, and global classes
        Attributes:
            desc (str) to change the instance description for identification
        Returns:
            None
        """

        ''' instantiate property attributes '''
#         super().__init__(
# #             desc=self.__desc__,
#             realm="DATABASE"
#         )

        self.__name__ = __name__
        self.__package__ = __package__
        self.__module__ = __module__
        self.__app__ = __app__
        self.__ini_fname__ = __ini_fname__
        self.__conf_fname__ = __conf_fname__
        self.__desc__ = desc

        __s_fn_id__ = f"{self.__name__} function <__init__>"

        ''' default values '''
        
        ''' initiate to load app.cfg data '''
        global logger
        global pkgConf
        global appConf

        try:
            self.cwd=os.path.dirname(__file__)
            pkgConf = configparser.ConfigParser()
            pkgConf.read(os.path.join(self.cwd,__ini_fname__))

            self.rezHome = pkgConf.get("CWDS","PROJECT")
            sys.path.insert(1,self.rezHome)

            ''' innitialize the logger '''
            from rezaware.utils import Logger as logs
            logger = logs.get_logger(
                cwd=self.rezHome,
                app=self.__app__, 
                module=self.__module__,
                package=self.__package__,
                ini_file=self.__ini_fname__)
            ''' set a new logger section '''
            logger.info('########################################################')
            logger.info("%s %s",self.__name__,self.__package__)

            logger.debug("%s initialization for %s module package %s %s done.\nStart workloads: %s."
                         %(self.__app__,
                           self.__module__,
                           self.__package__,
                           self.__name__,
                           self.__desc__))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return None

    ''' Function --- LOAD PDF ---

        authors: <nuwan@soulfish.lk>
    '''
    @staticmethod
    def load_pdf_files(
        folder_path:str=None,
        **kwargs
    )->List:
        """
        Description:
            Loads all the PDFs in a folder to a list of langchain Documents
        Attributes :
            folder_path (str) directing to the folder
        Returns :
            documents (list)
        Exceptions :
            Incorrect folder path raizes exception
            Folder with no PDFs raises an exception
        """

        __s_fn_id__ = f"{dataWorkLoads.__name__} function <load_pdf_files>"

        try:
            if not os.path.isdir(folder_path):
                raise AttributeError("Invalid folder path %s" % folder_path)
            logger.debug("%s Loading PDFs from %s", __s_fn_id__, folder_path)
            ''' load into documents '''
            documents = []
            for file in os.listdir(folder_path):
                if file.endswith('.pdf'):
                    pdf_path = os.path.join(folder_path, file)
                    loader = PyPDFLoader(pdf_path)
                    documents.extend(loader.load())
            if not isinstance(documents,list) or len(documents)<=0:
                raise RuntimeError("Failed to load PDFs from %s" % folder_path)

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)
            return None

        finally:
            logger.info("%s Loaded %d document pages", __s_fn_id__, len(documents))
            return documents

    
    ''' Function --- TEXT TO CHUKS ---

        authors: <nuwan@soulfish.lk>
    '''
    @staticmethod
    def text_to_chunks(
        text:list=None,
        chunk_size:int=1000, 
        chunk_overlap:int=200,
        **kwargs
    )->List:
        """
        Description:
            Split the text to chunks
        Attributes :
            folder_path (str) directing to the folder
        Returns :
            documents (list)
        Exceptions :
            Incorrect folder path raizes exception
            Folder with no PDFs raises an exception
        """

        __s_fn_id__ = f"{dataWorkLoads.__name__} function <text_to_chunks>"

        try:
            ''' validate inputs '''
            if not isinstance(text,list) or len(text)<=0:
                raise AttributeError("Invalid %s text" % type(text))
            if not isinstance(chunk_size,int) and chunk_size<=0:
                raise AttributeError("Invalid chunk_size %d must be > 0; typically 1000")
            if not isinstance(chunk_overlap,int) and chunk_overlap<0:
                raise AttributeError("Invalid chunk_overlap %d must be >= 0")
            logger.debug("%s Splitting %d text documents into %d chunks with %d overlap", 
                         __s_fn_id__, len(text), chunk_size, chunk_overlap)
            ''' split the text '''
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap
            )
            chunks = text_splitter.split_documents(text)
            if not isinstance(chunks,list) or len(chunks)<=0:
                raise RuntimeError("Failed split %d text document" % len(text))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)
            return None

        finally:
            logger.info("%s Split %d document into %d chunks", __s_fn_id__, len(text), len(chunks))
            return chunks
