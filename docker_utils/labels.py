#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read container labels and detect defained labels"""

import docker
import re

LABEL_ROOT = 'com.docker.swarm.execron'
LABEL_EXEC = 'exec'
LABEL_WEBHOOK = 'webhook'
LABEL_INTERVAL = 'interval'
LABEL_NUMBER = 'number'  # container number or task number (for swarm)


def get_containers(client):
    return client.containers.list(filters={"label": [LABEL_ROOT + '.' + LABEL_EXEC]})


def get_possible_labels():
    labels = {}
    for l in [LABEL_EXEC, LABEL_INTERVAL, LABEL_NUMBER, LABEL_WEBHOOK]:
        labels[LABEL_ROOT + '.' + l] = l
    return labels


def get_execs(labels, possible_labels, id):
    execs = {}
    for lk, lv in labels.items():
        if lk in possible_labels:
            # exact match
            exec_lk = lk
            exec_key = 'default'

        else:
            # substring match
            ms = re.match(LABEL_ROOT + r'\.(\d+)\.(.*)', lk)
            if ms:
                exec_lk = LABEL_ROOT + '.' + ms.group(2)
                exec_key = int(ms.group(1))
            else:
                exec_key = None
                exec_lk = None

        if exec_key and exec_lk:
            if exec_key not in execs:
                execs[exec_key] = {'id': id}
            execs[exec_key][possible_labels[exec_lk]] = \
                int(lv) if possible_labels[exec_lk] in ['interval', 'number'] else lv

    return execs


def get_all_jobs(cs, possible_labels):
    jobs = []

    for c in cs:
        execs = get_execs(c.labels, possible_labels, c.id)
        for _, v in execs.items():
            jobs.append(v)

    return jobs


if __name__ == '__main__':
    possible_labels = get_possible_labels()
    client = docker.from_env()
    cs = get_containers(client)
    get_all_jobs(cs, possible_labels)
