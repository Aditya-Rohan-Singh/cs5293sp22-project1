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

Command: pipenv run python redactor.py --input <type of file (can be multiple)> --names --dates --phones --genders --address --concept <concept type (can be multiple)> --output <output file location> --stats <<filename/stdout/stderr>>


Argument Type:
=============

--input : Input file location and type of files. Can be multiple.

--names, --dates, --phones, --genders, --address : Type of data being redacted. No input values needed.

--Concept : Specific concept values being redacted. Can be multuple.

--output : Output location. It verifies if the location exists or not. Should be a valid location. Only single value can be given.

--stats : Either a file name or specialized file name (stdout or stderr). 

Command To execute Pytest:
==========================
pipenv run python -m pytest


Assumptions & Bugs:
==================

All the redacted values are being repaced by \u2588

1. The original structure of the document is not retained. All files are converted into a list of sentence and the redaction process happens sentence wise and then written into the file.
2. The usage of spacy does not assure 100% correctness. The library does not map everything to correct entity types always and some information might not get redacted correctly.
3. Below are the assumption and bugs for each argument type


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
All name types that spacy function tokenzie classifies as "Person" as entitype type is considered a name and redacted. There is some issue here as same name is being redacted and not redacted as well in the same email file. Spaces between names are not removed after being redacted.
Input
------
Multiple input file types can be given. It is considered that the input file type will have an extension. This is used to create the output redacted file names. Even without extension there should not be an issue.

Output
------
Outfile file location should be valid location. If the location does not exist the program will stop. The output files will be created in the given location with the .redacted name.

Stats
-----
The stats input value should either be a file name or "stdout"/ "stderr". If its a file name, then it will store values in a file at the current directory location. If its stdout or stderr, it will print the output on commandline.


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

redact_sentences(sentence, syn_list,flags)
-----------------------------------
=> It has a sentence of the input file and the synonym list as input arguments.

=> If any word in the synonym list is found in the sentence. The whole sentence is redacted and returned. Otherwise the code processes to individual redaction.

=> Keeps a count of synonym matches even if the sentence is redacted.

=> Based on the flag value it will check if the specific value needs to be redacted or not

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
=> Import all the functions from project1.py

"__main__"
---------
=> Arguments input, concept, output and stats are given with values.

=> Arguments names, gender, dates, addrerss and phone number are passed without any values.

=> All the above arguments are required for the code to go forward.

=> If the output location exists, then the code proceeds otherwise sends error message and stops.
 

main(input,output,concepts,stats)
---------------------------------

=> Prints the output folder locations

=> Open the stats file in write mode if the stat argument is a file name.

=> Iterates through the list of concept inputs and calls the imported find_syn() function to get a list of synonyms. Creates a single list of synonyms for all list of concepts.

=> Iterates through the list of input values.

=> Calls the imported input_file_name() which returns a list of filenames based on the input value.

=> If there are no files under the input value, returns values no files found and moves to next input value.

=> If Files found under input value, iterates through each filename from the list of filenames.

=> Uses the filename to create the output file name with .redacted extension.

=> Call imported function read_inputfile which converts the input filename into a list of sentences.

=> Check if the list of sentences is empty or not. If empty then no redaction needed. Otherwise the progam proceeds.

=> Add the output location to the new redacted file and open it in write mode.

=> Write the new file name into stats file if the stat argument is a file name otherwise prints it using stdout or stderr write function to command line.

=> It calls imported function redacted_sentence which returns the the redacted sentence with count of no. of differnt values that were redacted.

=> The sentence is written into the open redacted file. 

=> Add the count to the total count of the file

=> Close the file

=> Write the total count of redacted terms and their type for each file into the stats file if the stat argument is a file name otherwise prints it using stdout or stderr write function to command line.

=> Close the stats file if the stat argument is a file name.


Test Cases
==========

Input files : inputfile1.txt, inputfile2.txt, inputfile3.txt

Warnings can be ignored. Not sure how to fix them.

input()
-------
=> Made input_type "tests/ * .txt" as fixture (Remove spaces)

test_input_file_name(input):
---------------------------
=> Takes input_type as argument.

=> Function input_file_name() returns list of files under the input_type

=> Length of list of filenames checked to be 3 or not.

test_read_inputfiles(input):
---------------------------
=> Takes input_type as argument

=> Function input_file_name() returns list of files under the input_type

=> Each file name is iterated and function read_inputfiles() is called with filename as argument.

=> Each returns each file as a list of sentences.

=> Check if the returned list of sentences is greated than 0.

test_find_syn():
----------------
=> Define concept as 'Receipt'

=> calls function find_syn() with concept as argument.

=> Check if number of values returned with the concept is 31. Total synonyms is 30.

test_redact_sentence(input):
----------------------------
=> Takes input_type as argument

=> Function input_file_name() returns list of files under the input_type

=> Each file name is iterated and function read_inputfiles() is called with filename as argument.

=> Each returns each file as a list of sentences.

=> Each sentence is passed through the redacted_sentence function which returns a redacted sentence.

=> Check if the value of returned value is greater than 0. 
