#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 make_code_info.py

 Makes the document entries for the documents section.

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

# For the Document wrapper class.
from wrappers.code import CodeRepository


if __name__ == "__main__":

    print("*")
    print("*===================*")
    print("* make_code_info.py *")
    print("*===================*")
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
    log_file_path = os.path.join('logfiles', 'log_make_code_info.log')

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

    lg.info(" *===================*")
    lg.info(" * make_code_info.py *")
    lg.info(" *===================*")
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

    # Get the code repository information from the JSON file.

    with open(input_file_path, "r") as jf:
        js = json.load(jf)

    #print js

    t = """
%______________________________________________________________________________
\\begin{table}[htbp]
\\caption{\\label{tab:SUBJECT_CODEcode}Code repositories associated with
SUBJECT_NAME research and activities.}
\\lineup
\\begin{indented}
\item[]\\begin{tabular}{@{}llll}
\\br
\\centre{1}{$\\quad$Host            $\\quad$} &
\\centre{1}{$\\quad$Organisation    $\\quad$} &
\\centre{1}{$\\quad$Repository Name $\\quad$} &
\\centre{1}{$\\quad$Section         $\\quad$} \\\\
\\mr
"""

    t = t.replace("SUBJECT_CODE", subject_code)
    t = t.replace("SUBJECT_NAME", subject)

    s = ""

    ms = []

    for mj in js:
        ms.append(CodeRepository(mj))

    for m in sorted(ms):

        lg.info(" * Repository name     : %s" % (m.get_repository_name()))
        lg.info(" *")
        s += "%=============================================================================\n"
        s += "\\subsubsection{%s}\n" % (m.get_repository_short_title())
        s += "\\label{sec:%s}\n" % (m.get_label())
        s += "%=============================================================================\n"
        s += "\\url{%s}\n" % (m.get_repository_homepage())
        s += "\n\n"
        if m.has_doi():
            s += "\\begin{itemize}\n"
            s += "\\tightlist\n"
            s += "\\item \\bullettext{Latest release}: %s\n" % (m.get_release())
            s += "\\item \\bullettext{DOI}: \\href{http://doi.org/%s}{%s}\n" % (m.get_doi(), m.get_doi())
            s += "\\end{itemize}\n"
        s += "%s\n" % (m.get_summary_latex())
        s += "%\n"
        s += "\n"

        # Add the presentation entry to the table.
        t += "\\url{%s} & \\href{%s}{%s} & \\href{%s}{%s} & \\ref{sec:%s} \\\\\n" % (\
          m.get_host(), \
          m.get_organization_homepage(), m.get_organization_name(), \
          m.get_repository_homepage(), m.get_repository_name(), \
          m.get_label()\
        )

    # Complete the presentations table.
    t += """\\br
\\end{tabular}
\\end{indented}
\\end{table}
%______________________________________________________________________________
"""

    ## The path of the TeX output file containing the code repository information.
    output_tex_path = os.path.join(output_path, "code.tex")

    with open(output_tex_path, "w") as sf:
        sf.write(s)

    ## The path of the table TeX file.
    output_tex_table_path = os.path.join(output_path, "codetable.tex")

    with open(output_tex_table_path, "w") as tf:
        tf.write(t)
