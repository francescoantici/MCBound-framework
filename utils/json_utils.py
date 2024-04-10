import os 
import json 

read_json = lambda jp: json.load(open(jp, "rb"))

write_json = lambda obj, jp: json.dump(obj, open(jp, "wb"))