#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import shutil
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .io_json import IOJson


class IOAssets(IOJson):
    ASSET_DIR = 'assets'

    def __init__(self, config=None):
        super().__init__()
        self.config = {}
        if config is not None:
            self.config = config

        self._root_path = Path(self.config.project_root)
        self.config.set('ROOT_PATHS', 'project_root', self._root_path.as_posix())
        self._asset_root = Path(self.config.get('ROOT_PATHS', 'assets_root'))
        self._model_root = Path(self.config.get('ROOT_PATHS', 'model_root'))
        self.init_logging()
        self.clean_up()
        # self.get_model_dir()

    def get_assets_dir(self, *paths, is_rel=0) -> Path:
        """
        :param paths: sub dir of assets
        :param is_rel:
            0: Absolute path
            1: Relative path
        :return: Path
        """
        sub_dir = self._asset_root.joinpath(self.ASSET_DIR, *paths)
        if not sub_dir.exists():
            sub_dir.mkdir(parents=True)

        if is_rel:
            root_dir = Path(self.ASSET_DIR)
            sub_dir = root_dir.joinpath(*paths)

        return sub_dir

    def get_model_dir(self, *paths, is_rel=0) -> Path:
        """
        :param paths: sub dir of assets
        :param is_rel:
            0: Absolute path
            1: Relative path
        :return: Path
        """
        sub_dir = self._model_root.joinpath(self.config.get_model('root_dir'), *paths)
        if not sub_dir.exists():
            sub_dir.mkdir(parents=True)

        if is_rel:
            root_dir = Path(self.config.get_model('root_dir'))
            sub_dir = root_dir.joinpath(*paths)

        return sub_dir

    def get_data_dir(self, *sub_dirs, is_rel=0) -> Path:
        data_dir = self.config.get_data('root_dir')
        sub_dir = self.get_assets_dir(data_dir, *sub_dirs, is_rel=is_rel)
        return sub_dir

    def get_input_dir(self, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.config.get_data('input_dir')
        return self.get_data_dir(sub_dir, *sub_dirs, is_rel=is_rel)

    def get_output_dir(self, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.config.get_data('output_dir')
        return self.get_data_dir(sub_dir, *sub_dirs, is_rel=is_rel)

    def get_cache_dir(self, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.config.get_data('cache_dir')
        return self.get_data_dir(sub_dir, *sub_dirs, is_rel=is_rel)

    def get_report_dir(self, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.config.get_data('report_dir')
        return self.get_data_dir(sub_dir, *sub_dirs, is_rel=is_rel)

    def get_logging_dir(self, *sub_dirs, is_rel=0) -> Path:
        data_dir = self.config.get_logging('root_dir')
        sub_dir = self.get_assets_dir(data_dir, *sub_dirs, is_rel=is_rel)
        return sub_dir

    @staticmethod
    def get_file_path(path, *paths):
        file = Path(*paths)
        file = file.joinpath(path)
        return file

    def get_model_path(self, file_path, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.get_model_dir(*sub_dirs, is_rel=is_rel)
        file_path = sub_dir.joinpath(file_path)
        return file_path

    def get_input_path(self, file_path, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.get_input_dir(*sub_dirs, is_rel=is_rel)
        file_path = sub_dir.joinpath(file_path)
        return file_path

    def get_output_path(self, file_path, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.get_output_dir(*sub_dirs, is_rel=is_rel)
        file_path = sub_dir.joinpath(file_path)
        return file_path

    def get_cache_path(self, file_path, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.get_cache_dir(*sub_dirs, is_rel=is_rel)
        file_path = sub_dir.joinpath(file_path)
        return file_path

    def get_report_path(self, file_path, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.get_report_dir(*sub_dirs, is_rel=is_rel)
        file_path = sub_dir.joinpath(file_path)
        return file_path

    def get_logging_path(self, file_path, *sub_dirs, is_rel=0) -> Path:
        sub_dir = self.get_logging_dir(*sub_dirs, is_rel=is_rel)
        file_path = sub_dir.joinpath(file_path)
        return file_path

    def scan_dir(self, input_dir: str):
        folders = {}
        for entry in os.scandir(self.get_assets_dir(input_dir)):
            if entry.is_dir():
                folders[entry.name] = entry
        # for dirName, subdirList, fileList in os.walk(self.get_assets_dir(input_dir)):
        #     folders.append(dirName.parts)

        return folders

    def scan_files(self, input_dir: str, exts=['.*']):
        files = []
        for data_path in Path(self.get_assets_dir(input_dir)).glob('**/*'):
            if '.*' not in exts:
                if data_path.suffix.lower() not in exts:
                    continue
            elif data_path.is_dir():
                continue

            files.append(data_path)

        return files

    def clean_up(self):
        if int(self.config.get_data('clean_up')):
            shutil.rmtree(self.get_data_dir(), ignore_errors=True)

    def init_logging(self):
        if self.config.get_logging('filename') != '':
            filename = self.get_logging_path(self.config.get_logging('filename'))
            logging.basicConfig(handlers=[RotatingFileHandler(filename=filename.as_posix(), mode='w',
                                                              maxBytes=512, backupCount=4)],
                                level=eval('logging.{}'.format(self.config.get_logging('level'))),
                                format=self.config.get_logging('format'),
                                datefmt=self.config.get_logging('datefmt'),
                                )
        else:
            logging.basicConfig(level=eval('logging.{}'.format(self.config.get_logging('level'))),
                                format=self.config.get_logging('format'),
                                datefmt=self.config.get_logging('datefmt'),
                                )
