#Changes

* Majority functions were not being executed due to the HTTPS error while using beautiful soup library. Fixed that and added more changes for better results.


* Wrong redaction character or amount: 
	* Project1.py: redact_sentence(): Replacing the redacted word with redacted block of similar length instead of 1 redacted block for all substitutions.

* Redact sentence - Concept
	* project1.py: redact_sentence(): Redacts all the characters in the sentence with a uniblock chatacter.

* Output files not stored in respective folder: 
	* project1.py: find_syn(): Added error handling in find_syn() function for beautiful soup library when parsing synonyms from web. Https error being thrown is resolved which was causing issue for the output files to be generated.
	* project1.py: read_files(): Returns raw data as well to the redactor.main().

* Missing/No Features Found- Names
	* project1.py: redact_sentence(): Added name compairson using label_ using spacy.

* Missing/No Features - Addresses
	* project1.py: redact_sentence(): Changed regex to handle specfic formats of address based on US postal addresses found online.

* Small amount of Features Found - Concept
	* project1.py: find_syn(): Added nltk wordnet in find_syn() function to cover more words for concept.
	* project1.py: find_syn(): Added hyponyms() for all words being passed to find_sym() to handle more concept words.
	* redactor.py: main(): Added code to handle string as input for concept. It strips the string into tokens, removes stopwords and appends all related words into a list of words that is used for comparison.
* Missing/No Features Found - Gender
	* project1.py: redact_sentence(): Changed Gender regex to handle plural words and manage case sensitivity. 

* Missing/No Features Found- Phone Number
	* project1.py: redact_sentence(): Added more regex to cover phone number formats.

* Missing/No Features Found - Dates
	* project1.py: redact_sentence(): Changed location of address redaction to before dateparser as dateparser consider 4 digits numbers as date and redacts them.

* Other Changes
	* redactor.py: main(): Writing redacted data as a whole into output file instead of sentences to fix formatting. 
	* project1.py: read_files(): Returns raw data as well to the redactor.main().


* Clarification: I'm using flags to call reduction process. [Name,Dates,Phones,Genders,Address] is the list of flags. If the value is 1 then the flag is being called, if 0 then not being called.

* Missing Test Functions
	* test_project1.py: Added 2 more test cases to check for different flags being passed. Comparing the count of redacted words with expected count of redacted words to test redaction process.
		* Testing just for Dates, Phones, Genders, Address. 
		* Testing just for Names, Genders, Address.
