import glob
import spacy
import re
from dateparser.search import search_dates
import warnings
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
#import en_core_web_md

warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)
nlp = spacy.load('en_core_web_sm')


def input_file_name(type):
    input_files=glob.glob(type)
    return(input_files)

def read_inputfiles(input):
    with open(input) as f:
            
        lines=f.read().replace('\n','. ')
        sentences = list(map(str.strip, lines.split(". ")))
        sentences = list(filter(None,sentences))
        return(sentences)
    f.close()

def redact_sentence(sentence,syn_list):
    #nlp = en_core_web_md.load()
    counter = 0
    count_phone = 0
    count_date = 0
    count_gender = 0
    count_name = 0
    count_address = 0

    #Redacting concepts
    count_concept = 0
    for word in syn_list:
        #sentence = re.sub(word,'\u2588',sentence)
        lenconcept = re.findall(word,sentence)
        if (len(lenconcept) > 0):
            counter = 1
            count_concept = count_concept + len(lenconcept)
    
    #If there are no concept words in the sentence.
    if(counter == 0):
    #Remove 10 digit phone number
        # for fromat xxxxxxxxxx
        sentence, count = re.subn(r'\d{10}','\u2588',sentence)
        count_phone = count_phone + count
        
        #for fromat (xxx)-xxxxxxx
        sentence, count = re.subn(r'[(]\d{3}[)]-\d{7}','\u2588',sentence)
        count_phone = count_phone + count
        
        #for format (xxx)-xxx-xxxx
        sentence,count = re.subn(r'[(]\d{3}[)]-\d{3}-\d{4}','\u2588',sentence)
        count_phone = count_phone + count
    
        #Remove dates
        matches = search_dates(sentence)
        if matches is not None:
            for x in matches:
                sentence = re.sub(x[0],'\u2588',sentence)
            count_date = len(matches)

        #Remove gender related terms
        gender_terms=['him','her','is','male','female','mother','father','aunt','uncle','niece','nephew','son','daughter','he','she','man','woman','boy','girl','husband','wife','actor','actress']
        for term in gender_terms:
            lengender = re.findall(r"\b" + re.escape(term) + r"\b", sentence.lower())
            if (len(lengender) > 0):
                sentence,count = re.subn(r"\b" + re.escape(term) + r"\b",'\u2588',sentence.lower())
                count_gender = count_gender + count
        
        #Remove address
        sentence, count = re.subn(r'\d{1,6}\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s*[A-Z]{2}\s*\d{5}',"\u2588",sentence)
        count_address = count_address + count

        #Removes names
        doc = nlp(sentence)
        redacted_sentence = []
        for token in doc:
            if token.ent_type_ == 'PERSON' or token.ent_type == 'DATE' or token.ent_type == 'ORG':
                redacted_sentence.append('\u2588')
                redacted_sentence.append(' ')
                count_name = count_name + 1
            else:
                redacted_sentence.append(token.text)
                redacted_sentence.append(' ')
        final_sentence = "".join(redacted_sentence)

        return(final_sentence,count_concept,count_phone,count_date,count_gender,count_address,count_name)
    else:
        final_sentence = '\u2588'
        return(final_sentence,count_concept,count_phone,count_date,count_gender,count_address,count_name)

def find_syn(word):
    stripped_string = word.strip()
    fixed_string = stripped_string.replace(" ", "_")
    my_url = f'https://thesaurus.plus/synonyms/{fixed_string}'

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")
    word_boxes = page_soup.find("ul", {"class": "list paper"})
    results = word_boxes.find_all("div", "list_item")
    syn_list = []
    for result in results:
        test = result.text.split('   ')
        string = re.sub('^ ','',test[1])
        syn_list.append(string)
    return(syn_list)

