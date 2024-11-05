#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Andrew <hieutt39@fpt.com>"

import os
import shutil
import json
import codecs
from datetime import datetime


class IOJson:
    @staticmethod
    def get_folder(assets, dir_name, by_timestamp=False, mode=0o777):
        """
        Parameters
        ----------
        dir_name
        assets
        by_timestamp
        mode
        Returns
        -------
        """
        dir_path = os.path.join(assets, dir_name)
        if by_timestamp:
            now = datetime.now()
            dir_name = f'{dir_name}-{int(datetime.timestamp(now))}'
            dir_path = os.path.join(assets, dir_name)
        # else:
        #     shutil.rmtree(dir_path, True)

        os.makedirs(dir_path, mode=mode, exist_ok=True)
        return dir_path

    @staticmethod
    def encode(obj_dict={}, ensure_ascii=True, indent=4, sort_keys=False, allow_nan=True):
        obj_str = json.dumps(obj_dict, indent=indent,
                             sort_keys=sort_keys,
                             ensure_ascii=ensure_ascii,
                             allow_nan=allow_nan,
                             default=str)
        return obj_str

    @staticmethod
    def decode(obj_str):
        if isinstance(obj_str, str):
            obj_dict = json.loads(obj_str)
            return obj_dict
        else:
            return json.loads("{}")

    @staticmethod
    def read_json(file_path, mode='r', encoding='utf8'):
        """
        Load json file and decode json to Object too
        """
        file_data = codecs.open(file_path, mode=mode, encoding=encoding)
        data = json.load(file_data)
        file_data.close()
        return data

    def write_json(self, data: dict, file_path: str, ensure_ascii=True, mode='w', encoding='utf8'):
        """
        Write json file
        Parameters
        ----------
        :param data: Dict type data
        :param file_path: json file path
        :param encoding
        :param mode
        :param ensure_ascii
        :return:
        """
        if isinstance(data, dict) or isinstance(data, list):
            with codecs.open(file_path, mode=mode, encoding=encoding) as f:
                data = self.encode(data,
                                   indent=4,
                                   sort_keys=False,
                                   ensure_ascii=ensure_ascii,
                                   allow_nan=True)
                f.write(data)

        else:
            print('Type of Data must is Dict or List')
