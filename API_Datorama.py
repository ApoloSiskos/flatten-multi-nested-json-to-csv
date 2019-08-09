import datorama
import requests
import ast
import json
import urllib
import collections
import pandas as pd
import urllib2

#Post request to get token
try:
    req = urllib.request.Request("https://login.random.co/connect/token")

    req.add_header("Connection", "Keep-Alive")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("Accept", "application/json")
    req.add_header("Authorization", "Basic xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    body = b"grant_type=password&username=xxxxxx&password=yyyyyyyyyyyy&scope=mediasoft.api.external"

    response = urllib.request.urlopen(req, body)
    result = response.read()

    #Convert bytes to dictionary
    token_returned = ast.literal_eval(result.decode('utf-8'))
    token = list(token_returned.values())[0]

except:
    print('False')

#Get request to retrieve the JSON file
try:
    req = urllib.request.Request("https://random.digital/external/api/Metrics?from=2019-05-01&to=2019-07-22")

    req.add_header("Connection", "keep-alive")
    req.add_header("Authorization", "Bearer "+str(token)) #token
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3")
    req.add_header("Accept-Encoding", "deflate, br")
    req.add_header("Accept-Language", "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7")

    response = urllib.request.urlopen(req)
    '''response = urllib2.urlopen(req)
    response_str = response.read().decode('utf-8')
    response_json = json.loads(response_str)'''
    data_temp = response.read()
    #Convert byte type to JSON format
    my_json = data_temp.decode('utf8').replace("'", '"')

    # JSON parsed
    null = None
    temp_json = json.loads(my_json)
    if len(temp_json) > 0:
        if len(temp_json['clients'][0]['brands']) > 0:
            print('json not empty check') #return message that json is empty
        else:
            print('json empty') #continue manipulating the json    

except:
    print('False')


req = urllib2.Request("http://apolosiskos.co.uk/data.json")
response = urllib2.urlopen(req)
response_str = response.read().decode('utf-8')
response_json = json.loads(response_str)

temp_json=response_json

mid_step = json.loads(json.dumps(temp_json[0]['clients'][0]['brands'][0]['campaigns']))

#Function that converts date (key) to a value in the dictionary of metrics
def change_keys(d):
    for k, v in d.items():
        if k=='metrics':
            new_v = []
            for kk, vv in v.items():
                new_v.append({'date': kk})
                new_v[-1].update(**vv)
            second_step = {'metrics':new_v}
            d2 = d.copy()
            del d2['metrics']
            second_step.update(**d2)
            return second_step
    return d

final_step = json.loads(json.dumps(mid_step), object_hook=change_keys)

records = []

for item in final_step:                       
  for main in item["placements"]:                     
      for metrics in main["metrics"]:
          # Init new dict (df row) with "mainNames"
          sub_dict = {"campaignName": item['campaignName']}  
          # Add all fields from "metrics"
          sub_dict.update(metrics)     
          # Add "placementName" field                   
          sub_dict["placementName"] = main["placementName"]                 
          # append sud dict to list outputs
          records.append(sub_dict)   

df = pd.DataFrame(records)

# Generating a list of values for our headers' row 
row_values_list = list(df.columns.values)

# Writing a new row to the csv input file from values list 
datorama.add_row(row_values_list) 

# Creating a list of the two rows we want to write at once 
multiple_rows = list(map(list, df.values))

# Writing several rows at once to the csv by sending a list of multiple values' lists 
datorama.add_rows(multiple_rows) 

# Saving the csv file to upload it to our data stream 
datorama.save() 
