import logging
import numpy as np
import pandas as pd
import re
import os
import json
from pathlib import Path
from sqlite3 import OperationalError
from collections import Counter
from .db_conn import DbConn, logger
from django.conf import settings
from src.utilities.files.files import scan_files, clean_up, mkdir


class HealthDbService(DbConn):
    def __init__(self):
        super(HealthDbService, self).__init__()

    def healthcheck(self):
        query = '''SELECT VERSION();'''
        logger.info(f'--- Main DB ---')
        df_main = self.run_sql_query(query, self.conn_source)
        if df_main is not None:
            logger.info(df_main)
        logger.info(f'--- Second DB ---')
        df_second = self.run_sql_query(query, self.conn_destination)
        if df_second is not None:
            logger.info(df_second.head())

    def healthcheck_table(self):
        logger.info(f'--- Main DB ---')
        query_main = f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA="{self.migrate_db['main']['db']}" AND TABLE_TYPE="BASE TABLE";'''
        logger.info(query_main)
        df_main = self.run_sql_query(query_main, self.conn_source)
        # if df_main is not None:
        #     logger.info(df_main)
        logger.info(f'--- Second DB ---')
        query_second = f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA="{self.migrate_db['second']['db']}" AND TABLE_TYPE="BASE TABLE";'''
        logger.info(query_second)
        df_second = self.run_sql_query(query_second, self.conn_destination)
        # if df_second is not None:
        #     logger.info(df_second)

        df = pd.DataFrame(data=[
            ["Main", 'Second'],
            [df_main.shape[0], df_second.shape[0]],
        ])
        logger.info(df)

