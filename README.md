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

All the redacted values are being repaced by \u2588

1. The original structure of the document is not retained. All files are converted into a list of sentence and the redaction process happens sentence wise and then written into the file.
2. Below are the assumption and bugs for each argument type


Concept
-------
Only single word concept are being considered in the program. It cannot work for phrases. The program is scraping all synonyms of the word given as concepts from the internet using Beautiful Soup libraries.
All the words provided in concepts will have a common list of synonyms that will be used for comparison and if matches the sentence is redacted. please provide only words as input for stats.

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

Input
------
Multiple input file types can be given. It is considered that the input file type will have an extension. This is used to create the output redacted file names. Even without extension there should not be an issue.

Output
------
Outfile file location should be valid location. If the location does not exist the program will stop. The output files will be created in the given location with the .redacted name.

Stats
-----
The stats input value should either be the file names "stdout" or "stderr" or a file location should be provided. If its a valid file location, then a file with default name stdout will be created.


Project1.py
===========

input_file_name(type)
---------------------
=> Value provided in commandline as argument is passed as input argument to the fucntion. 

=> It uses glob library to file the list of files matching the input type and return list of file names.

read_inputfiles(filename)
-------------------------
=> With filename as input argument. 

=> It opens the file. Replaces all new line with a '.' and then splits it into a list of sentences.

=> Converts the file into a list of sentences that can be accessed one by one which is then returned.

redact_sentences(sentence, syn_list)
-----------------------------------
=> It has a sentence of the input file and the synonym list as input arguments.

=> If any word in the synonym list is found in the sentence. The whole sentence is redacted and returned. Otherwise the code processes to individual redaction.

=> Keeps a count of synonym matches even if the sentence is redacted.

=> It checks for 3 differnt formats of phone number and replaces them with redacted block. The formats and redacted block is mentioned in Assumptions.

=> Keeps a count of readcted phone numbers.

=> Uses search_dates() from dateparser library to find the differnt formats of dates in the sentences. Replaces it with redacted block if any found.

=> Keeps a count of redacted dates.

=> A list of gender related terms are compared with the sentence using regex to find if any matches. All matches are replaced with redacted block. 

=> Keeps a count of redacted gender terms.

=> Replaces any value matchcing the regex created from standardized postal address format with redacted block,

=> Keeps a count of redacted address.

=> Each sentence is tokenized using spacy library. For each token value, if the entity type is "Person" or "Date" or "Org" it is replaces.

=> Keeps a ocunt of all redacted token values. 

=> Returns the redacted sentence with a count of all redacted values and types.

find_syn(word)
-------------
=> Concept word is given as input argument.

=> Using Beautiful soup library, the site thesaurus.plus is used to scrap all the synonyms of the given word and appended into a list. 

=> After formatting the returned value, a list of words is returned to the main function.


Redactor.py
===========

__main__
---------
=> Arguments input, concept, output and stats are given with values.

=> Arguments names, gender, dates, addrerss and phone number are passed without any values.

=> All the above arguments are required for the code to go forward.

=> If the output location exists, then the code proceeds otherwise sends and error message and stops.

=> If a location is given as input in stats, it will create a file called stdout at the given location and calls the main function with input, output, concept and stat values as arguments.

=> If a name is given as input in stats, it checks if the name matches specialized file names and calls the main function with input, output, concept and stat values as arguments.

=> Otherwise program terminates with the respective error message. 

main(input,output,concepts,stats)
---------------------------------
 
