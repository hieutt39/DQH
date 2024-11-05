import os
import shutil
from os import path
import imghdr
from django.conf import settings


class LibFile:
    def get_abs_path(self, file_path: str):
        file_path = file_path.replace('public', '')
        file_path = file_path.lstrip('/')
        ab_media_root = path.abspath(settings.MEDIA_ROOT)
        return path.join(ab_media_root, file_path)

    # dir is not keyword
    def make_dir(self, whatever):
        try:
            os.makedirs(whatever)
            return True
        except OSError as ex:
            print("Make dir error", ex)
            return False

    def copy_tree(self, src, dst):
        try:
            shutil.copytree(src, dst)
            return True
        except OSError as ex:
            print("Copy tree error", ex)
            return False

    def copy_file(self, src, dst):
        try:
            shutil.copy2(src, dst)
            return True
        except OSError as ex:
            print("copy file error", ex)
            return False

    def rm_tree(self, src):
        try:
            shutil.rmtree(src)
            return True
        except OSError as ex:
            print("Remove Tree error", ex)
            return False

    def rm_file(self, src):
        try:
            os.remove(src)
            return True
        except OSError as ex:  ## if failed, report it back to the user ##
            print("Remove file error", ex)
            return False

    def validate_extension(self, file_path: str, exts: []):
        if imghdr.what(file_path) not in exts:
            return False

        return True

    def upload_file(self, file, folder='images'):
        # if self.validate_extension(file):
        file_name = '_'.join(file.name.split()).lower()
        folder_path = self.get_abs_path(folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        destination = open(path.join(folder_path, file_name), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return "{}/{}".format(folder, file_name)

    def upload_files(self, files, folder='tool'):
        path_files = []
        for file in files:
            path_files.append(self.upload_file(file, folder))
        return path_files

lib_file = LibFile()