import spacy
import re 

nlp = spacy.load('en_core_web_sm')

trails = ("classic")

sentence = "Turning \"Red\"s' Ball Scene Is An Instant Classic"
nlp_doc=nlp(sentence.lower())

# for x in nlp_doc :
#     if x.pos_ == "PROPN" or x.pos_ == "NOUN" or x.pos_ == "VERB":
#         print(x.orth_.replace('"', '\''))

res = [x.orth_.replace('"', '\'') for x in nlp_doc if x.pos_ == 'PROPN' or x.pos_ == 'NOUN' or x.pos_ == 'VERB']
_list = re.split(r'classic', ' '.join(res))
print(_list)