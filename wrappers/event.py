#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the Operating System stuff.
import os

#...for the logging.
import logging as lg

#...for the JSOB.
import json

#...for the time (being).
import time

class Event(object):
    def __init__(self, m):

        ## The event title.
        self.__title = str(m["title"])

        ## The shortened event title.
        self.__short_title = str(m["short_title"])

        ## The UNIX timestamp representing the start time of the event.
        self.__timestamp = m["timestamp_start"]

        ## The time object representing the start time of the event.
        self.__thetime = time.gmtime(self.__timestamp)

        ## The date and time string to display.
        self.__time_string = time.strftime("%A %d %b %Y, %H:%M (%Z)", self.__thetime)

        ## The UNIX timestamp representing the end time of the event.
        self.__timestamp_end = None
        #
        ## The time object representing the end of the event.
        self.__the_end_time = None
        #
        if "timestamp_end" in m.keys():
            self.__timestamp_end = m["timestamp_end"]
            self.__the_end_time = time.gmtime(self.__timestamp_end)

        ## The URL of the event (if available).
        self.__event_url = None
        #
        if "event_url" in m.keys():
            self.__event_url = m["event_url"]

        ## The URL of the slides (if available).
        self.__slides_url = None
        #
        if "slides_url" in m.keys():
            self.__slides_url = m["slides_url"]

        ## The label to be used for the event's subsection.
        self.__label = m["label"]

        ## A full-text (but brief!) summary of the event.
        self.__summary = m["summary"]

    def __lt__(self, other):
        return self.get_timestamp() < other.get_timestamp()
    def get_title(self):
        return self.__title
    def get_short_title(self):
        return self.__short_title
    def get_label(self):
        return self.__label
    def get_timestamp(self):
        return self.__timestamp
    def get_time_string(self):
        return self.__time_string
    def has_event_end_time(self):
        return self.__the_end_time != None
    def get_start_date_string(self):
        return time.strftime("%A %d %b %Y", self.__thetime)
    def get_end_date_string(self):
        return time.strftime("%A %d %b %Y", self.__the_end_time)
    def has_event_url(self):
        return self.__event_url != None
    def get_event_url(self):
        return self.__event_url
    def get_event_url_latex(self):
        return self.__event_url.replace("_", "\_")
    def get_slides_url(self):
        return self.__slides_url
    def get_slides_url_latex(self):
        return self.__slides_url.replace("_", "\_")
    def get_event_date_short(self):
        return time.strftime("%Y-%m-%d", self.__thetime)
    def get_summary_latex(self):
        return self.__summary
