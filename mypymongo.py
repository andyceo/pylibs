from pymongo import MongoClient
from pylibs import config


def connect(section, collection=None):
    """Connect to the mongo"""
    host = config[section]['host']
    port = int(config[section]['port'])
    username = config[section]['username']
    password = config[section]['password']
    db = config[section]['database'] if config.has_option(section, 'database') else config[section]['db']
    client = MongoClient("mongodb://{}:{}@{}:{}/{}".format(username, password, host, port, db))

    if collection is None:
        return client[db]
    else:
        return client[db][collection]
