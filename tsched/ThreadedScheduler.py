#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Common class for deferred execution (scheduling) of any callables objects like functions in separate thread."""
import logging
import sched
import sys
import threading


class ThreadedScheduler(threading.Thread):
    _scheduler = None
    _stop_sheduler = False

    def __init__(self):
        self._scheduler = sched.scheduler()
        super().__init__(target=self._scheduler.run)

    def _threaded_scheduler_exec(self, schedule_item):
        logging.info('Executing %s...', schedule_item['callable'])
        try:
            args = schedule_item['args'] if 'args' in schedule_item and schedule_item['args'] else ()
            kwargs = schedule_item['kwargs'] if 'kwargs' in schedule_item and schedule_item['kwargs'] else {}
            res = schedule_item['callable'](*args, **kwargs)
            logging.info('Executed successfully (%s returned).', type(res))
        except Exception as e:
            m = getattr(e, 'message', repr(e))
            logging.warning('Exception due %s execution: %s', schedule_item['callable'], m)
        if not self._stop_sheduler:
            self._scheduler.enter(schedule_item['delay'], schedule_item['priority'], self._threaded_scheduler_exec,
                                  (schedule_item,))
            logging.info('%s scheduled with delay %d', schedule_item['callable'], schedule_item['delay'])
        sys.stdout.flush()

    def start_scheduler(self, schedule):
        """Schedule given callables for further execution

        :param schedule: Callables list. Each list item is a dictionary with following structure:
            {
                'callable': callable,                                   # required
                'delay': delay_in_seconds,                              # required
                'priority': scheduled_job_priority,                     # required
                'args': callable_positional_arguments_list_or_tuple,    # not required, default is ()
                'kwargs': callable_keyed_arguments_dictionary           # not required, default is {}
            }
        :type schedule: list

        :returns: None
        """
        self._stop_sheduler = False
        for s in schedule:
            self._scheduler.enter(s['delay'], s['priority'], self._threaded_scheduler_exec, (s,))
        logging.info('Scheduler initialized!')

    def stop_scheduler(self, immediately=True):
        self._stop_sheduler = True
        logging.info('Stop flag set.')
        if immediately:
            list(map(self._scheduler.cancel, self._scheduler.queue))
            logging.info('Scheduler queue cleaned!')


if __name__=='__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def printer(a, b="this is b"):
        print(a, b)

    def exceptional():
        raise ValueError

    ts = ThreadedScheduler()
    schedule = [
        {
            'delay': 1,
            'priority': 2,
            'callable': printer,
            'args': ['this is a'],
            'kwargs': {}
        },
        {
            'delay': 2,
            'priority': 10,
            'callable': printer,
            'args': ('awesome',),
            'kwargs': {'b': 'bad'}
        },
        {
            'delay': 3,
            'priority': 10,
            'callable': exceptional,
            'args': None,
            'kwargs': None
        },
        {
            'delay': 3,
            'priority': 10,
            'callable': exceptional,
        },
    ]

    ts.start_scheduler(schedule)
    ts.start()

    # Exception must be correctly handled to
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info('Keyboard interrupt, finishing loop...\n')

    ts.stop_scheduler()
    ts.join()
