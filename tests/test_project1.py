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
    assert len(input_files) == 1

def test_read_inputfiles(input):
    input_files=project1.input_file_name(input)
    for filename in input_files:
        sentences = project1.read_inputfiles(filename)
        assert len(sentences) == 12

def test_find_syn():
    concept = 'receipt'
    syn_list = ['receipt']
    syn_list.extend(project1.find_syn(concept))
    assert len(syn_list) == 37


def test_redact_sentence(input):
    input_files=project1.input_file_name(input)
    concept = 'receipt'
    #Testing for all flags
    flags=[1,1,1,1,1]
    final_count = [0,0,0,0,0,0]
    syn_list = []
    syn_list.extend(concept)
    syn_list.extend(project1.find_syn(concept))
    for filename in input_files:
        list_sentences = project1.read_inputfiles(filename)
        for sentence in list_sentences:
            redacted_sentence,count= project1.redact_sentence(sentence,syn_list, flags)
            final_count[0] = final_count[0] + count[0]
            final_count[1] = final_count[1] + count[1]
            final_count[2] = final_count[2] + count[2]
            final_count[3] = final_count[3] + count[3]
            final_count[4] = final_count[4] + count[4]
            final_count[5] = final_count[5] + count[5]
    assert final_count == [6,1,2,1,1,3]
