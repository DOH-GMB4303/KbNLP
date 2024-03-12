import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases




class Preprocesser:
    stop_words = stopwords.words('english')
    stop_words += ['null', 'data', ]


    @staticmethod
    def process(doc):
        if doc is None:
            return []
        doc = Preprocesser.clean_text(doc)
        doc = Preprocesser.get_n_grams(doc)
        return doc


    @staticmethod
    def clean_text(doc):
        doc = Preprocesser.lowercase_text(doc)
        doc = Preprocesser.remove_numbers(doc)
        doc = Preprocesser.remove_uninformative_numbers(doc)
        doc = Preprocesser.remove_one_char_words(doc)
        doc = Preprocesser.lemmatize(doc)
        doc = Preprocesser.remove_stop_words(doc)
        return doc

    @staticmethod
    def get_n_grams(doc):
        bigrams = Phrases(doc, min_count=5)
        trigrams = Phrases(bigrams[doc], min_count=2)
        doc += [bigram for bigram in bigrams[doc] if "_" in bigram]
        doc += [trigram for trigram in trigrams[doc] if "_" in trigram]
        return doc

    @staticmethod
    def lowercase_text(text):
        return text.lower()

    @staticmethod
    def remove_numbers(text):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(text)
    
    @staticmethod
    def remove_uninformative_numbers(text):
        return [token for token in text if not token.isnumeric()]
    
    @staticmethod
    def remove_one_char_words(text):
        return [token for token in text if len(token) > 1]

    @staticmethod
    def lemmatize(text):
        lmtzr = WordNetLemmatizer()
        return [lmtzr.lemmatize(token) for token in text]

    @staticmethod
    def remove_stop_words(text):
        return [token for token in text if token not in Preprocesser.stop_words]



if __name__ == "__main__":
    pass