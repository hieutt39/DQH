from alf_fw import alf_assets

DEFAULT_INPUT = 'pdfs'


class IOUpload(object):
    def upload_file(self, file, folder=DEFAULT_INPUT):
        # file_name = '_'.join(file.name.split()).lower()
        folder_path = alf_assets.get_input_dir(folder)
        file_path = alf_assets.get_file_path(folder_path, file.name)
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return alf_assets.get_relative_path(file_path)

    def upload_files(self, files, folder=DEFAULT_INPUT):
        path_files = []
        for file in files:
            path_files.append(self.upload_file(file, folder))
        return path_files
