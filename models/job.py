class Job:
    
    def __init__(self, username, job_name, core_number, node_number, env, freq_req): #**kwargs
        self.username = username 
        self.job_name = job_name
        self.core_number = core_number 
        self.node_number = node_number 
        self.env = env  
        self.freq_req = freq_req
        #self.__dict__.update(**kwargs)
                        
    @staticmethod
    def from_json(json):
        return Job(username=json["username"], job_name=json["job_name"], core_number=json["core_number"], node_number=json["node_number"], env=json["env"], freq_req=json["freq_req"])
    
    def __str__(self):
        d = self.__dict__
        return ",".join([str(d[k]) for k in d])            
    
    
    