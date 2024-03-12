import logging
from datetime import datetime as dt
from dataclasses import dataclass, field
import json

import kbnlp.configs as cfg


@dataclass
class AppProfile:
    start_time: str = field(default=dt.now(), repr=False)
    end_time: str = field(default=None, repr=False)

    documents_processed: int = field(default=0)

    def __post_init__(self):
        pass


def jsonify(dict, path, overwrite=False):
    mode = "ab"
    if overwrite:
        mode = "wb"
    with open(path, mode) as fp:
        json.dump(dict, fp)


def dictify(path):
    with open(path, "rb") as fp:
        return json.load(fp)


def tsvify(tuple, path, overwrite=False):
    import pandas as pd

    mode = "ab"
    if overwrite:
        mode = "wb"
    row = pd.Series(tuple)
    row.to_csv(path, mode=mode, header=False, sep="\t")


def pkl(obj, path):
    import pickle

    with open(path, "ab+") as fp:
        pickle.dump(obj, fp)


def unpkl(path):
    import pickle
    with open(path, "rb") as fp:
        try:
            while True:
                yield pickle.load(fp)
        except EOFError:
            raise EOFError

            
if __name__ == "__main__":
    AP = AppProfile()
