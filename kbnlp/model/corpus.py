from kbnlp.preprocess.fetcher import SPFetch
from kbnlp.util.utils import pkl
import kbnlp.configs as cfg

from gensim import corpora
import logging

print(__name__)

# logging
logger = logging.getLogger(__name__)


class DocCorpus:
    """
    Corpus class for gensim models to use as input data source
        fetcher: SPFetch object
    """

    def __init__(self):
        self.fetcher = SPFetch()
        # Loop through tokens and add to dictionary
        if cfg.DICTIONARY_PATH.exists():
            self.dictionary = corpora.Dictionary.load(cfg.DICTIONARY_PATH.as_posix())
            logger.info("Dictionary loaded from file")
        else:
            self.dictionary = self.generate_dict()
            logger.info("Dictionary generated and saved to file")

        if cfg.CORPUS_PATH.exists():
            self.corpus = corpora.MmCorpus(cfg.CORPUS_PATH.as_posix())
            logger.info("Corpus loaded from file")
        else:
            self.corpus = []
            logger.info("Corpus generated and saved to file upon iteration")

        self.word_frequency_dict = self.generate_word_frequency()

    def __iter__(self):
        """Iterate through the fetcher's tokens"""
        import pickle

        if self.corpus != []:
            for doc in self.corpus:
                yield doc
        else:
            with open(cfg.DOCTOKEN_CACHE_PATH, "rb") as f:
                while True:
                    try:
                        tks = pickle.load(f)
                        # Transform words to ids
                        tks = self.dictionary.doc2bow(tks)
                        self.corpus.append(tks)
                        yield tks
                    except EOFError:
                        # Save corpus to file when done iterating
                        print("saving corpus")
                        self.save_corpus()
                        break

    def generate_dict(self):
        """Generate a dictionary from the fetcher's tokens/docs"""
        # Load dictionary from file if it exists
        if cfg.DICTIONARY_PATH.exists():
            return corpora.Dictionary.load(cfg.DICTIONARY_PATH.as_posix())
        # Otherwise, generate a new dict
        d = corpora.Dictionary()
        # Iterate through the fetcher object to yield one document at a time
        for tk_list in self.fetcher:
            d.add_documents([tk_list])
            pkl(tk_list, cfg.DOCTOKEN_CACHE_PATH)

        d.filter_extremes(no_below=2, no_above=0.9)
        d.compactify()
        d.save(cfg.DICTIONARY_PATH.as_posix())
        return d

    def save_corpus(self):
        """Save the corpus to a file"""
        corpora.MmCorpus.serialize(cfg.CORPUS_PATH.as_posix(), self.corpus)

    def to_numpy(self):
        '''Convert corpus to numpy array'''
        import numpy as np
        from gensim.matutils import corpus2dense
        return corpus2dense(self.corpus, num_terms=self.corpus.num_terms, num_docs=self.corpus.num_docs)
    @staticmethod
    def from_numpy(numpy_matrix):
        '''Convert numpy array to corpus'''
        import numpy as np
        from gensim.matutils import Dense2Corpus
        return Dense2Corpus(numpy_matrix)

    def generate_word_frequency(self):
        '''Get word frequency dictionary'''
        word_frequency_dict = {}
        for id1, freq in self.dictionary.dfs.items():
            for word, id2 in self.dictionary.token2id.items():
                if id1 == id2:
                    word_frequency_dict[word] = freq
        return word_frequency_dict

    def find_docs(self, word):
        '''Find documents containing a word'''
        return self.dictionary.dfs[word]


if __name__ == "__main__":
    dc = DocCorpus()
    for doc in dc:
        print(doc)

