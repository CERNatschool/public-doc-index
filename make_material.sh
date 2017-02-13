#!/bin/bash
#
# CERN@school
python cas/presentations/make_presentations_info.py cas/presentations/presentations.json cas/presentations/. CERN@school cas

python make_documents_info.py cas/documents/documents.json cas/documents/. CERN@school cas
python make_events_info.py    cas/events/events.json       cas/events/.    CERN@school cas
python make_code_info.py      cas/code/code.json           cas/code/.      CERN@school cas

# MoEDAL
python moedal/presentations/make_presentations_table.py moedal/presentations/presentations.json moedal/presentations/.

python make_documents_info.py moedal/documents/documents.json moedal/documents/ MoEDAL moedal
python make_events_info.py    moedal/events/events.json       moedal/events/    MoEDAL moedal       
python make_code_info.py      moedal/code/code.json           moedal/code/      MoEDAL moedal

# The publications table.
python make_paper_summary_tables.py common/bib/cernatschool.bib
