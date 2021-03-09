from parser import RedditParser

from load_format import load_to_server
from loading_data import load_page_data

link = "https://www.reddit.com/top/?t=month"
limit = 100
parser = RedditParser()
posts = load_page_data(parser, link, limit)
for post in posts:
    load_to_server(post)
