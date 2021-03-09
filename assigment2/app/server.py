import http.server
import json
import re
from collections import namedtuple
from urllib.parse import urlparse

from adapters.database.mongo_db.mongoDB import MongoDB
from adapters.database.postgres_db.postgres import PostgresqlDB
from config import DBConfig
from domain_app.url_view import URLView

DATABASE = {'postgresql': PostgresqlDB, 'mongodb': MongoDB}

URL_DICT = {
    re.compile('/posts/'): {
        'GET': 'get_data',
        'POST': 'add_post'
    },
    re.compile(r'/posts/(.+)/'): {
        'GET': 'get_post',
        'PUT': 'update_post',
        'DELETE': 'remove_post'
    }
}

def get_url(requestline):
    char_find=requestline.find('/')

def find_matches(d, item):
    for k in d.keys():
        if re.fullmatch(k, item):
            return d[k]


ResponseStatus = namedtuple("ResponseStatus",
                            ["response", "ContentType", "data"])


class MyServerHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.BaseHTTPRequestHandler.end_headers(self)

    def send_headers(self, response_status, response_content):
        self.send_response(response_status)
        self.send_header("Content-type", response_content)
        self.end_headers()

    def perform_requests(self, method, url=None, args=None, query=None):
        try:
            func_name = find_matches(URL_DICT, url)[method]
        except KeyError:
            self.send_headers(404, 'application/json')
            return
        config = DBConfig()
        url_view = URLView(
            DATABASE[str(config.configs().database)[8:]],
            config.configs()
        )
        func = getattr(url_view, func_name)
        response = func(url=url, args=args, query=query)
        self.send_headers(response.response, response.ContentType)
        self.wfile.write(json.dumps(response.data, default=str).encode())

    def do_GET(self):
        query = urlparse(self.path).query
        query_components = {}
        if len(query) > 1:
            query_components = dict(qc.split("=") for qc in query.split("&"))
            self.path = self.path[:self.path.find("?")]
        print(self.path)
        return self.perform_requests(
            'GET',
            url=self.path,
            query=query_components)

    def do_POST(self):
        headers = self.headers['Content-Length']
        raw_body = self.rfile.read(int(headers)).decode('utf-8')
        post_args = json.loads(raw_body)
        return self.perform_requests('POST', url=self.path, args=post_args)

    def do_PUT(self):
        headers = self.headers['Content-Length']
        raw_body = self.rfile.read(int(headers)).decode('utf-8')
        post_args = json.loads(raw_body)
        return self.perform_requests('PUT', url=self.path, args=post_args)

    def do_DELETE(self):
        return self.perform_requests('DELETE', url=self.path)


PORT = 8087
server_address = ('localhost', PORT)
server = http.server.HTTPServer(server_address, MyServerHandler,)
server.serve_forever()
