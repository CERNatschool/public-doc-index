#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 make_presentations_table.py

 Makes the presentation entries for the MoEDAL section.

 See the README.md file for more information.

 http://researchinschools.org

"""

#...for the Operating System stuff.
import os

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for the JSOB.
import json

#...for the time (being).
import time

class Presentation(object):
    """ Wrapper class for a presentation. """
    def __init__(self, m):

        ## The presentation title.
        self.__title = str(m["title"])

        ## The shortened presentation title.
        self.__short_title = str(m["short_title"])

        ## The meeting type.
        self.__meeting_type = m["meeting_type"]

        ## The UNIX timestamp representing the start time of the meeting.
        self.__timestamp = m["timestamp"]

        ## The time object representing the start time of the meeting.
        self.__thetime = time.gmtime(self.__timestamp)

        ## The date and time string to display.
        self.__time_string = time.strftime("%A %d %b %Y, %H:%M (%Z)", self.__thetime)

        ## The URL of the meeting at which the presentation was given.
        self.__meeting_url = m["meeting_url"]

        ## The URL of the slides.
        self.__slides_url = m["slides_url"]

        ## The label to be used for the presentation's subsection.
        self.__label = m["label"]

        ## A full-text (but brief!) summary of the presentation's slides.
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
    def get_meeting_url(self):
        return self.__meeting_url
    def get_meeting_url_latex(self):
        return self.__meeting_url.replace("_", "\_")
    def get_slides_url(self):
        return self.__slides_url
    def get_slides_url_latex(self):
        return self.__slides_url.replace("_", "\_")
    def get_meeting_type(self):
        return self.__meeting_type
    def get_meeting_type_long(self):
        if self.__meeting_type=="SAN":
            return "Software \& Analysis Meeting"
        elif self.__meeting_type=="COL":
            return "Collaboration Meeting"
    def get_meeting_date_short(self):
        return time.strftime("%Y-%m-%d", self.__thetime)
    def get_summary_latex(self):
        return self.__summary


if __name__ == "__main__":

    print("*")
    print("*=============================*")
    print("* make_presentations_table.py *")
    print("*=============================*")
    print("*")

    # Parse the command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFilePath",   help="Path to the input file.")
    parser.add_argument("outputPath",      help="Path to the output folder.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The output path.
    output_path = args.outputPath
    #
    # Check if the output directory exists. If it doesn't, raise an error.
    if not os.path.isdir(output_path):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (output_path))

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    ## Log file path.
    log_file_path = os.path.join(output_path, 'log_make_presentations_table.log')

    # Configure the logging.
    lg.basicConfig(filename=log_file_path, filemode='w', level=level)

    ## The path to the input file.
    input_file_path = args.inputFilePath
    #
    if not os.path.exists(input_file_path):
        raise IOError("* ERROR: Unable to find input file at '%s'." % (input_file_path))

    lg.info(" *========================*")
    lg.info(" * make_meetings_table.py *")
    lg.info(" *========================*")
    lg.info(" *")
    lg.info(" * Input file path : %s" % (input_file_path))
    lg.info(" * Output path     : %s" % (output_path))
    lg.info(" *")


    # Get the meetings from the JSON file.

    with open(input_file_path, "r") as jf:
        js = json.load(jf)

    #print js

    t = """
%______________________________________________________________________________
\\begin{table}[h]
\\caption{\\label{tab:moedalmeetings}A list of the MoEDAL-related
presentations given by the Fellow. Collaboration meeting presentations
are indicated with an asterisk.}
\\lineup
\\begin{indented}
\item[]\\begin{tabular}{@{}ll}
\\br
\\centre{1}{$\\quad$Date    $\\quad$} &
\\centre{1}{$\\quad$Title   $\\quad$} \\\\
\\mr"""


    s = ""

    ms = []

    for mj in js:
        ms.append(Presentation(mj))

    for m in sorted(ms):

        lg.info(" * Title       : %s" % (m.get_title()))
        lg.info(" * Short title : %s" % (m.get_short_title()))
        lg.info(" * Timestamp   : %d" % (m.get_timestamp()))
        lg.info(" * Time        : %s" % (m.get_time_string()))
        lg.info(" * Meeting URL : %s" % (m.get_meeting_url()))
        lg.info(" * Slides URL  : %s" % (m.get_slides_url()))
        lg.info(" *")
        s += "%=============================================================================\n"
        s += "\\subsubsection{%s %s}\n" % (m.get_meeting_type_long(), m.get_meeting_date_short())
        s += "\\label{meeting:%s}\n" % (m.get_label())
        s += "%=============================================================================\n"
        s += "\\begin{itemize}\n"
        s += "\\item \\bullettext{Full title}: %s;\n" % (m.get_title())
        s += "\\item \\bullettext{Date and time}: %s;\n" % (m.get_time_string())
        s += "\\item \\bullettext{Meeting URL}: \\href{%s}{%s} (\href{%s}{slides});\n" % (m.get_meeting_url_latex(), m.get_meeting_url_latex(), m.get_slides_url_latex())
        s += "\\end{itemize}\n"
        s += "%s\n" % (m.get_summary_latex())
        s += "%\n"
        s += "\n"

        # Add the presentation entry to the table.
        if m.get_meeting_type() == "COL":
            t += "\\texttt{%s *} & \\hyperref[meeting:%s]{%s.}\\\\\n" % (m.get_meeting_date_short(), m.get_label(), m.get_short_title())
        else:
            t += "\\texttt{%s} & \\hyperref[meeting:%s]{%s.}\\\\\n" % (m.get_meeting_date_short(), m.get_label(), m.get_short_title())

    # Complete the presentations table.
    t += """\\br
\\end{tabular}
\\end{indented}
\\end{table}
%______________________________________________________________________________
"""

    ## The path of the TeX output file containing the presentation information.
    output_tex_path = os.path.join(output_path, "presentations.tex")

    with open(output_tex_path, "w") as sf:
        sf.write(s)

    ## The path of the table TeX file.
    output_tex_table_path = os.path.join(output_path, "presentationstable.tex")

    with open(output_tex_table_path, "w") as tf:
        tf.write(t)
