from kbnlp.util.logging.logger import init_logger
init_logger()
from kbnlp.preprocess.fetcher import SPFetch
import kbnlp.configs as cfg
import kbnlp.model.corpus as corp





if __name__ == '__main__':
    corpus = corp.DocCorpus()
    for doc in corpus:
        pass




