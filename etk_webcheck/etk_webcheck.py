import requests

class WebCheck:
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_FORBIDDEN = 403
    HTTP_NOT_FOUND = 404
    HTTP_METHOD_NOT_ALLOWED = 405
    HTTP_INTERNAL_SERVER_ERROR = 500
    HTTP_SERVICE_UNAVAILABLE = 503

    def __init__(self):
        self.urls = []

    def add_url(self, url):
        self.urls.append(url)

    def check_url(self, url):
        try:
            response = requests.get(url)
            return (url, response.status_code)
        except requests.exceptions.RequestException as e:
            return (url, str(e))

    def check_urls(self):
        results = []
        for url in self.urls:
            results.append(self.check_url(url))
        return results