# The CERN@school Programme: Document Index
CERN@school is a student-led research programme that brings
CERN into the classroom.
This repository contains the LaTeX code and JSON files
needed to generate the CERN@school Programme's Document Index,
which provides an index of the
documents,
presentations,
events,
code repositories,
and
publications
related to research and other activities associated with the
programme from June 2012 to December 2016.
The Index therefore effectively serves as a chronicle of the programme
for this period, covering the national expansion of the CERN@school Timepix detector
network, the launch of the Langton Ultimate Cosmic ray Intensity Detector (LUCID),
the TimPix project (part of ESA astronaut's Principia mission),
and the integration of CERN@school with the Monopole and Exotics Detector
at the LHC (MoEDAL) research programme.
Links and references to all relevant documents, presentations, code, and data
are provided where available.
The published document itself may be found here:

http://doi.org/10.5281/zenodo.227090


## Disclaimers
* _The code featured here dates from 2017. While every attempt has been
made to ensure that it is usable, some work may be required to get it
running on your own particular system.
We recommend using a GridPP CernVM; please refer to
[this guide](http://doi.org/10.6084/m9.figshare.4552825.v1)
for further instructions.
Unfortunately CERN@school cannot guarantee further support for this code.
Please proceed at your own risk_.
* _This repository is now deprecated, and remains here for legacy purposes.
For future work regarding CERN@school, please refer to the
[Institute for Research in Schools](http://researchinschools.org) (IRIS)
[GitHub repository](https://github.com/InstituteForResearchInSchools)._


## Getting the code
First, clone this repo into your working directory:

```bash
$ git clone https://github.com/CERNatschool/public-doc-index.git
$ cd public-doc-index
```


## Generating the document
Firstly, the individual Python scripts that run on the documents,
presentations, etc. have to be run on the JSON files
that contain the records. This can be done by running
the following script:

```bash
$ source make_material.sh
```

The LaTeX document can then be generated with:

```bash
$ source process.sh
```


## Licenses
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br />
All documentation in this repository,
except where otherwise noted,
is covered by a
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

All software in this repository,
except where otherwise noted (including the `*.sty`, `*.srt`, `*.bst`, etc. LaTeX files),
is covered by the MIT license (see `LICENSE`).


## Acknowledgements
CERN@school was supported by
the UK [Science and Technology Facilities Council](http://www.stfc.ac.uk) (STFC)
via grant numbers ST/J000256/1 and ST/N00101X/1,
as well as a Special Award from the Royal Commission for the Exhibition of 1851.
Please refer to the Acknowledgements section (Section 7, `ack.tex`)
for a full list of acknowledgements.


## Useful links
* [The Document Index on Zenodo](http://doi.org/10.5281/zenodo.227090);
* The [Institute for Research in Schools](http://researchinschools.org) (IRIS) homepage;
* The [IRIS CERN@school website](http://researchinschools.org/CERN);
* The [Official IRIS GitHub Organization](https://github.com/InstituteForResearchInSchools).
