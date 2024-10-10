#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# import os
# from dotenv import load_dotenv
# load_dotenv()

# from mining.modules.crypto.etp import rwRDB as rdb
# from mining.modules.crypto.ai import crew as cr

def run():
    inputs = {
        "topics": ['common alerting protocol','ITU X.1303'],
        "title" : 'why common alerting protocol is essential for early warning',
        "aptitude":'Unversity junior level student in public safety administration'
    }
#     clsCrew = cr.crewWorkLoads()
    clsCrew.crew().kickoff(inputs=inputs)


''' Function --- LOGGER ---
    author: <farmraider@protonmail.com>
'''
def get_logger_handle(
    log_dir:str=None,
    file_name:str="app.log",
):
    """
    Description:
        Invokes a logging instance for the setup process
    Attribute:
        NA
    Returns:
        logger (logger) object
    """
    __s_fn_id__ = f"{__name__} function <get_logger_handle>"

    __def_log_form__ = '[%(levelname)s] - %(asctime)s - %(name)s - %(message)s'
    
    try:
        ''' validate function inputs '''
        if log_dir is None or "".join(log_dir.split())=="":
            log_dir=os.path.dirname(__file__)
        if file_name is None or "".join(file_name.split())=="":
            file_name="app.log"

        ''' formulate file path '''
        if not os.path.isdir(os.path.join(log_dir)):
            os.makedirs(os.path.join(log_dir))
        _log_fpath=os.path.join(log_dir,file_name)
        if not os.path.exists(_log_fpath):
            with open(_log_fpath, 'w') as fp:
                pass

        ''' invoke logging instance '''
        logger = logging.getLogger("DAG")
        logger.setLevel("DEBUG")
        if (logger.hasHandlers()):
            logger.handlers.clear()
        fh = logging.FileHandler(_log_fpath,'w+')
        fh.setLevel("DEBUG")
        formatter = logging.Formatter(__def_log_form__)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    except Exception as err:
        logger.error("%s %s \n",__s_fn_id__, err)
        logger.debug(traceback.format_exc())
        print("[Error]"+__s_fn_id__, err)

    return logger

''' Function --- MAIN --- 
    author: <farmraider@protonmail.com>
'''
def main():
    """
    Description:
        The main function will execute all steps for setting up a new project or
        updating the configuration of an existing project
    Attributes:
        NA
    Returns
        NA
    Exception(s):
    """

    __s_fn_id__ = f"{__name__} function <main>"
    __def_from_days__= 10
    __def_date_format__ = '%Y-%m-%d'
    __def_fname__ = 'params_build_wap.json'
    __desc__ = " ".join([__app__, __module__, __package__, __name__])

    global config
    global logger
    global clsCrew

    try:
        cwd=os.path.dirname(__file__)
        proj_dir = os.path.abspath(cwd).split(f'{__app__}/')[0]
        sys.path.insert(1,proj_dir)

        ''' innitialize the logger '''
        _log_dir=os.path.join(proj_dir,__app__,'logs',__module__,__package__)
        logger = get_logger_handle(
            log_dir=_log_dir,
            file_name = "app.log",
        )
        ''' set a new logger section '''
        logger.info('########################################################')
        logger.info("Initializing Main in %s",__name__)

        ''' import portfolio build classes '''
        from wrangler.modules.topics.research import crew as cr
        clsCrew = cr.aiWorkLoads()

#         ''' define args '''
#         parser = argparse.ArgumentParser(description="setup main controller arg and flags")
#         parser.add_argument("--file",type= str)

#         d = vars(parser.parse_args())

#         ''' read from json parameter file '''
#         _fpath = os.path.join(proj_dir,__app__,'data',__module__,__package__,__def_fname__)
#         if "file" in d.keys() and d["file"] is not None and "".join(d["file"].split())!="":
#             _fpath = d["file"]
#             logger.debug("%s file path set to %s",__s_fn_id__,str(_fpath))
#             ''' validate file exists and is a json dict '''
#             if not os.path.isfile(_fpath):
#                 raise ValueError("Invalid file %s does NOT exist" % _fpath)
#             logger.debug("%s confirmed %s exisits", __s_fn_id__, _fpath)
#             ''' read the df of from and to dates '''
#             param_dict = read_param_dict(_fpath)
#             if not isinstance(param_dict, dict) \
#                 or len(param_dict)<=0:
#                 raise AttributeError("Failed valid read parameters from %s" 
#                                      % _fpath.upper())
#             logger.debug("%s Successfully got %d validated parameters from %s", 
#                          __s_fn_id__, len(param_dict), _fpath)

#         else:
#             raise AttributeError("missing --file argument with valid parameter json file")

#         ''' go through each date between from and to '''
#         total_days_, saved_date_lst_ = 0, []
#         saved_date_lst_, total_days_ = move_daily_wap(params=param_dict)
# #         if not isinstance(saved_date_lst_,list) or len(saved_date_lst_)<=0:
# #             raise ChildProcess("Failed select_top_assets returned empty %s dates list" 
# #                                % type(saved_date_lst_))
#         logger.debug("%s Completed moving weighted assets portfolios for %d of %d dates", 
#                      __s_fn_id__, len(saved_date_lst_), total_days_)

        run()
        print("done %s" % datetime.now().isoformat())

    except Exception as err:
        logger.error("%s %s \n",__s_fn_id__, err)
        logger.debug(traceback.format_exc())
        print("[Error]"+__s_fn_id__, err)

    return None

''' EXECUTION CONTROLLER '''
if __name__ == "__main__":
    ''' Initialize with default environment variables '''
    __name__ = "main"
    __package__ = "research"
    __module__ = "topics"
    __app__ = "mining"
    __ini_fname__ = "app.ini"
    __conf_fname__ = "app.cfg"
    __tmp_data_dir_ext__ = "tmp/"

    ''' Load necessary and sufficient python librairies that are used throughout the class'''
    try:
        ''' standard python packages '''
        import os
        import sys
        from dotenv import load_dotenv
        load_dotenv()
        import logging
        import traceback
        import functools
        import configparser
        import argparse
        
        from datetime import datetime, date, timedelta
        import pandas as pd
        import json
        from schema import Schema, And, Use, Optional, SchemaError

        cwd=os.path.dirname(__file__)
        proj_dir = os.path.abspath(cwd).split(f'{__app__}/')[0]
        sys.path.insert(1,proj_dir)

        print("All packages in %s %s %s %s imported successfully!"
              % (__app__,__module__,__package__,__name__))

        main()

    except Exception as e:
        print("Some software packages in {0} didn't load\n{1}".format(__name__,e))
