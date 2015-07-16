# coding: utf-8
# Module: timers
# Created on: 14.07.2015
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)
from __future__ import division
import threading
from datetime import datetime, timedelta
from time import sleep


class Timer(object):
    """Timer class"""
    def __init__(self, interval, func, *args, **kwargs):
        """
        Class constructor

        :param interval: int timer interval in seconds
        :param func: a callable object
        :param args: function positional args
        :param kwargs: function kwargs
        """
        self._interval = interval
        self._func = func
        self._abort_flag = threading.Event()
        self._thread = threading.Thread(target=self._runner, args=args, kwargs=kwargs)
        self._thread.daemon = True

    def _runner(self, *args, **kwargs):
        """
        Timed function runner

        :return:
        """
        timestamp = datetime.now()
        while not self._abort_flag.is_set():
            if datetime.now() - timestamp >= timedelta(seconds=self._interval):
                self._func(*args, **kwargs)
                timestamp = datetime.now()
            sleep(0.1)

    def start(self):
        """
        Timer start

        :return:
        """
        self._thread.start()

    def abort(self):
        """
        Abort timer

        :return:
        """
        self._abort_flag.set()


def check_seeding_limits(torrenter, max_ratio=0, max_time=0):
    """
    Check seding limits

    :param torrenter:
    :param max_ratio:
    :param max_time:
    :return:
    """
    for torrent in torrenter.get_all_torrents_info():
        try:
            ratio = torrent['total_upload'] / torrent['total_download']
        except ZeroDivisionError:
            ratio = 0
        if torrent['state'] == 'seeding' and max_ratio and ratio >= max_ratio:
            torrenter.pause_torrent(torrent['info_hash'])
        try:
            if (torrent['state'] == 'seeding'
                and max_time
                and datetime.now() - datetime.strptime(torrent['completed_time'], '%Y-%m-%d %H:%M:%S')
                    >= timedelta(hours=max_time)):
                torrenter.pause_torrent(torrent['info_hash'])
        except ValueError:
            pass


def save_resume_data(torrenter):  # Not used yet.
    """
    Save torrents resume data

    :param torrenter:
    :return:
    """
    torrenter.save_all_resume_data()
