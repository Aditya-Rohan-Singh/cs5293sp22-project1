import glob
import spacy
import boto3

client = boto3.client('comprehend')

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

def redact_sentences(sentence):
    response = client.detect_pii_entities(
                Text= sentence,
                LanguageCode='en'
    )
    clean_text = sentence
    for NER in reversed(response['Entities']):
        clean_text = clean_text[:NER['BeginOffset']] + NER['Type'] + clean_text[NER['EndOffset']:]
    return(clean_text)

if __name__ == '__main__':
    input_files=input_file_name('*.txt')
    for filename in input_files:
        list_sentences = read_inputfiles(filename)
        for single_sentence in list_sentences:
            redacted_sentence = redact_sentence(single_sentence)
            print(redacted_sentence)
