from service.job_characteriser.job_characteriser import IJobCharacteriser

class FugakuJobCharacteriser(IJobCharacteriser):
    
    TOP_PERF = 3380
    TOP_BM = 1024
        
    def characterise_jobs(self, jobs_data:list, to_digit=False) -> list:
        parsed_data = list(map(lambda j: {"performance": (((((j["perf2"] + (j["perf3"] * 4)))/(j["elp"] - j["idle_time_ave"])))/j["nnuma"])/1e9, "mem_bandwidth": (((((j["perf4"]+j["perf5"]))*(256/8))/(j["nnuma"]))/(2**30))/(j["elp"] - j["idle_time_ave"])}, jobs_data))
        return list(map(lambda jd: self.characterise(jd["performance"], jd["mem_bandwidth"], to_digit), parsed_data)) 