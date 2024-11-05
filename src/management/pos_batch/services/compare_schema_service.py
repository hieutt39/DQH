import pandas as pd
from collections import Counter
from .db_conn import DbConn, logger
from time import sleep


class CompareSchemaService(DbConn):
    def __init__(self, source_info=None, destination_info=None):
        super(CompareSchemaService, self).__init__(source_info, destination_info)
        self.filter_field_name = 'Table'
        self.file_path = self.get_folder('compare/schema', False)

    def process(self):
        table_main_names = self.get_tables(self.database_names['source'], self.conn_source)
        table_second_names = self.get_tables(self.database_names['destination'], self.conn_destination)
        return self.exec_process(table_main_names, table_second_names, to_exec=True)

    def exec_process(self, table_main_names, table_second_names, to_exec=True):
        """
        Compare schema database
        Returns
        -------

        """
        df_main = pd.DataFrame()
        df_second = pd.DataFrame()
        # Get all structure of main schema
        for table_name in table_main_names:
            df = self.get_structure(table_name, self.conn_source)
            df.insert(loc=0, column=self.filter_field_name, value=table_name)
            df_main = pd.concat([df_main, df])
        # Get all structure of second schema
        for table_name in table_second_names:
            df = self.get_structure(table_name, self.conn_destination)
            df.insert(loc=0, column=self.filter_field_name, value=table_name)
            df_second = pd.concat([df_second, df])

        df_summary = pd.DataFrame(data=[
            self.keys,
            [df_main.shape[0], df_second.shape[0]],
        ])

        df_data = pd.concat([
            df_main.loc[df_main[self.filter_field_name].isin(table_main_names)].reset_index(drop=True),
            df_second.loc[df_second[self.filter_field_name].isin(table_second_names)].reset_index(drop=True),
        ], axis='columns', keys=self.keys)
        df_data = df_data.applymap(str).reset_index(drop=True)

        table_names = []
        table_names.extend(table_main_names)
        table_names.extend(table_second_names)
        table_names = list(dict.fromkeys(table_names))

        df_diff = self.compare_by(
            df_main,
            df_second,
            columns=table_names
        )
        if to_exec:
            with pd.ExcelWriter(f'{self.file_path}/schema.xlsx', engine="openpyxl") as writer:
                df_summary.to_excel(writer, sheet_name='Summary')
                df_data.to_excel(writer, sheet_name='Mapping')
                df_diff.to_excel(writer, sheet_name='Diff')
        # self.send_message(df_summary.to_html(classes="table table-bordered table-hover dataTable"))
        self.send_message(df_diff.to_html(
            classes="table table-bordered table-hover dataTable table-striped",
            escape=False,
        ))
        # self.send_message(df_diff.to_html(classes="table table-bordered table-hover dataTable"))
        return df_diff

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
        df1 = df1.astype(str)
        df2 = df2.astype(str)
        if len(columns) > 0:
            df1 = df1.loc[df1[self.filter_field_name].isin(columns)].reset_index(drop=True)
            df2 = df2.loc[df2[self.filter_field_name].isin(columns)].reset_index(drop=True)

        on = on if on else df1.columns
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
        df1ondf2on = pd.DataFrame(list(c1c2.elements()), columns=on).astype(str)
        df2ondf1on = pd.DataFrame(list(c2c1.elements()), columns=on).astype(str)
        df1df2 = df1.merge(df1ondf2on).drop_duplicates(subset=on)
        df2df1 = df2.merge(df2ondf1on).drop_duplicates(subset=on)

        return pd.concat([df1df2, df2df1], axis=1, keys=self.keys)
