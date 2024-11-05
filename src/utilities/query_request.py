from os.path import splitext


class QueryRequest:
    request = None

    def __init__(self, request):
        self.request = request

    def get_data(self, method=None):
        if self.request.method == 'POST':
            query_params = self.request.data_log
        else:
            query_params = self.request.query_params

        return query_params

    def get_scope(self):
        items = {}
        for scope in self.request._request.scope:
            items[scope] = {}
            if scope == 'headers':
                for header in self.request._request.scope[scope]:
                    key, value = header
                    items[scope][key.decode('ascii')] = value.decode('ascii')

        return items

    def validate_require(self, name, query_params, is_require, min_lenght=None, max_lenght=None):
        if is_require:
            if name not in query_params:
                return "'{}' is required".format(name)

        if min_lenght is not None:
            value = query_params.get(name)
            if len(value) < int(min_lenght):
                return "'{}' Minimum of {} characters".format(name, min_lenght)

        if max_lenght is not None:
            value = query_params.get(name)
            if len(value) > int(max_lenght):
                return "'{}' Maximum of {} characters".format(name, max_lenght)

        return None

    def validate_extension(self, file_path: str, exts: []):
        name, ext = splitext(str(file_path))
        # if imghdr.what(file_path) not in exts:
        if ext not in exts:
            return False

        return True

    def get_number(self, name, default=0, is_require=False, min_lenght=None, max_lenght=None):
        query_params = self.get_data(self.request.method)
        error = self.validate_require(name, query_params, is_require, min_lenght, max_lenght)
        if error is None:
            value = query_params.get(name)
            if value is not None:
                return int(value)
            else:
                return default

        else:
            return default

    def get_string(self, name, default='', is_require=False, min_lenght=None, max_lenght=None):
        query_params = self.get_data()
        error = self.validate_require(name, query_params, is_require, min_lenght, max_lenght)
        if error is not None:
            return default
        else:
            value = query_params.get(name)
            return value

    def get_filetype(self, name, method='GET', is_require=False, default=''):
        query_params = self.get_data(method)
        error = self.validate_require(name, query_params, is_require)
        if error is not None:
            return default, 'E00012'
        else:
            value = query_params.get(name)
            if value in ['01', '02']:
                return value, None
            else:
                return value, 'E00001'
                # return value, "The value of '{}' must be 01 or 02".format(name)

    def get_file(self, name, method='POST', is_require=True, exts=['.jpg', '.jpeg', '.png', '.tif']):
        query_params = self.get_data(method)
        print('params', query_params)
        error = self.validate_require(name, query_params, is_require)
        if error is not None:
            return None, 'E00012'
        else:
            value = query_params.get(name)
            if self.validate_extension(value, exts):
                return value, None
            else:
                return value, 'E00001'
                # return value, "The extension of '{}' must be {}".format(name, ' or '.join(exts))
