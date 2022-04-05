
import argparse
import sys
import re
import os.path
from project1 import input_file_name, read_inputfiles, redact_sentence, find_syn

def main(input,output,concepts,stats):
    print("Output Folder Location:",output,"\n\n")
    print("stats: ",stats,"\n\n") 
    #Opening Stats file
    if(stats != 'stdout' or stats != 'stderr'):
        std = open(stats,"w")
    
    #Creating Concept word list
    syn_list = []
    syn_list.extend(concepts)
    for concept in concepts:
        syn_list.extend(find_syn(concept))
    print("Concept Words: ",len(syn_list),"\n\n")
    
    #Loop to cycle through multiple input types
    for file_type in input:
        input_files=input_file_name(file_type)

        #If case if there are no files under the input type
        if len(input_files) == 0:
            print("No files found under input : ",file_type)
            print("--------------------------\n\n")
        else:
            print("Files found under input type: ",file_type)
            print("-----------------------------")
            #Loop to cycle through each text file
            for filename in input_files:
                print("\n\nFilename: ",filename)
                final_count_concept = 0
                final_count_phone = 0
                final_count_date = 0
                final_count_gender = 0
                final_count_name = 0
                final_count_address = 0
                if re.search('.',str(filename)):
                    new_filename = filename.split('.')[0] + '.redacted'
                else:
                    new_filename = filename + '.redacted'
                list_sentences = read_inputfiles(filename)
                if len(list_sentences) == 0:
                    print("Empty File. No Redaction Needed\n\n")
                else:
                    file_location = output + "/" + new_filename
                    print(file_location)
                    write_file = open(file_location,"w")
                    if(stats!="stdout" and stats!="stderr"):
                        std.write(new_filename)
                        std.write("\n-----------------\n")
                    for single_sentence in list_sentences:
                        redacted_sentence,count_concept,count_phone,count_date,count_gender,count_address,count_name = redact_sentence(single_sentence,syn_list)
                        write_file.write(redacted_sentence)
                        write_file.write('\n')
                        final_count_concept = final_count_concept + count_concept
                        final_count_phone = final_count_phone + count_phone
                        final_count_date = final_count_date + count_date
                        final_count_gender = final_count_gender + count_gender
                        final_count_address = final_count_address + count_address
                        final_count_name = final_count_name + count_name
                        #print(redacted_sentence)
                    write_file.write('\n')
                    write_file.close()
                    print("Redacted File Name:",new_filename,"\n\n")
                    stringdata1 = "Total concept related words: " + str(final_count_concept) + "\n"
                    stringdata2 = "Total Phone Numbers: " + str(final_count_phone) + "\n"
                    stringdata3 = "Total Date: " + str(final_count_date) + "\n"
                    stringdata4 = "Total Gender: " + str(final_count_gender) + "\n"
                    stringdata5 = "Total address: " + str(final_count_address) + "\n"
                    stringdata6 = "Total Name: " + str(final_count_name) + "\n"
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
    if(stats != 'stdout' or stats != 'stderr'):
        std.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Program to redact documents")
    parser.add_argument("--input", type=str, required=True, action='append', help="Type of Input files")
    parser.add_argument("--names", action = 'store_true', required=True,  help="Redact Names")
    parser.add_argument("--dates", action = 'store_true', required=True,  help="Redact dates")
    parser.add_argument("--phones", action = 'store_true', required=True,  help="Redact phones")
    parser.add_argument("--genders", action = 'store_true', required=True,  help="Redact genders")
    parser.add_argument("--address", action = 'store_true', required=True,  help="Redact address")
    parser.add_argument("--concept", type=str, required=True, action='append', help="Type of Concept")
    parser.add_argument("--output", type=str, required=True,  help="Location of output files")
    parser.add_argument("--stats", type=str, required=True, help="File name for stats (stdout or stderr) or file location")
    args = parser.parse_args()
    if args.input and args.output and args.stats and args.concept:
        if os.path.exists(args.output):
            main(args.input,args.output,args.concept,args.stats)
        else:
            print("Output path does not exists. Please provide correct path")
