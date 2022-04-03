cs5293sp22-project1
====================

Text Analytics - Project 1

Author: Aditya Rohan Singh

Email: aditya.rohan.singh-1@ou.edu

Libraries used: argparse, re, os.path, glob, spacy, dateparser, bs4, urllib

Libraries to insall: pytest, spacy, dateparser, bs4, click"==8.0.0"


Command to install the libraries:
=================================

pipenv install pytest

pipenv install spacy

python -m spacy download en_core_web_md

pipenv install 

pipenv install bs4

pipenv uninstall click

pipenv install click==8.0.0


Command to Execute Project1:
===========================

Location: ~/cs5293sp22-project1/project1/redactor.py

Command: pipenv run python redactor.py --input <type of file (can be multiple)> --names --dates --phones --genders --address --concept <concept type (can be multiple)> --output <output file location> --stats <<filename/location>>


Argument Type:
=============
--input : Input file location and type of files. Can be multiple.
--names, --dates, --phones, --genders, --address : Type of data being redacted. No input values needed.
--Concept : Specific concept values being redacted. Can be multuple.
--output : Output location. It verifies if the location exists or not. Should be a valid location. Only single value can be given.
--stats : Either location or file name (stdout or stderr). If the file location is not valid or the names are not either stdout or stderr, Program will stop.


Command To execute Pytest:
==========================
pipenv run python -m pytest


Assumptions & Bugs:
==================

1. The original structure of the document is not retained. All files are converted into a list of sentence and the redaction process happens sentence wise and then written into the file.
2. Below are the assumption and bugs for each argument type
Concept
-------
Only single word concept are being considered in the program. It cannot work for phrases. The program is scraping all synonyms of the word given as concepts from the net using Beautiful Soup libraries.
All the words provided in concepts will have a common list of synonyms that will be used for comparison and if matches the sentence is redacted.

Phone Number
------------
3 formats of phone numbers will be redacted. xxxxxxxxxx, (xxx)-xxxxxxx, (xxx)-xxx-xxxx. These were the most common types of phone formats. 

Dates
-----
Dateparser library is being used to find the list of dates in a particule sentence. It covers majority types of dates. It does also consider any 4 digit number as year as the format is YYYY. So digit values in that format is also getting redacted.

Gender
------
'him','her','is','male','female','mother','father','aunt','uncle','niece','nephew','son','daughter','he','she','man','woman','boy','girl','husband','wife','actor','actress' is the list of gender related terms being considered in the code. These words are being considered as gender related terms and being redacted in the code.

Address
--------
Postal address are very difficult to pindown on what could or what could not be an address. So all address in the folowing regular expression format are considered as address and redacted.
'\d{1,6}\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s*[A-Z]{2}\s*\d{5}

Name
----
All name types that spacy function tokenzie classifies as "Person" as entitype type is considered a name and redacted. There is some issue here as same name is being redacted and not redacted as well in the same email file.  
