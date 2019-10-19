#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provide some extra functions to work with MongoDB via pymongo."""
from pymongo import MongoClient
import utils


def connect(config) -> MongoClient:
    """Connect to the MongoDB with given config"""
    host = config['host'] if 'host' in config else \
        config['MONGODB_HOST'] if 'MONGODB_HOST' in config else 'localhost'

    port = int(config['port']) if 'port' in config else \
        int(config['MONGODB_PORT']) if 'MONGODB_PORT' in config else 27017

    username = config['username'] if 'username' in config else config['MONGODB_USERNAME']
    password = config['password'] if 'password' in config else config['MONGODB_PASSWORD']
    database = config['database'] if 'database' in config else config['MONGODB_DATABASE']
    return MongoClient("mongodb://{}:{}@{}:{}/{}".format(username, password, host, port, database))


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
