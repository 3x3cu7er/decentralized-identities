import secrets
import string
import hashlib
import base64
import random
from getpass import getpass
import sys

PASSWD_LENGTH = 16

def create_passwd(pass_length):
    PASSWD = ""
    PUNCTUATION = string.punctuation
    DIGITS = string.digits
    ALPHA = string.ascii_letters

    RAND_CHAR = ALPHA+DIGITS+PUNCTUATION
    gen_passwd = PASSWD.join( secrets.choice(RAND_CHAR) for _ in range(PASSWD_LENGTH))

    return gen_passwd
    
passwd = create_passwd(PASSWD_LENGTH)


def md5_hash_passwd(passwd):
    
    md5 = hashlib.md5()
    md5.update(passwd.encode("ascii"))
    return md5.hexdigest()


def sha256_hash_passwd(passwd):
    sha256 = hashlib.sha256()
    sha256.update(passwd.encode("ascii"))
    return sha256.hexdigest()
    

def generate_username(name_of_user):
    # Constraints 
	minimum_capital_letter = 2
	minimum_specia_char = 2
	minimum_digits = 2
	min_len_of_username = 8
	special_chars = ['@','#','$','&']
    

	# variable to store generated username
	username = ""

	# remove space from name of user
	name_of_user = "".join(name_of_user.split())

	# convert whole name in lowercase 
	name_of_user = name_of_user.lower()

	# calculate minimum characters that we need to take from name of user 
	minimum_char_from_name = min_len_of_username-minimum_digits-minimum_specia_char

	# take required part from name 
	temp = 0
	for i in range(random.randint(minimum_char_from_name,len(name_of_user))):
		if temp < minimum_capital_letter:
			username += name_of_user[i].lower()
			temp += 1
		else:
			username += name_of_user[i]

	# temp_list to store digits and special_chars so that they can be shuffled before adding to username 
	temp_list=[]
	# add required digits 
	for i in range(minimum_digits):
		temp_list.append(str(random.randint(0,9)))

	# append special characters 
	for i in range(minimum_specia_char):
		temp_list.append(special_chars[random.randint(0,len(special_chars)-1)])

	# shuffle list 
	random.shuffle(temp_list)

	username += "".join(temp_list)
    
	return username









import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import time
# Download NLTK resources (if not already downloaded)
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('vader_lexicon')

# Load Spacy model for advanced NER
nlp = spacy.load("en_core_web_sm")

def process_identity_text_advanced(text):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize words and remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = [word_tokenize(sentence) for sentence in sentences]
    words = [word.lower() for word_list in word_tokens for word in word_list if word.isalnum() and word.lower() not in stop_words]
    
    # Perform Part-of-Speech Tagging
    pos_tags = pos_tag(words)
    
    # Perform Named Entity Recognition using NLTK
    named_entities_nltk = ne_chunk(pos_tags)
    
    # Extract named entities
    entities_nltk = []
    for entity in named_entities_nltk:
        if isinstance(entity, nltk.tree.Tree):
            entities_nltk.append(" ".join([word for word, tag in entity.leaves()]))
    
    # Perform Named Entity Recognition using SpaCy
    doc = nlp(text)
    entities_spacy = [ent.text for ent in doc.ents]
    
    # Calculate word frequency
    word_freq = FreqDist(words)
    
    # Perform Sentiment Analysis using VADER
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    
    return entities_spacy

# Example text related to identity issues
text = """
I'm John Smith, I was born in New York City in 1980. I studied at Harvard University and currently works at Google. 
I'm  facing identity theft issues as someone has been using his social security number to open fraudulent accounts.
"""


# Process the advanced identity text
entities_spacy = process_identity_text_advanced(text)


name_of_user = entities_spacy[0]


