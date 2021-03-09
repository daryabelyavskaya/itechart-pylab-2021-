import json

import requests

from utils import Logger

logger_page = Logger('load to server logger')
logger_page.set_logger_level('INFO')


def load_to_txt(posts):
    return json.dumps(posts, ident=None)


def load_to_server(post):
    try:
        requests.post(
            'http://localhost:8087/posts/',
            json=post
        )
        logger_page.logger_info_message('load post to server')
    except ConnectionError:
        logger_page.logger_info_message('cant load post to server')
