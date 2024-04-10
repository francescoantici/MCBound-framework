from sklearn.neighbors import KNeighborsClassifier

from service.classification_model.classification_model import IClassificationModel

class KNN(IClassificationModel):
    
    name = "KNN"
    
    def __init__(self, **kwargs):
        self._model =  KNeighborsClassifier(**kwargs)