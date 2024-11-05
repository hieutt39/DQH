import pandas as pd
import json
from datetime import datetime
from collections import Counter
from src.utilities.files.files import *
from .db_conn import DbConn, logger
import numpy as np


class CompareDataService(DbConn):
    def __init__(self, source_info=None, destination_info=None):
        super(CompareDataService, self).__init__(source_info, destination_info)
        self.file_path = self.get_folder('compare/data', False)

    def compare_by(self, df1, df2, sort_field_names=None, on=None, columns=[]):
        """
        Parameters
        ----------
        df1
        df2
        sort_field_names
        on
        columns

        Returns
        -------

        """
        # df1 = df1.dropna().astype(str)
        # df2 = df2.dropna().astype(str)
        # df1 = df1.fillna(np.nan)
        # df2 = df2.fillna(np.nan)
        # df1 = df1.replace(to_replace=[None], value='', inplace=True)
        # df2 = df2.replace(to_replace=[None], value='', inplace=True)
        df1 = df1.astype(str)
        df2 = df2.astype(str)
        if len(columns) > 0:
            df1 = df1.loc[:, df1.columns.isin(columns)]
            df2 = df2.loc[:, df2.columns.isin(columns)]

        on = on if on else columns
        if sort_field_names is not None:
            df1on = df1[on].sort_values(by=sort_field_names, ascending=True, na_position='first')
            df2on = df2[on].sort_values(by=sort_field_names, ascending=True, na_position='first')
        else:
            df1on = df1[on]
            df2on = df2[on]

        c1 = Counter(df1on.apply(tuple, 'columns'))
        c2 = Counter(df2on.apply(tuple, 'columns'))
        c1c2 = c1 - c2
        c2c1 = c2 - c1
        df1on_df2on = pd.DataFrame(list(c1c2.elements()), columns=on).astype(str)
        df2on_df1on = pd.DataFrame(list(c2c1.elements()), columns=on).astype(str)
        df1df2 = df1.merge(df1on_df2on).drop_duplicates(subset=on)
        df2df1 = df2.merge(df2on_df1on).drop_duplicates(subset=on)
        # df2df1 = df2df1.dropna()
        # df1df2 = df1df2.dropna()
        return pd.concat([df1df2, df2df1], axis=1, keys=self.keys)

    def diff_analysis(self, df1, df2, df_diff, table_name=None):
        """
        Parameters
        ----------
        :param df1
        :param df2
        :param df_diff
        :param table_name

        Returns
        -------

        """
        try:
            result = '<span class="badge bg-green">Pass</span>' if abs(
                df_diff[self.keys[0]].shape[0]) == 0 else '<span class="badge bg-red">Failed</span>'
            df = pd.DataFrame(data=[
                [
                    table_name, df1.shape[0], df2.shape[0],
                    result
                ],
            ], columns=['Table name', self.keys[0], self.keys[1], 'Result'])
        except Exception as e:
            df = pd.DataFrame(data=[
                [
                    table_name, -1, -1, '<span class="badge bg-red">Failed</span>'
                ],
            ], columns=['Table name', self.keys[0], self.keys[1], 'Result'])

        return df

    def process(self):
        table_main_names = self.get_tables(self.database_names['source'], self.conn_source)
        table_second_names = self.get_tables(self.database_names['destination'], self.conn_destination)
        return self.exec_process(table_main_names, table_second_names, to_exec=True)

    def exec_process(self, table_main_names, table_second_names, to_exec=True):
        tables = []
        tables.extend(table_main_names)
        tables.extend(table_second_names)
        analysis_df = pd.DataFrame()
        with pd.ExcelWriter(f'{self.file_path}/diff.xlsx', engine="openpyxl") as writer_diff:
            for table_name in list(dict.fromkeys(tables)):
                sql = f'SELECT * FROM {table_name};'
                df_main = self.run_query(sql, self.conn_source)
                df_second = self.run_query(sql, self.conn_destination)
                column_names = []
                column_names.extend(df_main.columns.values)
                column_names.extend(df_second.columns.values)
                column_names = list(dict.fromkeys(column_names))

                if df_second.empty:
                    df_second = pd.DataFrame(columns=column_names)
                elif df_main.empty:
                    df_main = pd.DataFrame(columns=column_names)

                logger.info('Compare: START')
                try:
                    df_diff = self.compare_by(df_main, df_second, columns=column_names)
                except:
                    df_diff = pd.DataFrame(columns=column_names)

                logger.info('Compare: END')

                logger.info('--START: export data to files')
                # if df_diff is not None:
                if len(table_name) > 31:
                    table_name = table_name[:31]
                analysis_df = pd.concat([analysis_df, self.diff_analysis(df_main, df_second, df_diff, table_name)],
                                        ignore_index=1)
                df_diff.to_excel(writer_diff, sheet_name=table_name)

                logger.info('--FINISH: Export data to files')
            analysis_df.to_excel(writer_diff, sheet_name="Summary")
            self.send_message(analysis_df.to_html(
                classes="table table-bordered table-hover dataTable table-striped",
                escape=False,
            ))

        return analysis_df
