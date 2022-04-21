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
        assert len(sentences) == 13

def test_find_syn():
    concept = 'receipt'
    syn_list = ['receipt']
    syn_list.extend(project1.find_syn(concept))
    assert len(syn_list) == 37


def test_redact_sentence(input):
    input_files=project1.input_file_name(input)
    concept = 'receipt'
    #Flags describe the flags passed in the command line. [Name,Dates,Phones,Genders,Address]. For value 1 the flag is being used, 0 means its not being used.
    #Testing for all flags
    flags=[1,1,1,1,1]
    #Testing for Dates, Phones, Genders, Address
    flag1=[0,1,1,1,1]
    #Testing for Names, Genders, Address
    flag2=[1,0,0,1,1]
    
    final_count = [0,0,0,0,0,0]
    final_count1 = [0,0,0,0,0,0]
    final_count2 = [0,0,0,0,0,0]
    syn_list = ['receipt']
    syn_list.extend(project1.find_syn(concept))
    for filename in input_files:
        list_sentences = project1.read_inputfiles(filename)
        for sentence in list_sentences:
            redacted_sentence,count= project1.redact_sentence(sentence,syn_list, flags)
            redac_sen, count1 = project1.redact_sentence(sentence,syn_list,flag1)
            red_sen, count2 = project1.redact_sentence(sentence,syn_list,flag2)
            print(count)
            #count of redacted type[Concept, Phone NUmbers, Date, gender, address,name]
            for i in range(len(final_count)):
                final_count[i] = final_count[i] + count[i]
                final_count1[i] = final_count1[i] + count1[i]
                final_count2[i] = final_count2[i] + count2[i]
                
    assert final_count == [6,1,2,5,2,3]
    assert final_count1 == [6,1,2,5,2,0]
    assert final_count2 == [6,0,0,6,2,3]

