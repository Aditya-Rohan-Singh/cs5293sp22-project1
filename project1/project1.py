import glob
import spacy
import re
from dateparser.search import search_dates

nlp = spacy.load('en_core_web_sm')

def input_file_name(type):
    input_files=glob.glob(type)
    return(input_files)

def read_inputfiles(input):
    with open(input) as f:
            
        lines=f.read().replace('\n','. ')
        sentences = list(map(str.strip, lines.split(". ")))
        sentences = list(filter(None,sentences))
        print(sentences)
        return(sentences)
    f.close()

def redact_sentence(sentence):
    
    #Remove 10 digit phone numbers
    sentence = re.sub(r'\d{10}','\u2588',sentence)
    
    #Remove dates
    matches = search_dates(sentence)
    if matches is not None:
        for x in matches:
            sentence = re.sub(x[0],'\u2588',sentence)

    #Removes names
    doc = nlp(sentence)
    redacted_sentence = []
    for token in doc:
        if token.ent_type_ == 'PERSON' or token.ent_type == 'GPE' or token.ent_type == 'DATE' or token.ent_type == 'ORG':
            redacted_sentence.append('\u2588')
            redacted_sentence.append(' ')
        else:
            redacted_sentence.append(token.text)
            redacted_sentence.append(' ')
    final_sentence = "".join(redacted_sentence)
    return(final_sentence)

if __name__ == '__main__':
    input_files=input_file_name('*.txt')
    for filename in input_files:
        list_sentences = read_inputfiles(filename)
        for single_sentence in list_sentences:
            redacted_sentence = redact_sentence(single_sentence)
            print(redacted_sentence)
            
