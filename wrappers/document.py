#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the Operating System stuff.
import os

#...for the logging.
import logging as lg

#...for the JSOB.
import json

class Document(object):
    def __init__(self, m):

        ## The presentation title.
        self.__title = str(m["title"])

        ## The shortened presentation title.
        self.__short_title = str(m["short_title"])

        ## The Document Reference Number (DRN).
        self.__drn = str(m["drn"])

        ## The DOI.
        self.__doi = None
        #
        if "doi" in m.keys():
            self.__doi = m["doi"]

        ## The URL (if any).
        self.__url = None
        #
        if "url" in m.keys():
            self.__url = m['url']

        ## The (Grid) Logical File Name (LFN) -- if any.
        self.__lfn = None
        #
        if "lfn" in m.keys():
            self.__lfn = m['lfn']

        ## The label to be used for the document's subsection.
        self.__label = m["label"]

        ## A full-text (but brief!) summary of the document.
        self.__summary = m["summary"]

    def __lt__(self, other):
        if "PUB" in self.get_drn() and "INT" in other.get_drn():
            return True
        elif "INT" in self.get_drn() and "PUB" in other.get_drn():
            return False
        else:
            return self.get_drn() < other.get_drn()
    def get_title(self):
        return self.__title
    def get_short_title(self):
        return self.__short_title.replace("&","\&")
    def get_label(self):
        return self.__label
    def get_drn(self):
        return self.__drn
    def has_doi(self):
        return self.__doi != None
    def get_doi(self):
        return self.__doi
    def has_url(self):
        return self.__url != None
    def get_url_latex(self):
        return self.__url.replace("_", "\_")
    def has_lfn(self):
        return self.__lfn != None
    def get_lfn(self):
        return self.__lfn
    def get_summary_latex(self):
        return self.__summary
