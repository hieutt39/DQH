import json
import logging
from django.conf import settings
import sshtunnel
import paramiko
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from difflib import Differ, HtmlDiff, unified_diff, SequenceMatcher

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DbConn:
    def __init__(self):
        self.conn_source = None
        self.conn_destination = None
        self.tunnel_source = None
        self.tunnel_destination = None

    def __del__(self):
        self.mysql_disconnect()

    def re_connection(self):
        self.mysql_disconnect()

    def mysql_connect(self, db_config: dict, ssh_config: dict):
        """Connect to a MySQL server using the SSH tunnel connection

        :return connection: Global MySQL database connection
        """
        tunnel = None
        logger.info('--------------------------- MYSQL: CONNECTING ---------------------------')
        try:
            if ssh_config.get('ssh_tunnel', False):
                # SSH connection
                tunnel = self._ssh_open_tunnel(ssh_config, db_config)
                conn = pymysql.connect(
                    host='127.0.0.1',
                    user=db_config.get('username'),
                    passwd=db_config.get('password'),
                    db=db_config.get('db'),
                    port=tunnel.local_bind_port
                )
            else:
                conn = pymysql.connect(
                    host=db_config.get('host'),
                    user=db_config.get('username'),
                    passwd=db_config.get('password'),
                    db=db_config.get('db'),
                    port=db_config.get('port')
                )
        except Exception as e:
            logger.error(e)
            raise Exception(f"<code class='text-red'>{str(e)}</code>")
        logger.info('--------------------------- MYSQL: CONNECTED ---------------------------')

        return conn, tunnel

    def mysql_disconnect(self):
        """Closes the MySQL database connection.
        """
        logger.info('--------------------------- MYSQL: DISCONNECTING ---------------------------')
        if self.conn_source is not None:
            self.conn_source.close()
            logger.info('--------------------------- MYSQL: SOURCE DISCONNECTED ---------------------------')
        if self.conn_destination is not None:
            self.conn_destination.close()
            logger.info('--------------------------- MYSQL: DESTINATION DISCONNECTED ---------------------------')
        if self.tunnel_source is not None:
            self.tunnel_source.close()
            logger.info('--------------------------- TUNNEL: SOURCE DISCONNECTING ---------------------------')
        if self.tunnel_destination is not None:
            self.tunnel_destination.close()
            logger.info('--------------------------- TUNNEL: DESTINATION DISCONNECTING ---------------------------')

    @staticmethod
    def _ssh_open_tunnel(ssh_config: dict, db_config: dict = None, verbose=False):
        """Open an SSH tunnel and connect using a username and password.

        :param verbose: Set to True to show logging
        :return tunnel: Global SSH tunnel connection

        Parameters
        ----------
        ssh_config
        """
        if verbose:
            sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

        logger.info('--------------------------- SSH: OPEN TUNNEL ---------------------------')
        try:
            tunnel = sshtunnel.SSHTunnelForwarder(
                (ssh_config.get('ssh_host'), int(ssh_config.get('ssh_port'))),
                ssh_username=ssh_config.get('ssh_username'),
                ssh_pkey=paramiko.RSAKey.from_private_key_file(ssh_config.get('ssh_rsa')),
                remote_bind_address=(db_config.get('host'), db_config.get('port')),
            )
            tunnel.start()
        except Exception as e:
            logger.error(e)
            raise Exception(f"<code class='text-red'>{str(e)}</code>")
        return tunnel


class DbSchema(DbConn):
    def __init__(self):
        super(DbSchema, self).__init__()
        self.columns = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']

    @staticmethod
    def run_sql_query(sql, conn, columns=None):
        try:
            return pd.read_sql_query(sql, conn, columns)
        except Exception as e:
            logger.error(e)
            return pd.DataFrame()

    def get_tables(self, conn: pymysql.connect):
        table_names = []
        if conn is not None:
            sql = "select table_name from information_schema.tables where table_schema='{}';"
            sql = sql.format(conn.db.decode('utf-8'))
            df = self.run_sql_query(sql, conn)
            if 'table_name' in df:
                table_name = 'table_name'
            else:
                table_name = 'TABLE_NAME'
            table_names = df[table_name].values.tolist()
        return table_names

    def get_structure_table(self, conn: pymysql.connect, table_name: str):
        sql = f'DESCRIBE `{table_name}`;'
        df = self.run_sql_query(sql, conn)
        field_names = []
        if df.shape[0] > 0:
            df['field_name'] = "Field: " + df['Field'].astype(str) + ", Type: " + df['Type'].astype(str) + ", Null: " + \
                               df['Null'].astype(str) + ", Key: " + df['Key'].astype(str) + ", Default: " + \
                               df['Default'].astype(str) + ", Extra: " + df['Extra'].astype(str)

            field_names = df['field_name'].values.tolist()
        return field_names


class DbFormatData:
    def __init__(self):
        pass

    @staticmethod
    def format_table(result: str):
        result = result.replace("class=\"diff\"", "class=\"diff table table-bordered table-hover\"")
        result = result.replace("nowrap=\"nowrap\"", "")

        return result


class DbCompare:
    def __init__(self):
        self.format_data = DbFormatData()
        self.differ = HtmlDiff()
        pass

    def compare(self, title, input1: list, input2: list, allow_format_table=True):
        input1.sort()
        input2.sort()
        result = self.differ.make_table(input1, input2, f'{title}', f'{title}')

        if allow_format_table:
            result = self.format_table(result)

        return result

    def format_table(self, result: str):
        result = self.format_data.format_table(result)
        return result

# if __name__ == "__main__":
#     c_ssh_config = {
#         'ssh_tunnel': True,
#         'ssh_host': '138.3.220.1281',
#         'ssh_port': 22,
#         'ssh_username': 'sonlnv',
#         'ssh_rsa': '/Users/trunghieu/Projects/Fsoft/RRK/RRK-tools/assets/rsa/id_rsa_sonlnv'
#     }
#     c_db_config_s = {
#         'host': '10.18.1.56',
#         'username': 'pos-web',
#         'password': 'LVM}LfGcO8Hr@9l3',
#         'db': 'pos_2',
#         'port': 3306,
#     }
#     c_db_config_d = {
#         'host': '10.18.1.56',
#         'username': 'pos-web',
#         'password': 'LVM}LfGcO8Hr@9l3',
#         'db': 'pos_4',
#         'port': 3306,
#     }
#     db_conn = DbSchema()
#     db_conn.conn_source, db_conn.tunnel_source = db_conn.mysql_connect(c_db_config_s, c_ssh_config)
#     db_conn.conn_destination, db_conn.tunnel_destination = db_conn.mysql_connect(c_db_config_d, c_ssh_config)
#     s_tables = db_conn.get_tables(db_conn.conn_source)
#     d_tables = db_conn.get_tables(db_conn.conn_destination)
#     df1df2 = s_tables.extend(d_tables)
#     print(s_tables)
#     print(d_tables)
#     # compare_data = DbCompare()
#     # compare_result = compare_data.compare('Tables', s_tables, d_tables)
#     #
#     # data_compares = [compare_result]
#     # for table_name in s_tables:
#     #     structure_table_s = db_conn.get_structure_table(db_conn.conn_source, table_name)
#     #     structure_table_d = db_conn.get_structure_table(db_conn.conn_destination, table_name)
#     #     compare_result_structure = compare_data.compare(table_name, structure_table_s, structure_table_d)
#     #     data_compares.append(compare_result_structure)
#     # print(data_compares)
