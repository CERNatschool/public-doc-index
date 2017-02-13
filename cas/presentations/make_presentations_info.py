#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 make_presentations_info.py

 Makes the presentation entries for the presentations section.

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
    """ The Presentations wrapper class. """
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
        self.__meeting_url = None
        #
        if "meeting_url" in m.keys():
            self.__meeting_url = m["meeting_url"]

        ## The URL of the slides.
        self.__slides_url = None
        #
        if "slides_url" in m.keys():
            self.__slides_url = m["slides_url"]

        ## The label to be used for the presentation's subsection.
        self.__label = m["label"]

        ## A full-text (but brief!) summary of the presentation's slides.
        self.__summary = m["summary"]

        ## The presentation type.
        self.__type = None
        #
        if "meeting_type" in m.keys():
            self.__type = m['meeting_type']

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
    def has_meeting_url(self):
        return self.__meeting_url != None
    def get_meeting_url(self):
        return self.__meeting_url
    def get_meeting_url_latex(self):
        return self.__meeting_url.replace("_", "\_")
    def has_slides_url(self):
        return self.__slides_url != None
    def get_slides_url(self):
        return self.__slides_url
    def get_slides_url_latex(self):
        return self.__slides_url.replace("_", "\_")
    def get_meeting_type(self):
        return self.__meeting_type
    def get_meeting_type_long(self):
        if self.__meeting_type=="COL":
            return "Collaboration Meeting"
        elif self.__meeting_type == "SCH":
            return "Schools talk"
    def is_schools_presentation(self):
        return self.__meeting_type == "SCH"
    def get_meeting_date_short(self):
        return time.strftime("%Y-%m-%d", self.__thetime)
    def get_summary_latex(self):
        return self.__summary

if __name__ == "__main__":

    print("*")
    print("*=============================*")
    print("* make_presentations_info.py *")
    print("*=============================*")
    print("*")

    # Parse the command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFilePath",   help="Path to the input file.")
    parser.add_argument("outputPath",      help="Path to the output folder.")
    parser.add_argument("subject",         help="The subject.")
    parser.add_argument("subjectCode",     help="The subject code (for labels etc.).")
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
    log_file_path = os.path.join(output_path, 'log_make_presentations_info.log')

    # Configure the logging.
    lg.basicConfig(filename=log_file_path, filemode='w', level=level)

    ## The path to the input file.
    input_file_path = args.inputFilePath
    #
    if not os.path.exists(input_file_path):
        raise IOError("* ERROR: Unable to find input file at '%s'." % (input_file_path))

    ## The subject of the presentations.
    subject = str(args.subject)

    ## The subject code (used for labels etc.)
    subject_code = str(args.subjectCode)

    lg.info(" *============================*")
    lg.info(" * make_presentations_info.py *")
    lg.info(" *============================*")
    lg.info(" *")
    lg.info(" * Input file path : %s" % (input_file_path))
    lg.info(" * Output path     : %s" % (output_path))
    lg.info(" * Subject         : %s" % (subject))
    lg.info(" * Subject code    : %s" % (subject_code))
    lg.info(" *")

    print("* Input file path : %s" % (input_file_path))
    print("* Output path     : %s" % (output_path))
    print("* Subject         : %s" % (subject))
    print("* Subject code    : %s" % (subject_code))
    print("*")


    # Get the meetings from the JSON file.

    with open(input_file_path, "r") as jf:
        js = json.load(jf)

    #print js
    t = """
%______________________________________________________________________________
\\begin{table}[h]
\\caption{\\label{tab:SUBJECT_CODEpresentations}A list of the
presentations relating to the SUBJECT_NAME programme.}
\\lineup
\\begin{indented}
\item[]\\begin{tabular}{@{}ll}
\\br
\\centre{1}{$\\quad$Date    $\\quad$} &
\\centre{1}{$\\quad$Title   $\\quad$} \\\\
\\mr"""

    t = t.replace("SUBJECT_CODE", subject_code)
    t = t.replace("SUBJECT_NAME", subject)

    ## String for the section TeX.
    s = ""

    ms = []

    for mj in js:
        ms.append(Presentation(mj))

    for m in sorted(ms):

        lg.info(" * Title       : %s" % (m.get_title()))
        lg.info(" * Short title : %s" % (m.get_short_title()))
        lg.info(" * Timestamp   : %d" % (m.get_timestamp()))
        lg.info(" * Time        : %s" % (m.get_time_string()))
        lg.info(" *")

        if m.is_schools_presentation():
            lg.info(" *--> Schools talk - skipping the subsection.")
            t += " \\texttt{%s} & %s.\\\\\n" % (m.get_meeting_date_short(), m.get_short_title())
            continue

        # Add the presentation entry to the table.
        t += " \\texttt{%s} & \\hyperref[meeting:%s]{%s.}\\\\\n" % (m.get_meeting_date_short(), m.get_label(), m.get_short_title())

        s += "%=============================================================================\n"
        s += "\\subsubsection{%s, %s}\n" % (m.get_short_title(), m.get_meeting_date_short())
        s += "\\label{meeting:%s}\n" % (m.get_label())
        s += "%=============================================================================\n"
        s += "\\begin{itemize}\n"
        s += "\\item \\bullettext{Full title}: %s;\n" % (m.get_title())
        s += "\\item \\bullettext{Date and time}: %s;\n" % (m.get_time_string())
        if m.has_meeting_url():
            if len(m.get_meeting_url_latex()) < 60:
                s += "\\item \\bullettext{Meeting URL}: \\href{%s}{%s}" % (m.get_meeting_url_latex(), m.get_meeting_url_latex())
            else:
                s += "\\item \\bullettext{Meeting URL}: \\href{%s}{%s...}" % (m.get_meeting_url_latex(), m.get_meeting_url_latex()[:40])
            if m.has_slides_url():
                s += " (\\href{%s}{slides})\n" % (m.get_slides_url_latex())
            else:
                s += "\n"
        s += "\\end{itemize}\n"
        s += "%s\n" % (m.get_summary_latex())
        s += "%\n"
        s += "\n"


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
    output_tex_info_path = os.path.join(output_path, "presentationstable.tex")

    with open(output_tex_info_path, "w") as tf:
        tf.write(t)
