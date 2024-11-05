import os
import uuid
import json
import pandas as pd
from difflib import Differ, HtmlDiff, unified_diff, SequenceMatcher
from collections import Counter
from .sync_message import SyncMessage, logger
from src.utilities.postman_py.core import PostPython
from src.utilities.io_json import IOJson


class CompareApiService(SyncMessage, IOJson):
    def __init__(self):
        super(CompareApiService, self).__init__()
        self.file_path = os.path.join(self.assets, 'collections')
        self.keys = ['Source', 'Destination']
        self.uid = uuid.uuid4()

    def process(self):
        return self.exec_process()

    def response_process(self, response):
        print("response", response)
        df = pd.DataFrame([{'response': response.text}])
        try:
            data = response.json()
        except:
            data = response.text

        data = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False).split("\n")

        # Save the data received from Api to Database
        # self.write_json({'response': data_source}, f'{json_path}/{api_name}.source.json')

        return df, data

    def exec_process(self, collection, environment_source={}, environment_destination={}):
        # collection_file = f'{self.file_path}/SOM.postman_collection.json'
        collection_file = f'{collection}'
        # Get collection name
        collection_name = self.get_collection_name(collection_file)
        json_path = self.get_folder(self.file_path, collection_name)

        # Prepare the data from Collections for call API
        runner_source = self.get_runner(collection_file, environment_source)
        runner_destination = self.get_runner(collection_file, environment_destination)
        collection_requests = runner_source.get_collection_request()

        df_diff_all = {}
        diff_analysis = pd.DataFrame()
        for collection_request in collection_requests:
            for collection_req in collection_request:
                # Get API name from Collections while scan per item
                api_name = self.get_api_name(collection_req)
                collection_source = eval(collection_req.replace("post_python", "runner_source"))
                collection_destination = eval(collection_req.replace("post_python", "runner_destination"))

                df_source, response_source = self.response_process(collection_source)
                df_destination, response_destination = self.response_process(collection_destination)
                differ = HtmlDiff()
                compare_result = differ.make_table(response_source, response_destination, 'Source (response)',
                                                   'Destination (response)')
                compare_result = compare_result.replace("class=\"diff\"",
                                                        "class=\"diff table table-bordered table-hover\"")
                compare_result = compare_result.replace("nowrap=\"nowrap\"", "")

                try:
                    df_diff = self.compare_by(df_source, df_destination, columns=list(df_source.columns))
                    diff_analysis = pd.concat(
                        [diff_analysis, self.diff_analysis(df_source, df_destination, df_diff, api_name)],
                        ignore_index=True)

                    df_diff_all.update({
                        api_name: {
                            'compare_result': compare_result,
                            'data': df_diff,
                            'result': 'Passed' if abs(df_diff[self.keys[0]].shape[0]) == 0 else 'Failed',
                        }
                    })
                except Exception as e:
                    df_diff_all.update({
                        api_name: {
                            'compare_result': compare_result,
                            'data': pd.DataFrame(),
                            'result': 'Failed',
                        }
                    })
                    logger.error(e)

        self.send_message(
            diff_analysis.to_html(
                classes="table table-bordered table-hover dataTable table-striped",
                escape=False
            ))
        return {'df_diff': df_diff_all, 'diff_analysis': diff_analysis}

    @staticmethod
    def get_runner(collection_file: str, environment: dict):
        runner = PostPython(collection_file, True)
        runner.environments.update(environment)
        return runner

    def diff_analysis(self, df1, df2, df_diff, column_name=None):
        """
        Parameters
        ----------
        :param df1
        :param df2
        :param df_diff
        :param column_name

        Returns
        -------

        """
        try:
            url = f'/tools/api/detail?uid={self.uid}&api_name={column_name}'
            column_name_url = f'<a href="{url}" target="_blank_">{column_name}</a>'
            result = '<span class="badge bg-green">Passed</span>' if abs(
                df_diff[self.keys[0]].shape[0]) == 0 else '<span class="badge bg-red">Failed</span>'
            df = pd.DataFrame(data=[
                [
                    column_name_url, df1.shape[0], df2.shape[0],
                    # abs(df_diff[self.keys[0]].shape[0])
                    result
                ],
            ], columns=['Api name', self.keys[0], self.keys[1], 'Result'])
        except Exception as e:
            df = pd.DataFrame(data=[
                [
                    column_name, -1, -1, '<span class="badge bg-red">Failed</span>'
                ],
            ], columns=['Api name', self.keys[0], self.keys[1], 'Result'])
            logger.error(e)
        return df

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
        return pd.concat([df1df2, df2df1], axis=1, keys=self.keys)

    @staticmethod
    def get_collection_name(collection_path):
        collection_name = collection_path.split("/")[2].replace(".json", "")
        return collection_name

    @staticmethod
    def get_api_name(collection_req):
        api_name = collection_req.split(".")[2].replace("()", "")
        return api_name

    def get_json_path(self, folder):
        json_path = self.get_folder(self.file_path, folder)
        return json_path

    def sorting(self, item):
        if isinstance(item, dict):
            return sorted((key, self.sorting(values)) for key, values in item.items())
        if isinstance(item, list):
            return sorted(self.sorting(x) for x in item)
        else:
            return item

    def exec_process_test(self, collection, environment_source={}, environment_destination={}):
        collection_file = f'{collection}'
        # Get collection name
        collection_name = self.get_collection_name(collection_file)
        json_path = self.get_folder(self.file_path, collection_name)

        # Prepare the data from Collections for call API
        runner_source = self.get_runner(collection_file, environment_source)
        collection_requests = runner_source.get_collection_request()

        df_diff_all = {}
        diff_analysis = pd.DataFrame()
        for collection_request in collection_requests:
            for collection_req in collection_request:
                # Get API name from Collections while scan per item
                api_name = self.get_api_name(collection_req)
                data = self.read_json(f'{json_path}/{api_name}.source.json')
                df_source = pd.DataFrame(data)
                # data.append(data[0])
                # data.append(data[1])
                # data.append(data[2])
                df_destination = pd.DataFrame(data)

                try:
                    df_diff = self.compare_by(df_source, df_destination, columns=list(df_source.columns))
                    diff_analysis = pd.concat(
                        [diff_analysis, self.diff_analysis(df_source, df_destination, df_diff, api_name)],
                        ignore_index=True)
                    df_diff_all.update({
                        api_name: {
                            'data': df_diff,
                            'result': 'Passed' if abs(df_diff[self.keys[0]].shape[0]) == 0 else 'Failed',
                        }
                    })
                except Exception as e:
                    df_diff_all.update({
                        api_name: {
                            'data': pd.DataFrame(),
                            'result': 'Failed',
                        }
                    })
                    logger.error(e)
        self.send_message(
            diff_analysis.to_html(
                classes="table table-bordered table-hover dataTable table-striped",
                escape=False
            )
        )
        return {'df_diff': df_diff_all, 'diff_analysis': diff_analysis}
