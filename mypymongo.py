from pymongo import MongoClient
from pylibs import config
from pylibs import utils


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


def excluded_fields(db, collection):
    excluded_fields = {
        'mongo-alfadirect': {
            'bitfinex_balances': {
                '_id': False,
            },
            'bitfinex_offers': {
                '_id': False,
                'changelog': False,
            }
        }
    }
    return excluded_fields[db][collection]


def update_timestamps(collection, id_field_name='_id', timestamp_field_name='timestamp'):
    for document in collection.find({}):
        ts = utils.timestamp_normalize(document[timestamp_field_name])
        if ts != document[timestamp_field_name]:
            collection.update_one({id_field_name: document[id_field_name]}, {'$set': {
                'timestamp': ts,
            }})
            utils.message('Updated: id {}, old {}, new {}'.format(document[id_field_name], document['timestamp'], ts))
        else:
            utils.message('Unchanged document id {}, {}'.format(document[id_field_name], document['timestamp']))


def remove_changelogs(collection, id_field_name='_id', changelog_field_name='changelog'):
    for document in collection.find({}):
        if changelog_field_name in document:
            collection.update_one({id_field_name: document[id_field_name]}, {'$unset': {
                changelog_field_name: 1,
            }})
            utils.message('Removed field {} in document id {}'.format(changelog_field_name, document[id_field_name]))
        else:
            utils.message('Unchanged document id {}'.format(document[id_field_name]))
