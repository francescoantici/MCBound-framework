from datetime import datetime

class IDataFetcher:
    
    def fetch(self, st:datetime = None, et:datetime = None) -> list:
        pass 
