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
            #data = re.sub("?:(\)", "\ ",data)
            lines=data.replace('\n','. ')
            sentences = list(map(str.strip, lines.split(". ")))
            sentences = list(filter(None,sentences))
            return(sentences,data)
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
            date_patterns = ['\d{10}','[(]\d{3}[)][-\.\s]*-[-\.\s]*\d{7}','[(]\d{3}[)][-\.\s]*-[-\.\s]*\d{3}[-\.\s]*-[-\.\s]*?\d{4}','\d{3}[-\.\s]*-[-\.\s]*\d{3}[-\.\s]*-[-\.\s]*\d{4}','\d{3} \d{3} \d{4}']
            reg1 = re.compile(r"\s*(?:(" + ")|(".join(date_patterns) + r"))")
            match1 = reg1.findall(sentence)
            if len(match1) > 0:
                for m in match1[0]:
                    if(len(m)>1):
                        red1 = '\u2588'*len(m) 
                        sentence = sentence.replace(m,red1)
                        #sentence, count = re.subn(m,red1,sentence)
                        stats_count[1] = stats_count[1] + 1
        
        #Remove address
        if(flags[4]==1):
            address_patterns = '(\d{1,6}[A-Za-z]?\s(?:[A-Za-z0-9#-]+\s){0,7}(?:[A-Za-z0-9#-]+,*)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,*)\s*[A-Z]{2}\s*\d{4,5})'
            match2 = re.findall(address_patterns,sentence)
            if len(match2)>0:
                for m in match2:
                    if(len(m)!=0):
                        red = '\u2588'*len(m)
                        sentence,count =re.subn(m,red,sentence)
                        stats_count[4] = stats_count[4] + count

        #Remove dates
        if(flags[1] == 1):
            matches = search_dates(sentence)
            if matches is not None:
                for x in matches:
                    rep = '\u2588'*len(x[0])
                    sentence = re.sub(x[0],rep,sentence)
                    stats_count[2] = stats_count[2] + 1

        #Remove gender related terms
        if(flags[3] == 1):
            matches =[]
            gender_terms=['Girl','chairwoman','chairman','lady','lord','goddess','god','herione','hero','fiancee','fiance','widow','widower','women','princess','prince','queen','king','herself','himself','grandmom','grandma','grandpa','bride','groom','sir','maam','ma','pa','granddaughter','grandmother','grandfather','brother','sister','gentleman','gentlemen','gentlewoman','girlfriend','boyfriend','spokesmen','spokeswoman','spokesman','guy','men','grandson','him','her','his','male','female','mother','father','aunt','uncle','niece','nephew','son','daughter','he','she','man','woman','boy','girl','husband','wife','actor','actress']
            #reg = re.compile(r"\b(?:(" + "(')?s?)|(".join(gender_terms) + r"))\b", flags=re.I)
            for term in gender_terms:
                reg=re.compile(r"\b((("+term+r")(')?(s)*))\b",flags=re.I)
                match = reg.findall(sentence.lower())#,re.IGNORECASE)
                if len(match) > 0:
                    for m in match[0]:
                        matches.append(m)
            for m in matches:
                if(len(m)>1):
                    red = ''
                    red = '\u2588'*len(m)
                    sentence,count = re.subn(m,red,sentence)
                    stats_count[3] = stats_count[3] + count
        
        #Removes names
        if(flags[0]==1):
            doc = nlp(sentence)
            for token in doc:
                if token.ent_type_ == 'Person':
                    rep ='\u2588'*len(token.text)
                    text = token.text
                    sentence, count = re.subn(text,rep,sentence)
                    stats_count[5] = stats_count[5] + count

            for token in doc.ents:
                if token.label_ == 'PERSON':
                    rep = '\u2588'*len(token.text)
                    text = token.text
                    sentence,count = re.subn(text,rep,sentence)
                    stats_count[5] = stats_count[5] + count
        #print(stats_count)
        return(sentence,stats_count)
    else:
        new_sentence = ''
        for i in sentence:
            if(i!='\n'):
                new_sentence = new_sentence + '\u2588'
            else:
                new_sentence = new_sentence + ' '
        #print(stats_count)
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
        for lemma in syn.hyponyms():
            synm = lemma.lemma_names()
            for x in synm:
                syn_list.append(x)
    #print(syn_list)
    return(syn_list)
