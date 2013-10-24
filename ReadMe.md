# Notes on wp7datascripts #

## Background ##

This repository contains some of the many scripts developed during the [ViBRANT](http://vbrant.eu) project by work package 7, [Biodiversity literature access and data mining](http://vbrant.eu/content/wp7-biodiversity-literature-access-and-data-mining).

The scripts are released for general use under [GPLv2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt) in accordance with the project's formal description of work, Section _B 3.2 Plan for the use and dissemination of foreground_, sub-section _Software and training resources_:

> ViBRANT will adopt the IPR framework set in place under the EDIT FP6 project. All source
code generated through ViBRANT will be freely available under GNU General Public
Licence version 2.

## Contents ##

**Files**

brat_sorter.py
: Python 3 script to reorder entities in a brat stand-off file

call_ggws.php
: PHP script to invoke GoldenGATE web services. This sample uses the geolocation service to extract longitude and latitude from the embedded text. The script shows how to submit a request to GgWS and then repeatedly poll the service until the request is completed.

visualise.py
: Python 3 script to apply brat stand-off mark-up to its matching text file and produce a standalone HTML page to visualise the mark-up; accepts optional parameters to add navigation buttons to two other HTML pages, `prev` and `next`

**Folders**

call_gnrd
: How to call Global Names Recognition and Discovery, GNRD, running at the Oxford eResearch Centre, OeRC. Individual files are:

- `call_gnrd.py` - samples Python script to invoke the service
- `call_gnrd_sample.txt` and `call_gnrd_sample_big.txt` are two sample texts to use with the script
- `call_gnrd_sample_results.json` and `call_gnrd_sample_big_results.json` are the output from running the script to compare your results against; the script writes its output to `call_gnrd_sample.json` and `call_gnrd_sample_big.json`

## Licence ##

This software is released under GNU General Public Licence version 2. A copy of the licence is included in this folder.
 