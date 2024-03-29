
import argparse
import sys
import re
import os.path
working_directory = os.getcwd()
project1_path = working_directory + '/project1'
sys.path.append(project1_path)
from project1 import project1
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def main(input,output,concepts,stats,flags):
    string = "Output Folder Location:" + output + "\n\n"
    sys.stdout.write(string)
    #Opening Stats file
    if(stats != 'stdout' and stats != 'stderr'):
        std = open(stats,"w")
    
    #Creating Concept word list
    syn_list=[]
    concept_word = []
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(concepts[0])
    if len(word_tokens) > 1:
        for w in word_tokens:
            if w not in stop_words:
                concept_word.append(w)
        for word in concept_word:
            syn_list.append(word)
            syn_list.extend(project1.find_syn(word))
    else:
        #syn_list = []
        syn_list.extend(concepts)
        for concept in concepts:
            syn_list.extend(project1.find_syn(concept))

    #Loop to cycle through multiple input types
    for file_type in input:
        input_files=project1.input_file_name(file_type)

        #If case if there are no files under the input type
        if len(input_files) == 0:
            string = "No files found under input : " + file_type
            sys.stdout.write(string)
            sys.stdout.write("\n--------------------------\n\n")
        else:
            string = "Files found under input type: " + file_type
            sys.stdout.write(string)
            sys.stdout.write("\n-----------------------------")
            #Loop to cycle through each text file
            for filename in input_files:
                string = "\n\nFilename: " + filename
                sys.stdout.write(string)
                final_count = [0,0,0,0,0,0]

                new_filename = filename + '.redacted'
                list_sentences,raw_data = project1.read_inputfiles(filename)
                
                if len(list_sentences) == 0:
                    sys.stdout.write("Empty File. No Redaction Needed\n\n")
                else:
                    if(output[-1]=='/'):
                        output = output[:-1]
                    new_filename = new_filename.split('/')[-1]
                    file_location = output + "/" + new_filename
                    write_file = open(file_location,"w")
                    if(stats!="stdout" and stats!="stderr"):
                        std.write(new_filename)
                        std.write("\n-----------------\n")
                    for single_sentence in list_sentences:
                        redacted_sentence, stats_count = project1.redact_sentence(single_sentence,syn_list,flags)
                        raw_data = raw_data.replace(single_sentence,redacted_sentence)
                        final_count[0] = final_count[0] + stats_count[0]
                        final_count[1] = final_count[1] + stats_count[1]
                        final_count[2] = final_count[2] + stats_count[2]
                        final_count[3] = final_count[3] + stats_count[3]
                        final_count[4] = final_count[4] + stats_count[4]
                        final_count[5] = final_count[5] + stats_count[5]
                    write_file.write(raw_data)
                    write_file.write('\n')
                    write_file.close()
                    string = "\nRedacted File Name:" + new_filename
                    sys.stdout.write(string)
                    sys.stdout.write("\n\n")
                    stringdata1 = "Total concept related words: " + str(final_count[0]) + "\n"
                    stringdata2 = "Total Phone Numbers: " + str(final_count[1]) + "\n"
                    stringdata3 = "Total Date: " + str(final_count[2]) + "\n"
                    stringdata4 = "Total Gender: " + str(final_count[3]) + "\n"
                    stringdata5 = "Total address: " + str(final_count[4]) + "\n"
                    stringdata6 = "Total Name: " + str(final_count[5]) + "\n"
                    if(stats == "stdout" or stats == "stderr"):
                        if(stats == 'stdout'):
                            sys.stdout.write(stringdata1)
                            sys.stdout.write(stringdata2)
                            sys.stdout.write(stringdata3)
                            sys.stdout.write(stringdata4)
                            sys.stdout.write(stringdata5)
                            sys.stdout.write(stringdata6)
                        else:
                            sys.stderr.write(stringdata1)
                            sys.stderr.write(stringdata2)
                            sys.stderr.write(stringdata3)
                            sys.stderr.write(stringdata4)
                            sys.stderr.write(stringdata5)
                            sys.stderr.write(stringdata6)
                    else:
                        std.write(stringdata1)
                        std.write(stringdata2)
                        std.write(stringdata3)
                        std.write(stringdata4)
                        std.write(stringdata5)
                        std.write(stringdata6)
                        std.write("\n\n")
    if(stats != 'stdout' and stats != 'stderr'):
        std.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Program to redact documents")
    parser.add_argument("--input", type=str, required=True, action='append', help="Type of Input files")
    parser.add_argument("--names", action = 'store_true', required=False,  help="Redact Names")
    parser.add_argument("--dates", action = 'store_true', required=False,  help="Redact dates")
    parser.add_argument("--phones", action = 'store_true', required=False,  help="Redact phones")
    parser.add_argument("--genders", action = 'store_true', required=False,  help="Redact genders")
    parser.add_argument("--address", action = 'store_true', required=False,  help="Redact address")
    parser.add_argument("--concept", type=str, required=True, action='append', help="Type of Concept")
    parser.add_argument("--output", type=str, required=True,  help="Location of output files")
    parser.add_argument("--stats", type=str, required=True, help="File name for stats (stdout or stderr) or file location")
    args = parser.parse_args()
    if args.input and args.output and args.stats and args.concept:
        if os.path.exists(args.output):
            redaction_flags=[0,0,0,0,0]
            if(args.names):
                redaction_flags[0]=1
            if(args.dates):
                redaction_flags[1]=1
            if(args.phones):
                redaction_flags[2]=1
            if(args.genders):
                redaction_flags[3]=1
            if(args.address):
                redaction_flags[4]=1
            main(args.input,args.output,args.concept,args.stats,redaction_flags)
        else:
            print("Output path does not exists. Please provide correct path")
