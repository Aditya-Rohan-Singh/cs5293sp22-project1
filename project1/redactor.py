
import argparse
import re
import os.path
from project1 import input_file_name, read_inputfiles, redact_sentence

def main(input,output):
    print("Output Folder Location:",output,"\n\n")
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
                print("Filename: ",filename)
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
                    for single_sentence in list_sentences:
                        redacted_sentence = redact_sentence(single_sentence)
                        write_file.write(redacted_sentence)
                        write_file.write('\n')
                        #print(redacted_sentence)
                    write_file.write('\n')
                    write_file.close()
                    print("Redacted File Name:",new_filename,"\n\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Program to redact documents")
    parser.add_argument("--input", type=str, required=True, action='append', help="Type of Input files")
    parser.add_argument("--output", type=str, required=True,  help="Location of output files")
    args = parser.parse_args()
    if args.input and args.output:
        if os.path.exists(args.output):
            main(args.input,args.output)
        else:
            print("Output path does not exists. Please provide correct path")
