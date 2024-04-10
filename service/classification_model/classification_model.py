import skops.io as sio
import os

class IClassificationModel:
    
    name = None
    
    def __init__(self):
        self._model = None
    
    def train(self, x: list, y: list) -> bool:
        try:
            self._model = self._model.fit(x, y)
        except Exception as e:
            print(e)
            return False 
        else:
            return True
    
    def predict(self, x: list) -> list:
        try:
            return self._model.predict(x)
        except Exception as e:
            print(e)
            return []
         
    def save(self, fp:str, stage = "prod") -> bool:
        try:
            sio.dump(self, os.path.join(fp, f"{self.name}_{stage}")) 
        except Exception as e:
            print(e)
            return False
        else:
            return True
    
    def update(self, fp:str, stage="prod") -> None:
        try:
            self = sio.load(os.path.join(fp, f"{self.name}_{stage}"), trusted=True)
        except Exception as e:
            print(e)
    
    @classmethod
    def from_saved_model(cls, fp:str, stage = "prod"):
        return sio.load(os.path.join(fp, f"{cls.name}_{stage}"), trusted=True)
    