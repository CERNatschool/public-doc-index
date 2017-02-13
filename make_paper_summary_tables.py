#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 make_paper_summary_tables.py

 See the README.md file for more information.

 http://researchinschools.org

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for the BibTeX files.
import bibtexparser

# Import the Paper wrapper class.
from wrappers.paper import Paper

if __name__ == "__main__":

    print("*")
    print("*==========================================*")
    print("* CERN@school: Make the Publications Table *")
    print("*==========================================*")
    print("*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("bibfilePath",     help="Path to the input dataset.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the input BibTeX file.
    bibfile_path = args.bibfilePath

    # Check if the input file exists. If it doesn't, quit.
    if not os.path.exists(bibfile_path):
        raise IOError("* ERROR: '%s' input file does not exist!" % (bibfile_path))

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=os.path.join('./logfiles/.', 'make_paper_summary_tables.log'), filemode='w', level=level)

    lg.info(" *")
    lg.info(" *============================================*")
    lg.info(" * CERN@school: Make the Paper Summary Tables *")
    lg.info(" *============================================*")
    lg.info(" *")
    lg.info(" * Input BibTeX file: '%s'" % (bibfile_path))
    lg.info(" *")

    with open(bibfile_path, 'r') as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)

    lg.info(" * Number of entries: %d" % (len(bib_database.entries)))
    lg.info(" *")

    ## A list of the papers.
    papers = []

    # Get the papers (and check whether the PDF is there).
    for entry in bib_database.entries:
        if entry['ENTRYTYPE'] == 'article':
            paper = Paper(entry)
            papers.append(paper)

    ## The LaTeX table pages string.
    ts = ""

    ## The string for the top of the table.
    table_top_s = """
%______________________________________________________________________________
\\begin{table}[ht]
\\small
\\caption{\label{tab:papersTABLE_NUM}Publications associated with
and/or referenced by the CERN@school programme (TABLE_NUM/NUM_TABLES).}
\\lineup
\\begin{indented}
\\item[]\\begin{tabular}{@{}lllcc}
\\br
\\centre{1}{$\\quad$Citation    $\\quad$} &
\\centre{1}{$\\quad$DOI or URL  $\\quad$} &
\\centre{1}{$\\quad$Notes       $\\quad$} &
\\centre{1}{$\\quad$Year        $\\quad$} &
\\centre{1}{$\\quad$Ref.        $\\quad$} \\\\
\\mr
%"""

    ## The string for the bottom of the table.
    table_bottom_s = """
\\br
\\end{tabular}
\\end{indented}
\\end{table}
%______________________________________________________________________________
%"""

    # Break the list into a number of tables so that one fits on a page.

    ## Number of rows in each table.
    num_rows = 30

    if len(papers) <= num_rows:
        table_top_s = table_top_s.replace(" (TABLE_NUM/NUM_TABLES)", "")

    ## The number of tables found in the BibTeX file.
    number_of_tables = len(papers) / num_rows + 1

    ## The current table number.
    table_number = 0

    # Loop through the papers in reverse chronological order.
    for i, paper in enumerate(sorted(papers, reverse=False)):

        if ((i) % num_rows == 0) or ():
            table_number += 1
            lg.info("* Starting table % 3d with paper %d" % (table_number, i+1))

            # Add the top of the table.
            ts += table_top_s.replace("TABLE_NUM", "%d" % (table_number)).replace("NUM_TABLES", "%d" % (number_of_tables))


        if paper.has_doi():
            link = "http://dx.doi.org/%s" % (paper.get_doi())
        else:
            link = paper.get_url()
        link = link.replace("_", "\_")
        ts += "%_____________________________________________________________________________\n"
        ts += "\\texttt{%s} & \n" % (paper.get_id())
        if paper.has_doi():
            ts += "\\href{%s}{%s} &\n" % (link, paper.get_doi().replace("_", "\_"))
        else:
            ts += "\\href{%s}{%s} &\n" % (link, paper.get_url().replace("_", "\_"))
        if paper.has_annotation():
            ts += "%s & \n" % (paper.get_annotation())
        else:
            ts += " & \n"
        ts += "%s &\n" % (paper.get_year())
        ts += "\\cite{%s}\n" % (paper.get_id())
        ts += "\\\\\n"
        ts += "%_____________________________________________________________________________\n"

        if (i+1) % num_rows == 0 or (i+1) == len(papers):
            lg.info("* Finishing table % 3d with paper %d" % (table_number, i+1))

            # Add the bottom of the table.
            ts += table_bottom_s

            if (i+1) == len(papers):
                break

    ## Where to write the TeX file.
    output_path_tex_table = "autotable.tex"
    #
    with open(output_path_tex_table, "w") as tf:
        tf.write(ts)
