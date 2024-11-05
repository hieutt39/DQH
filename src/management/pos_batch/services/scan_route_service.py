import re
import json
from .db_conn import DbConn, logger
from django.conf import settings
from src.utilities.files.files import scan_files, clean_up, mkdir


class ScanRouteService:
    def __init__(self):
        super(ScanRouteService, self).__init__()

    def scan(self):
        php_path = '/Users/trunghieu/Projects/Fsoft/RRK/pos-pos-oci/config/routes.php'
        routes = {
            'redirect': [],
            'connect': [],
            'scope': [],
            'get': [],
        }
        with open(php_path) as data_file:
            lines = data_file.readlines()
            count = 0
            # Strips the newline character
            for line in lines:
                count += 1
                # print("Line{}: {}".format(count, line.strip()))
                connect_r = self.find_route_by('->connect', line)
                scope_r = self.find_route_by('->scope', line)
                get_r = self.find_route_by('->get', line)
                redirect_r = self.find_route_by('->redirect', line)
                if connect_r is not None:
                    routes['connect'].append(connect_r)
                if scope_r is not None:
                    routes['scope'].append(scope_r)
                if get_r is not None:
                    routes['get'].append(get_r)
                if redirect_r is not None:
                    routes['redirect'].append(redirect_r)
        print(json.dumps(routes, indent=2))
    @staticmethod
    def find_route_by(func, line_code):
        rs = None
        routes = re.findall(rf"{func}\(\'\/*.*\',", line_code)
        for route in routes:
            route = route.replace(f"{func}('", "")
            route = route.replace("',", "")
            rs = route

        return rs
