#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the Operating System stuff.
import os

#...for the logging.
import logging as lg

#...for the JSOB.
import json

class CodeRepository(object):
    def __init__(self, m):

        ## The repository name.
        self.__name = str(m["name"])

        ## The repository host.
        self.__host = str(m["host"])

        ## The repository's organization.
        self.__organization = None
        #
        if "organization" in m.keys():
            self.__organization = m['organization']

        ## A short title for the repository.
        self.__short_title = m['short_title']

        ## The DOI of the latest recorded release.
        self.__doi = None
        #
        ## The latest recorded release tag.
        self.__release = None
        #
        if "doi" in m.keys():
            self.__doi = m["doi"]
            self.__release = m["release"]

        ## The label to be used for the repository's subsection.
        self.__label = m["label"]

        ## A full-text (but brief!) summary of the repository.
        self.__summary = m["summary"]

    def __lt__(self, other):
        return self.get_repository_name() < other.get_repository_name()
    def get_repository_name(self):
        return self.__name
    def get_label(self):
        return self.__label
    def get_host(self):
        return self.__host
    def has_organization(self):
        return self.__organization != None
    def get_organization_name(self):
        return self.__organization
    def get_organization_homepage(self):
        return os.path.join(self.__host, self.__organization)
    def get_repository_homepage(self):
        if self.has_organization():
            return os.path.join(self.get_organization_homepage(), self.__name)
    def get_repository_short_title(self):
        return self.__short_title
    def has_doi(self):
        return self.__doi != None
    def get_doi(self):
        return self.__doi
    def get_release(self):
        return self.__release
    def get_summary_latex(self):
        return self.__summary
