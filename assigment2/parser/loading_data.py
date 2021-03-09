import json
import re
import time
from datetime import datetime, timedelta

import requests as req
import uuid1
from bs4 import BeautifulSoup

from constants import ElementsIdConstants
from utils import Logger

logger_page = Logger('page logger')
logger_page.set_logger_level('INFO')
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def load_page_data(parser, link, limit):
    posts = []
    parser.driver_get_link(link)
    logger_page.logger_info_message(f'get page link {link}')
    time.sleep(1)
    offset = 0
    while len(posts) < 30:
        elements = parser.find_elements_by_css_selector(
            ElementsIdConstants.POST_TAG_CSS_SELECTOR
        )
        users = parser.find_elements_by_css_selector(
            ElementsIdConstants.USER_TAG_CSS_SELECTOR
        )
        elements_links = parser.get_links(elements)
        users_links = parser.get_links(users)
        logger_page.logger_info_message('find all posts and their links')
        logger_page.logger_info_message('find all users and their links')
        usernames = [users_links[i][28:-1] for i in range(len(users_links))]
        for el in range(offset, len(elements_links) - 1):
            if len(posts) == 30:
                break
            user = users_links[el]
            post_page = req.get(elements_links[el], headers=HEADERS)
            user_page = req.get(user, headers=HEADERS)
            if user_page.status_code == 502 or post_page.status_code == 502:
                continue
            soup_post = BeautifulSoup(post_page.text, 'html.parser')
            soup_user = BeautifulSoup(user_page.text, 'html.parser')
            logger_page.logger_info_message(
                'user data received')
            logger_page.logger_info_message('post data received')
            post_karma, comment_karma = get_tooltip(soup_user, parser)
            try:
                reddit_post = {
                    **post_data(soup_post),
                    **user_page_data(soup_user),
                    'postUrl': elements_links[el],
                    'username': usernames[el],
                    'postKarma': post_karma,
                    'commentKarma': comment_karma,
                    'uniqueId': str(uuid1.uuid1())
                }
            except Exception:
                continue
            posts.append(reddit_post)
            logger_page.logger_info_message(f'the link #{el + 1} are valid')
        parser.scroll()
        offset += len(elements_links) - offset
    parser.close()
    return posts


def get_text(soup_element):
    if soup_element:
        return soup_element.text


def get_user_day(day):
    return datetime.strptime(day, '%B %d, %Y').strftime('%Y-%m-%d')


def user_page_data(soup):
    user_karma = get_text(soup.find(
        'span',
        id=ElementsIdConstants.USER_KARMA_TAG_ID
    )).split(',')
    user_day = get_text(soup.find(
        'span',
        id=ElementsIdConstants.USER_CAKE_DAY_TAG_ID
    ))
    if user_day is None or user_karma is None:
        raise Exception("Ivalid data")
    return {
        'userKarma': int(
            ''.join(map(str, user_karma))),
        'userCakeDay': get_user_day(user_day)
    }


def get_data(days):
    if days is not None:
        days_in_minutes = timedelta(days=int(days.split()[0]))
        return (datetime.today() - days_in_minutes).strftime('%Y-%m-%d')
    return ''


def reformat(data):
    return int(''.join(map(str, data.split('k')[0].split('.'))))


def post_data(soup):
    votes_number = get_text(soup.find(
        'div',
        class_=ElementsIdConstants.NUMBER_OF_VOTES_TAG_CLASS
    ))
    post = get_text(soup.find(
        'a',
        class_=ElementsIdConstants.POST_DATE_TAG_CLASS
    ))
    comments = get_text(soup.find('div').find(
        'span',
        class_=ElementsIdConstants.NUMBER_OF_COMMENTS_TAG_CLASS)
    )
    if votes_number is None or post is None or comments is None:
        raise Exception("Ivalid data")
    return {
        'numberOfVotes': reformat(votes_number),
        'postDate': get_data(post),
        'postCategory': get_text(soup.find(
            'span',
            class_=ElementsIdConstants.POST_CATEGORY_TAG_CLASS
        ))[2:],
        'numberOfComments': reformat(comments) * 100
    }


def get_tooltip(soup, parser):
    karma = soup.find('script', id='data').string
    json_text = re.search(r'window.___r = ({.*?})\s*;',
                          karma, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    flat_dict = json_treating(data)
    return flat_dict['postKarma'], flat_dict['commentKarma']


def json_treating(json_data):
    flat_dict = {}
    if isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, (list, dict)):
                flat_dict.update(json_treating(item))
        return flat_dict
    for key, value in json_data.items():
        if isinstance(value, (list, dict)):
            flat_dict.update(json_treating(value))
        else:
            flat_dict[key] = value
    return flat_dict
