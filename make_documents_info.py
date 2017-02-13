#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 make_documents_info.py

 Makes the document entries for the documents section.

 See the README.md file for more information.

 http://www.gridpp.ac.uk

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

# For the Document wrapper class.
from wrappers.document import Document


if __name__ == "__main__":

    print("*")
    print("*=========================*")
    print("* make_documents_info.py *")
    print("*=========================*")
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
    log_file_path = os.path.join(output_path, 'log_make_documents_info.log')

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

    lg.info(" *=========================*")
    lg.info(" * make_documents_info.py *")
    lg.info(" *=========================*")
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

    # Get the events from the JSON file.

    with open(input_file_path, "r") as jf:
        js = json.load(jf)

    #print js

    t = """
%______________________________________________________________________________
\\begin{table}[htbp]
\\caption{\\label{tab:SUBJECT_CODEdocuments}Documents relating to
SUBJECT_NAME research and activities.}
\\lineup
\\begin{indented}
\item[]\\begin{tabular}{@{}lll}
\\br
\\centre{1}{$\\quad$DRN         $\\quad$} &
\\centre{1}{$\\quad$Brief Title $\\quad$} &
\\centre{1}{$\\quad$DOI or URL  $\\quad$} \\\\
\\mr
"""

    t = t.replace("SUBJECT_CODE", subject_code)
    t = t.replace("SUBJECT_NAME", subject)

    s = ""

    ms = []

    for mj in js:
        ms.append(Document(mj))

    for m in sorted(ms):

        lg.info(" * Title       : %s" % (m.get_title()))
        lg.info(" * Short title : %s" % (m.get_short_title()))
        lg.info(" *")
        s += "%=============================================================================\n"
        s += "\\subsubsection{%s}\n" % (m.get_short_title())
        s += "\\label{meeting:%s}\n" % (m.get_label())
        s += "%=============================================================================\n"
        s += "\\begin{itemize}\n"
        s += "\\tightlist\n"
        s += "\\item \\bullettext{Full title}: %s\n" % (m.get_title())
        s += "\\item \\bullettext{DRN}: %s\n" % (m.get_drn())
        if m.has_doi():
            s += "\\item \\bullettext{DOI}: \\href{http://doi.org/%s}{%s}\n" % (m.get_doi(), m.get_doi())
        elif m.has_url():
            s += "\\item \\bullettext{URL}: \\href{%s}{%s}\n" % (m.get_url_latex(), m.get_url_latex())
        elif m.has_lfn():
            s += "\\item \\bullettext{LFN}: %s\n" % (m.get_lfn())
        s += "\\end{itemize}\n"
        s += "%s\n" % (m.get_summary_latex())
        s += "%\n"
        s += "\n"

        # Add the document entry to the table.
        if m.has_doi():
            t += "\\texttt{%s} & %s & \\href{http://doi.org/%s}{\\texttt{%s}} \\\\\n" % (m.get_drn(), m.get_short_title(), m.get_doi(), m.get_doi())
        elif m.has_url() and "twiki" in m.get_url_latex().lower():
            t += "\\texttt{%s} & %s & \\href{%s}{MoEDAL Twiki page} \\\\\n" % (m.get_drn(), m.get_short_title(), m.get_url_latex())
        elif m.has_url():
            t += "\\texttt{%s} & %s & See \\url{%s} \\\\\n" % (m.get_drn(), m.get_short_title(), m.get_url_latex())
        elif m.has_lfn():
            t += "\\texttt{%s} & %s & \\texttt{%s} \\\\\n" % (m.get_drn(), m.get_short_title(), m.get_lfn())

    # Complete the presentations table.
    t += """\\br
\\end{tabular}
\\end{indented}
\\end{table}
%______________________________________________________________________________
"""

    ## The path of the TeX output file containing the document information.
    output_tex_path = os.path.join(output_path, "documents.tex")

    with open(output_tex_path, "w") as sf:
        sf.write(s)

    ## The path of the table TeX file.
    output_tex_table_path = os.path.join(output_path, "documentstable.tex")

    with open(output_tex_table_path, "w") as tf:
        tf.write(t)
