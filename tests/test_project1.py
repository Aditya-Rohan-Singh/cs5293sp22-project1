import sys
import os.path
working_directory = os.getcwd()
project0_path = working_directory + '/project1'
sys.path.append(project0_path)
import project1
from project1 import project1
import pytest

@pytest.fixture()
def input():
    input_type = "tests/*.txt"
    return(input_type)

def test_input_file_name(input):
    input_files=project1.input_file_name(input)
    assert len(input_files) == 3

def test_read_inputfiles(input):
    input_files=project1.input_file_name(input)
    for filename in input_files:
        sentences = project1.read_inputfiles(filename)
        assert len(sentences) > 0

def test_find_syn():
    concept = 'receipt'
    syn_list = ['receipt']
    syn_list.extend(project1.find_syn(concept))
    assert len(syn_list) == 31


def test_redact_sentence(input):
    input_files=project1.input_file_name(input)
    concept = 'receipt'
    syn_list = []
    syn_list.extend(concept)
    syn_list.extend(project1.find_syn(concept))
    for filename in input_files:
        list_sentences = project1.read_inputfiles(filename)
        for sentence in list_sentences:
            redacted_sentence,count_concept,count_phone,count_date,count_gender,count_address,count_name = project1.redact_sentence(sentence,syn_list)
            assert len(redacted_sentence) >0
