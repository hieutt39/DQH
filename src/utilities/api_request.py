import requests


class ApiRequest(object):
    BASE_URL = ""
    USER_AGENT = ""

    def __init__(
            self,
            access_token=None,
            timeout=None,
            version=None,
            proxies=None,
            session=None,
            auth=None
    ):
        self.access_token = access_token
        self.timeout = timeout
        self.proxies = proxies
        self.session = session or requests.Session()
        self.app_secret_hmac = None
        self.version = version
        self.auth = auth

    def get_version(self):
        return str(self.version)

    def request(
            self, path, args=None, post_args=None, files=None, method=None, headers=None
    ):
        if headers is None:
            headers = {
                'Content-type': 'application/json; charset=utf-8',
            }
        if args is None:
            args = dict()
        if post_args is not None and method is None:
            method = "POST"

        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'

        try:
            response = self.session.request(
                method=method or "GET",
                url=self.BASE_URL + path,
                timeout=self.timeout,
                params=args,
                data=post_args,
                proxies=self.proxies,
                files=files,
                headers=headers,
                auth=self.auth
            )
        except requests.HTTPError as e:
            raise RuntimeError(response.text)

        result = {"status_code": response.status_code, "message": response.text, "data_log": []}
        headers = response.headers
        if not response.ok:
            raise RuntimeError(response.text)

        if "json" in headers["content-type"]:
            result["data_log"] = response.json()
        elif "image/" in headers["content-type"]:
            mimetype = headers["content-type"]
            result = {
                "data_log": response.content,
                "mime-type": mimetype,
                "url": response.url,
            }

        return result
