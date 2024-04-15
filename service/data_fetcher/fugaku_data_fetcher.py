from datetime import datetime
import pandas as pd

from service.data_fetcher.data_fetcher import IDataFetcher

class FugakuDataFetcher(IDataFetcher):
    """_summary_

    Due to privacy concerns, the implementation of this class cannot be released.
    """
    
    def __init__(self, **args):
        pass
    
    def fetch(self, st: datetime = None, et: datetime = None, feat:str = "adt") -> list:
        return []