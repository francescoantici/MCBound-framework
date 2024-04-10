from typing import Literal

class IJobCharacteriser:
    
    TOP_PERF = None
    TOP_BM = None
    
    def __init__(self, labels_map:dict = {"memory-bound":0, "compute-bound":1}):
        self.ridge_op = self.TOP_PERF/self.TOP_BM
        self.lbl2idx = labels_map
        self.idx2lbl = {v:k for k, v in labels_map.items()}
        
    def characterise(self, p_j:float, mb_j:float, to_digit = False) -> Literal[Literal["compute-bound", "memory-bound"], Literal[0, 1]]:
        lbl = "compute-bound" if p_j/mb_j > self.ridge_op else "memory-bound"
        return self.lbl2idx[lbl] if to_digit else lbl
    
    def characterise_jobs(self, jobs_data:list, to_digit=False) -> list:
        pass
            

    