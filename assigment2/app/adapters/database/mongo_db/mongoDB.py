from datetime import datetime

from adapters.database.db_base import AbstractDB
from pymongo import MongoClient


def get_time():
    return datetime.today().strftime("%Y-%m-%d")


def process_min_max_values(query, field_label):
    number_of_votes_min_value = query.get(f"votes_min")
    number_of_votes_max_value = query.get("votes_max")

    if not number_of_votes_min_value and not number_of_votes_max_value:
        return {}

    d = {'numberOfVotes': {}}
    if number_of_votes_min_value:
        d['numberOfVotes']["$gte"] = query['votes_min']
    if number_of_votes_max_value:
        d['numberOfVotes']["$lte"] = query['votes_max']

    return d


def get_post_category_query(query):
    if query.get("category"):
        return {"postCategory": query["postCategory"]}
    return {}


def get_query_attrs(query):
    query_dict = {
        **get_post_category_query(query),
        **process_min_max_values(query),
    }
    return query_dict


class MongoDB(AbstractDB):

    def __init__(self, config):
        self.config = config
        client = self.connect()
        self.db = client[self.config.database_name]

    def connect(self):
        return MongoClient(self.config.host, self.config.port)

    def get_post_info(self, args):
        post = self.db.posts.find({'uniqueId': args})
        if post is None:
            return post
        return list(dict(post))

    def get_posts_data(self, query=None):
        query_attr = get_query_attrs(query)
        if query.get('limit') and query.get("offset"):
            return list(self.db.posts.find(query_attr, {'_id': 0})
                        .limit(int(query['limit']))
                        .skip(int(query['offset'])))
        return list(self.db.posts.find(query_attr, {'_id': 0}))

    def insert_post(self, args):
        self.db.posts.insert_one({
            "uniqueId": args['uniqueId'],
            "postUrl": args['postUrl'],
            "username": args['username'],
            "userKarma": args['userKarma'],
            "userCakeDay": args['userCakeDay'],
            "postKarma": args['postKarma'],
            "commentKarma": args['commentKarma'],
            "postDate": args['postDate'],
            "numberOfComments": args['numberOfComments'],
            "numberOfVotes": args['numberOfVotes'],
            "postCategory": args['postCategory'],
            'postAddedDate': get_time()
        })

    def delete_post(self, args):
        self.db.posts.delete_one({'uniqueId': args})

    def update_posts(self, args, post_id):
        self.db.posts.update_many({'uniqueId': post_id}, {"$set": {
            "uniqueId": args['uniqueId'],
            "postUrl": args['postUrl'],
            "username": args['username'],
            "userKarma": args['userKarma'],
            "userCakeDay": args['userCakeDay'],
            "postKarma": args['postKarma'],
            "commentKarma": args['commentKarma'],
            "postDate": args['postDate'],
            "numberOfComments": args['numberOfComments'],
            "numberOfVotes": args['numberOfVotes'],
            "postCategory": args['postCategory'],
            'postAddedDate': get_time()
        }})
