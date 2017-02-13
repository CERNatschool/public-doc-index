#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

class Paper(object):
    """
    Wrapper base class for a paper.
    """

    def __init__(self, bd):
        """
        Constructor.

        @param [in] bd BibTeX entry dictionary.
        """

        ## The ID.
        self.__id = bd['ID']

        ## The title.
        self.__title = None
        #
        if 'title' in bd.keys():
            self.__title = bd['title']

        ## The year of publication.
        self.__year = None
        #
        if 'year' in bd.keys():
            self.__year = bd['year']

        ## The Digital Object Identifier (DOI).
        self.__doi = None

        ## The URL.
        self.__url = None

        if bd['ENTRYTYPE'] == "book":
            lg.info(" * %s is a book, skipping." % (self.get_id()))
            lg.info(" *")
            return None

        if 'doi' in bd.keys():
            self.__doi = bd['doi']

        if 'link' in bd.keys():
            self.__url = bd['link']

        ## Custom annotation - used in summary tables etc.
        self.__annotation = None
        #
        if 'annote' in bd.keys():
            self.__annotation = bd['annote']

        lg.info(" * Paper ID  : '%s'" % (self.get_id()))
        lg.info(bd)

        if self.has_title(): lg.info(" * Title     : '%s'" % (self.get_title()))
        else:                lg.info(" * '%s' HAS NO TITLE!" % (self.get_id()))
        if self.has_year():  lg.info(" * Year      : '%s'" % (self.get_year()))
        else:
            lg.info(" * '%s' HAS NO YEAR!" % (self.get_id()))
            #raise IOError("* %s has no year!" % (self.get_id()))
        if self.has_doi():  lg.info(" * DOI     : '%s'" % (self.get_doi()))
        else:
            lg.info(" * '%s' HAS NO DOI!"    % (self.get_id()))
            #raise IOError("* %s has no DOI!" % (self.get_id()))
        lg.info(" *")


    def __lt__(self, other):
        return self.get_year() < other.get_year()
    def get_id(self):
        return self.__id
    def has_title(self):
        return self.__title != None
    def get_title(self):
        return self.__title
    def has_year(self):
        return self.__year is not None
    def get_year(self):
        return self.__year
    def has_doi(self):
        return self.__doi is not None
    def get_doi(self):
        return self.__doi
    def has_url(self):
        return self.__url is not None
    def get_url(self):
        return self.__url
    def has_annotation(self):
        return self.__annotation is not None
    def get_annotation(self):
        return self.__annotation
