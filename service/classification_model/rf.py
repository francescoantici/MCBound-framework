from sklearn.ensemble import RandomForestClassifier

from service.classification_model.classification_model import IClassificationModel

class RF(IClassificationModel):
    
    name = "RF"
    
    def __init__(self, **kwargs):
        self._model = RandomForestClassifier(**kwargs)
    