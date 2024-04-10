from sentence_transformers import SentenceTransformer

from service.feature_encoder.feature_encoder import IFeatureEncoder

class SBEncoder(IFeatureEncoder):
    
    FEATURES = ["usr", "jnam", "cnumr", "nnumr", "cr_jobenv_req", "cr_freq_req"]
    
    def __init__(self, weights = "all-MiniLM-L6-v2") -> None:
       self._encoder = SentenceTransformer(weights)
    
    def _parse_data(self, data):
        parser = lambda d: ",".join([str(d[k]) for k in self.FEATURES])    
        return list(map(parser, data))