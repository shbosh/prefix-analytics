# clean text
import re
import string
import nltk

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction import text

class Preprocess:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.remove_list = stopwords.words('english')
        #self.remove_list.remove('no')
        self.remove_list += ['please', 'thank', 'pacific', 'canada',
        'none', 'florida', 'cst', 'tue', 'mon', 'wed', 'thu', 'fri', 'sat', 'monday', 'tuesday', 'wednesday', 'thursday','friday', 'saturday', 'sunday',
        'sun', 'cd', 'gmt', 'hw', 'sw', 'sg', 'error', 'still', 'need', 'call', 'service','customer', 'yesterday', 'today', 'year', 'yet', 'now', 'okay', 'spoke', 'spoken', 'no', 'benjamin', 'matthew', 'susan','jean', 'jason', 'hanelle', 'jan', 'feb', 'march', 'april', 'may','june', 'july', 'august', 'september', 'october', 'november', 'december']
        self.spelling_map = {
            'gantri': 'gantry',
            'gantree': 'gantry',
            'ystem': 'system',
            'patietn': 'patient',
            'patint': 'patient',
            'dispacth': 'dispatch',
#             'paramaters': 'parameters',
#             'reoboot': 'reboot',
#             'seperated': 'separated',
#             'x_ray': 'xray',
#             'probleme': 'problem',
#             'reformations': 'reformat',
#             'reformatts': 'reformat',
#             'reconstruit': 'reconstruct',
#             'reconstuctuion': 'reconstruction',
#             'refreash': 'refresh',
#             'roblems': 'problems',
#             'malfuntion': 'malfunction',
#             'messgae': 'message',
#             'maximun': 'maximum',
#             'keybord': 'keyboard',
#             'intercome': 'intercom',
#             'injectror': 'injector',
#             'proceeed': 'proceed',
#             'protocals': 'protocol',
#             'protoclos': 'protocol',
#             'recitify': 'rectify',
#             'noisey': 'noisy',
#             'equiipment': 'equipment'

        }

    def process_text(self, text):
        comp = re.compile(r'Image:[\S]*')
        text = comp.sub('', text)
        comp = re.compile(r'CD\W\w\w\w\W.*\d\d\d\dCST')
        text = comp.sub('', text)
        terms = self.tokenize(self.clean_text(text).lower().strip())
        clean_terms = [self.spelling_map.get(term) or term for term in terms if term not in self.remove_list and len(term) > 1]
        stemmed_tokens = list(self.porter_stem(clean_terms))
        # remove weird punctuation and numbers and images
        return stemmed_tokens

    def clean_text(self, text):
        final_text = ''
        for i in text:
            if i == ' ':
                final_text += i
            elif not i.isalpha():
                final_text += ' '
            else:
                final_text += i
        return final_text

    def tokenize(self, text):
        terms = []
        # tokenize sentences before words
        sentences = nltk.sent_tokenize(text)
        for sent in sentences:
            terms += nltk.word_tokenize(sent)
        return terms

    def porter_stem(self, terms):
        for term in terms:
            yield self.stemmer.stem(term)
