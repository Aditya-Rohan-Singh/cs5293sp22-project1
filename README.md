# -cs5293sp22-project1
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

Command To execute Pytest:
==========================
pipenv run python -m pytest


