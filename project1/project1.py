import glob
import spacy
import re
from dateparser.search import search_dates
import warnings
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
import en_core_web_md
import sys
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('omw-1.4')

warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)
nlp = en_core_web_md.load()

def input_file_name(type):
    input_files=glob.glob(type)
    return(input_files)

def read_inputfiles(input):
    with open(input) as f:
        try:
            data = f.read()
            lines=data.replace('\n','. ')
            sentences = list(map(str.strip, lines.split(". ")))
            sentences = list(filter(None,sentences))
            return(sentences)
    #f.close()
        except:
            print("Error while opening file: ",input)

def redact_sentence(sentence,syn_list,flags):
    counter = 0
    
    stats_count=[0,0,0,0,0,0]

    #Redacting concepts
    count_concept = 0
    for word in syn_list:
        lenconcept = re.findall(word,sentence)
        if (len(lenconcept) > 0):
            counter = 1
            count_concept = count_concept + len(lenconcept)
            stats_count[0] = stats_count[0] + len(lenconcept)
    
    #If there are no concept words in the sentence.
    if(counter == 0):
    #Remove 10 digit phone number
        # for fromat xxxxxxxxxx
        if(flags[2] == 1):
            
            sentence, count = re.subn(r'\d{10}','\u2588',sentence)
            stats_count[1] = stats_count[1] + count
        
        #for fromat (xxx)-xxxxxxx
            sentence, count = re.subn(r'[(]\d{3}[)]-\d{7}','\u2588',sentence)
            stats_count[1] = stats_count[1] + count

        #for format (xxx)-xxx-xxxx
            sentence,count = re.subn(r'[(]\d{3}[)]-\d{3}-\d{4}','\u2588',sentence)
            stats_count[1] = stats_count[1] + count
        #

        #Remove dates
        if(flags[1] == 1):
            matches = search_dates(sentence)
            if matches is not None:
                for x in matches:
                    sentence = re.sub(x[0],'\u2588',sentence)
                stats_count[2] = len(matches)

        #Remove gender related terms
        if(flags[3] == 1):
            gender_terms=['him','her','his','male','female','mother','father','aunt','uncle','niece','nephew','son','daughter','he','she','man','woman','boy','girl','husband','wife','actor','actress']
            reg = re.compile(r"\b(?:(" + "s?)|(".join(gender_terms) + r"))\b", flags=re.I)
            match = reg.findall(sentence)
            if match:
                for m in match[0]:
                    if(len(m)>1):
                        print(m)
                        red = ''
                        red = '\u2588'*len(m)
                        sentence,count = re.subn(m,red,sentence)
                        stats_count[3] = stats_count[3] + count
        
        #Remove address
        if(flags[4]==1):
            sentence, count = re.subn(r'\d{1,6}\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s*[A-Z]{2}\s*\d{5}',"\u2588",sentence)
            stats_count[4] = stats_count[4] + count

        #Removes names
        if(flags[0]==1):
            doc = nlp(sentence)
            redacted_sentence = []
            for token in doc:
                if token.ent_type_ == 'PERSON' or token.ent_type == 'ORG':
                    for i in range(len(token)):
                        redacted_sentence.append('\u2588')
                    redacted_sentence.append(' ')
                    stats_count[5] = stats_count[5] + 1
                else:
                    redacted_sentence.append(token.text)
                    redacted_sentence.append(' ')
            sentence = "".join(redacted_sentence)

        return(sentence,stats_count)
    else:
        new_sentence = ''
        for i in sentence:
            if(i!='\n'):
                new_sentence = new_sentence + '\u2588'
            else:
                new_sentence = new_sentence + ' '
        #print(new_sentence)
        
        return(new_sentence,stats_count)

def find_syn(word):
    stripped_string = word.strip()
    fixed_string = stripped_string.replace(" ", "_")
    my_url = f'https://thesaurus.plus/synonyms/{fixed_string}'
    syn_list = []    
    try:
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
        i = 0
        #return(syn_list)
    except OSError as ue:
        sys.stderr.write("The Server Could Not be Found")
    
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            syn_list.append(l.name())

    return(syn_list)
