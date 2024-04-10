from datetime import datetime
import pandas as pd

from service.data_fetcher.data_fetcher import IDataFetcher

class ParquetDataFetcher(IDataFetcher):
    
    def __init__(self, dfp:str):
        self._df = pd.read_parquet(dfp)
        
        self._df = self._df[self._df.elp != ""]
        self._df = self._df[self._df.perf3 != ""]
        self._df = self._df[self._df.perf2 != ""]
        self._df = self._df[self._df.idle_time_ave != ""]
        
        self._df["adt"] = pd.to_datetime(self._df.adt)
        self._df["sdt"] = pd.to_datetime(self._df.sdt)
        self._df["edt"] = pd.to_datetime(self._df.edt)
        
        self._df["day"] = self._df.adt.apply(lambda adt: adt.to_pydatetime().date())
        self._df["end_day"] = self._df.edt.apply(lambda edt: edt.to_pydatetime().date())
        self._df.elp = self._df.elp.astype(int)
        self._df.idle_time_ave = self._df.idle_time_ave.astype(float)
        self._df.nnuma = self._df.nnuma.astype(int)
        self._df["perf1"] = self._df.perf1.astype(float)
        self._df["perf2"] = self._df.perf2.astype(float)
        self._df["perf3"] = self._df.perf3.astype(float)
        self._df["perf4"] = self._df.perf4.astype(float)
        self._df["perf5"] = self._df.perf5.astype(float)
        self._df = self._df.fillna('')
    
    def fetch(self, st: datetime = None, et: datetime = None, feat:str = "adt") -> list:
        return self._df[(self._df[feat] >= st) & (self._df[feat] < et)].to_dict(orient="records")