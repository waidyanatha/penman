#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

''' Initialize with default environment variables '''
__name__ = "__propAttr__"
__package__= "scrape"
__module__ = "topics"
__app__ = "wrangler"
__ini_fname__ = "app.ini"
__conf_fname__ = "app.cfg"

''' Load necessary and sufficient python librairies that are used throughout the class'''
try:
    import os
    import sys
    import configparser    
    import logging
    import traceback
    import functools
    import findspark
    findspark.init()
    from pyspark.sql import functions as F
    from pyspark.sql import DataFrame
    from pyspark.sql.types import *
    from pyspark.sql.window import Window
    from datetime import datetime, date, timedelta

    print("All functional %s-libraries in %s-package of %s-module imported successfully!"
          % (__name__.upper(),__package__.upper(),__module__.upper()))

except Exception as e:
    print("Some packages in {0} module {1} package for {2} function didn't load\n{3}"\
          .format(__module__.upper(),__package__.upper(),__name__.upper(),e))

'''
    CLASS configure the master property details, groups, reference, and geom entities

    Contributors:
        * farmraider@protonmail.com

    Resources:

'''

class properties():

    ''' Function --- INIT ---

            author: <farmraider@protonmail.com>
    '''
    def __init__(
        self,
        realm:str=None,
        desc :str=None,
        **kwargs):
        """
        Decription:
            Initializes the features: class property attributes, app configurations, 
                logger function, data store directory paths, and global classes 
        Attributes:
            desc (str) identify the specific instantiation and purpose
        Returns:
            None
        """

        self.__name__ = __name__
        self.__package__ = __package__
        self.__module__ = __module__
        self.__app__ = __app__
        self.__ini_fname__ = __ini_fname__
        self.__conf_fname__ = __conf_fname__
        if desc is None or "".join(desc.split())=="":
            self.__desc__ = " ".join([self.__app__,self.__module__,
                                      self.__package__,self.__name__])
        else:
            self.__desc__ = desc

        self._data = None   # dataframe holding data class property
        self._realm= None
        if realm is not None:
            self._realm = realm
        self._realmList = ['portfolio',  # weighted asset portfolio (wap) selected for a datetime
                           'indicator',  # technical analysis indicators of each wap
                           'rebalance',  # rebalance history of the wap for each rebalanced datetime
                           'marketcap'   # past asset market capitalization, price, and volume data
                          ]
        self._rebalance=None
        self._index = None
#         self._attrs = {}
        global __def_db_attrs_dict__
        __def_db_attrs_dict__ = {
            "DBSCHEMA" : 'warehouse',
            "RFTBLNAME" : 'mcap_past',
            "RFDATEATTR": 'mcap_date',
            "RFNAMEATTR": 'asset_name',
            "RFVALATTR" : 'mcap_value',
            "RFWEIGHTATTR":'mcap_weight',
            "RFRORATTR" : 'mcap_simp_ror',
            "RFWTRORATT": 'weighted_ror',
            "RFASSETLST"  :['bitcoin'],
            "ASSETTBLNAME" :'mcap_past',
            "ASSETDATEATTR":'mcap_date',
            "ASSETNAMEATTR":'asset_name',
            "ASSETVALATTR" :'mcap_value',
            "ASSETWTATTR" : 'weight',
            "ASSETRORATTR" :'mcap_simp_ror',
            "ASSETWTRORATTR":'weighted_ror',
        }
        self._db_attrs = __def_db_attrs_dict__

        global pkgConf  # this package configparser class instance
        global appConf  # configparser class instance
        global logger   # rezaware logger class instance
#         global clsSDB   # etl loader sparkRDB class instance

        __s_fn_id__ = f"{self.__name__} function <__init__>"
        
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
            logger.info("%s Class",self.__name__)

            ''' import spark RDBM work load utils to read and write data '''
            from rezaware.modules.etl.loader import sparkRDBM as db
            self._clsSDB = db.dataWorkLoads(
                desc=self.__desc__,
#                 db_type = 'postgresql',
#                 db_name = 'tip',
#                 db_schema='warehouse',
#                 db_user = os.getenv("DATABASE_USER") #'farmraider',
#                 db_pswd = os.getenv("DATABASE_PSWD") #'spirittribe',
                spark_save_mode='append',
            )
            ''' import spark mongo work load utils to read and write data use app.cfg '''
            from rezaware.modules.etl.loader import sparkNoSQL as nosql
            self._clsNoSQL = nosql.dataWorkLoads(
                desc = self.__desc__,
#                 db_type = None, # database type mongodb, casandra, etc
#                 db_name = None,
#                 db_format=None,
#                 db_user = None,
#                 db_pswd = None,
#                 db_auth_source = None,
#                 db_auth_mechanism=None,
                **kwargs,
            )
#             ''' import spark time-series work load utils for rolling mean/variance computations '''
#             from rezaware.modules.ml.timeseries import rollingstats as stats
#             self._clsStats = stats.RollingStats(desc=self.__desc__)
            ''' import assset performance index class '''
            from mining.modules.finance.analysis import technical as ta
            self._clsTA =ta.AssetMovement(desc=self.__desc__)
            ''' import asset portfolio financial returns class '''
            from mining.modules.finance.analysis import returns as ret
            self._clsRet =ret.AssetMovement(desc=self.__desc__)
#             ''' import asset portfolio financial mpt class '''
#             from mining.modules.finance.analysis import mpt as mpt
#             self._clsMPT =mpt.AssetMovement(desc=self.__desc__)

            logger.debug("%s initialization for %s module package %s %s done.\nStart workloads: %s."
                         %(self.__app__,
                           self.__module__,
                           self.__package__,
                           self.__name__,
                           self.__desc__))

            print("%s Class initialization complete" % self.__name__)

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return None


    ''' Function --- CLASS PROPERTIES ---

            author: <farmraider@protonmail.com>

    '''
    ''' --- SPARK DATABASE CIONNECTION --- '''
    @property
    def clsSDB(self):
        """
        Description:
        Attributes :
        Returns :
        Exceptions :
        """

        __s_fn_id__ = f"{self.__name__} function <@property clsSDB>"

        try:
            if self._clsSDB is None:
                raise ConnectionError("No spark database connection detected")

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._clsSDB

    @clsSDB.setter
    def clsSDB(self,clsObj):

        __s_fn_id__ = f"{self.__name__} function <@setter clsSDB>"

        try:
            if clsObj is None:
                raise ConnectionError("Invalid spark session, cannot assign to property")

            self._clsSDB = clsObj 

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._clsSDB


    ''' --- SPARK NOSQL CIONNECTION --- '''
    @property
    def clsNoSQL(self):
        """
        Description:
        Attributes :
        Returns :
        Exceptions :
        """

        __s_fn_id__ = f"{self.__name__} function <@property clsNoSQL>"

        try:
            if self._clsNoSQL is None:
                raise ConnectionError("No spark clsNoSQL connection detected")

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._clsNoSQL

    @clsNoSQL.setter
    def clsNoSQL(self,clsObj):

        __s_fn_id__ = f"{self.__name__} function <@setter clsNoSQL>"

        try:
            if clsObj is None:
                raise ConnectionError("Invalid spark NoSQL session, cannot assign to property")

            self._clsNoSQL = clsObj 

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._clsNoSQL

    ''' DATABASE ATTRIBUTE DEFINITION '''
    @property
    def db_attrs(self):
        """
        Description:
            index @property and @setter functions to hold index measurements
        Attributes:
            None
        Returns (dataframe) self._index
        """

        __s_fn_id__ = f"{self.__name__} function <@property attrs>"

        try:
            if self._db_attrs is None:
                self._db_attrs = __def_db_attrs_dict__
                logger.warning("%s Invalid %s db_attrs class property set to default: %s...", 
                               __s_fn_id__, type(self._db_attrs), ",".join(list(self._db_attrs)[:3]))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._db_attrs

    @db_attrs.setter
    def db_attrs(self,db_attrs):

        __s_fn_id__ = "function <@setter db_attrs>"

        try:
            if db_attrs is None or not isinstance(db_attrs,dict):
                raise AttributeError("Invalid class property db_attrs %s" % type(db_attrs))
            for _attr_key, _attr_val in db_attrs.items():
                if _attr_key in __def_db_attrs_dict__:
                    self._db_attrs[_attr_key]=_attr_val

#             self._attrs = attrs

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._db_attrs
