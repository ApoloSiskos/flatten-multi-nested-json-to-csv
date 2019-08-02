import requests
import ast
import json
import urllib
import collections
import pandas as pd

data = [{"masterName":"AAAAA","mainNames":[{"numbers":[{"date":"2019-05-16T00:00:00Z","NumberOne":402,"NumberTwo":7830}],"name":"randomca"},{"numbers":[{"date":"2019-05-16T00:00:00Z","NumberOne":222,"NumberTwo":4015.31},{"date":"2019-05-31T00:00:00Z","NumberOne":192,"NumberTwo":3685.64}],"name":"randomka"},{"numbers":[],"name":"randomop"}]},{"masterName":"BBBBB","mainNames":[{"numbers":[],"name":"randomha"},{"numbers":[{"date":"2019-05-17T00:00:00Z","NumberOne":31,"NumberTwo":1500},{"date":"2019-05-31T00:00:00Z","NumberOne":236,"NumberTwo":31819.96}],"name":"randomba"}]}]

records = []

for item in data:                       
  for main in item["mainNames"]:                     
      for numbers in main["numbers"]:
          # Init new dict (df row) with "mainNames"
          sub_dict = {"masterName": item['masterName']}  
          # Add all fields from "numbers"
          sub_dict.update(numbers)     
          # Add "name" field                   
          sub_dict["name"] = main["name"]                 
          # append sud dict to list outputs
          records.append(sub_dict)   

df = pd.DataFrame(records)

#Export to CSV code can be added here
