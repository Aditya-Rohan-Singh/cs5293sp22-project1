#Changes

* Project1.py: redact_sentence(): Replacing the redacted word with redacted block of similar length instead of 1 redacted block for all substitutions.
* project1.py: find_syn(): Added error handling in find_syn() function for beautiful soup when parsing synonyms from web. Https error being thrown is resolved.
* project1.py: find_syn(): Added nltk wordnet in find_syn() function to cover more words for concept.
* project1.py: redact_sentence(): Changed Gender regex to handle plural words and manage case sensitivity. 
* project1.py: redact_sentence(): Added more regex to cover phone number formats.
* project1.py: redact_sentence(): Added name compairson from ent_type to label_ using spacy.
* project1.py: redact_sentence(): Changed location of address redaction to before dateparser as dateparser consider 4 digits numbers as date and redacts them.
* redactor.py: main(): Added code to handle string as input for concept. It strips the string into tokens, removes stopwords and appends all related words into a list of words that is used for comparison. 
* project1.py: find_syn(): Added hyponyms() for all words being passed to find_sym() to handle more concept words. 

* Just to clarify, I'm using flags to call reduction process. [Name,Dates,Phones,Genders,Address] is the list of flags. If the value is 1 then the flag is being called, if 0 then not being called.
* test_project1.py: Added 2 more test cases to check for different flags being passed. Comparing the count of redacted words with expected count of redacted words to test redaction process.
	* Testing just for Dates, Phones, Genders, Address. 
	* Testing just for Names, Genders, Address.
