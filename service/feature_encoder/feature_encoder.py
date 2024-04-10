class IFeatureEncoder:
    
    def __init__(self) -> None:
        self._encoder = None
    
    def _parse_data(self, data):
        return data
    
    def encode(self, x:list) -> list:
        try:
            return self._encoder.encode(self._parse_data(x)) 
        except Exception as e:
            print(e)
            return []
            
