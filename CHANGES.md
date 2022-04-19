#Changes

* Replacing the redacted word with redacted block of similar length instead of 1 redacted block for all substitutions.
* Added error handling in find_syn() function for beautiful soup when parsing synonyms from web.
* Added nltk wordnet in find_syn() function to cover more words for concept.
* Changed Gender regex to handle plural words and manage case sensitivity. 
* Added more regex to cover phone number formats.
* Changed name compairson from ent_type to label_ using spacy.
* Changed location of address redaction to before dateparser as dateparser consider 4 digits numbers as date and redacts them.
 
