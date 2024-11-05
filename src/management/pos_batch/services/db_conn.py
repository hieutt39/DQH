import os
import shutil
from datetime import datetime
from django.conf import settings
import pymysql
import sqlalchemy as sql
import pandas as pd
from .sync_message import SyncMessage, logger


class DbConn(SyncMessage):
    def __init__(self, source_info=None, destination_info=None):
        super(DbConn, self).__init__()
        # conn = connect(':memory:')
        self.conn_sqlite = None
        self.keys = ['Main', 'Second']
        self.columns = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']
        if source_info is None and destination_info is None:
            source_info = settings.MIGRATE_DB['source']
            destination_info = settings.MIGRATE_DB['destination']

        self.keys[0] = f'{source_info["database"]} (Source)'
        self.keys[1] = f'{destination_info["database"]} (Destination)'

        self.database_names = {
            'source': source_info["database"],
            'destination': destination_info["database"],
        }

        self.conn_source = self.mysql_connect(source_info)
        self.conn_destination = self.mysql_connect(destination_info)

    # def __del__(self):
    # self.mysql_disconnect()

    def re_connection(self):
        self.mysql_disconnect()
        self.mysql_connect()

    def get_structure(self, table_name, conn):
        """
        Parameters
        ----------
        table_name

        Returns DataFrame
        -------

        """
        df = pd.DataFrame()
        try:
            df = pd.read_sql(f'DESCRIBE `{table_name}`;',
                             conn,
                             columns=self.columns,
                             )
        except:
            pass

        return df

    def filter_fields(self, df):
        """
        Parameters
        ----------
        df: DataFrame

        Returns
        -------

        """
        list_fields = {}
        field_types = ['int', 'timestamp', 'varchar', 'text', 'date', 'datetime', 'decimal']
        for field_type in field_types:
            list_fields[field_type] = self.filter_field_by_type(df, field_type)

        return list_fields

    @staticmethod
    def filter_field_by_type(df, val, col='Type'):
        """
        Parameters
        ----------
        df: pd DataFrame
        val: value of column
        col: column names (Field, Type, Null, Key, Default, Extra)

        Returns
        -------

        """
        dff = df[df[col].str.contains(f"{val}")]
        return list(dff['Field'])

    def get_tables(self, db_name, conn):
        query_main = f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA="{db_name}" AND TABLE_TYPE="BASE TABLE";'''
        df = self.run_sql_query(query_main, conn)
        # df_main = df_main.loc[:, df_main.columns.isin(['TABLE_NAME'])]
        table_names = []
        for i in range(len(df)):
            table_names.append(df.loc[i, "TABLE_NAME"])
        return table_names

    def get_folder(self, name, by_timestamp=True, mode=0o777):
        """
        Parameters
        ----------
        name
        by_timestamp

        Returns
        -------
        """
        dir_name = f'{name}'
        dir_path = os.path.join(self.assets, dir_name)
        if by_timestamp:
            now = datetime.now()
            dir_name = f'{name}-{int(datetime.timestamp(now))}'
            dir_path = os.path.join(self.assets, dir_name)
        else:
            shutil.rmtree(dir_path, True)

        os.makedirs(dir_path, mode=mode, exist_ok=True)
        return dir_path

    @staticmethod
    def mysql_connect(conn_info: dict, lib_type='sqlalchemy'):
        """
        :return connection: Global MySQL database connection
        """
        conn = None
        logger.info('--------------------------- MYSQL: CONNECTING ---------------------------')
        if conn_info is not None:
            if lib_type == 'sqlalchemy':
                conn = sql.create_engine(
                    sql.URL.create(
                        drivername='mysql',
                        host=conn_info['hostname'],
                        username=conn_info['username'],
                        password=conn_info['password'],
                        database=conn_info['database'],
                        port=conn_info['port'])
                )
            elif lib_type == 'pymysql':
                conn = pymysql.connect(
                    host=conn_info['hostname'],
                    user=conn_info['username'],
                    passwd=conn_info['password'],
                    db=conn_info['database'],
                    port=conn_info['port'])
            else:
                logger.info(f'------------------ MYSQL: {conn_info["database"]} CONNECT FAILED -------------------')

            logger.info(f'----------------------- MYSQL: {conn_info["database"]} CONNECTED -----------------------')
        else:
            logger.info('--------------------------- MYSQL: CONNECT FAILED ---------------------------')

        return conn

    def mysql_disconnect(self):
        """Closes the MySQL database connection.
        """

        logger.info('--------------------------- MYSQL: DISCONNECTING ---------------------------')
        if self.conn_source is not None:
            # self.conn_source.close()
            logger.info('--------------------------- MYSQL: Main DISCONNECTED ---------------------------')

        if self.conn_destination is not None:
            # self.conn_destination.close()
            logger.info('--------------------------- MYSQL: Second DISCONNECTED ---------------------------')

    @staticmethod
    def run_query(sql, conn, chunksize=200, columns=[], on_test=False):
        """Runs a given SQL query via the global database connection.
        Parameters
        ----------
        :param sql: MySQL query
        :param conn: MySQL connection
        :param chunksize: limit records
        :param columns
        :param on_test
        :return: Pandas dataframe containing results
        """
        dfl = []
        if on_test:
            sql = f'{sql} limit 1;'

        logger.info(f'---SQL: {sql}: START')
        try:
            # Start Chunking
            for chunk in pd.read_sql(sql, conn, chunksize=chunksize):
                # Start Appending Data Chunks from SQL Result set into List
                logger.info(f'---SCANNED: {len(chunk)} records')
                dfl.append(chunk)

        except Exception as e:
            logger.error(e)
            dfl.append(pd.DataFrame(columns=columns))
        logger.info(f'---SQL: {sql}: END')

        # Start appending data from list to dataframe
        dfs = pd.concat(dfl, ignore_index=True)

        return dfs

    @staticmethod
    def run_sql_query(sql, conn):
        try:
            return pd.read_sql_query(sql, conn)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def export_csv(df, file_path):
        logger.info('START: export data to CSV')
        with pd.ExcelWriter(file_path) as writer:
            df.to_csv(writer, sheet_name='records', index=False)

        logger.info('FINISH: Export data to files')
