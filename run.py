import json 
import pandas as pd

#Original multi-nested JSON
data = [
    {
        "masterName": "AAAAAAAAAAA",
        "mainNames": [
            {
                "numbers": [
                    {
                        "date": "2019-05-16T00:00:00Z",
                        "NumberOne": 402.0,
                        "NumberTwo": 7830.0
                    }
                ],
                "name": "randomca"
            },
            {
                "numbers": [
                    {
                        "date": "2019-05-16T00:00:00Z",
                        "NumberOne": 222.0,
                        "NumberTwo": 4015.31
                    },
                    {
                        "date": "2019-05-31T00:00:00Z",
                        "NumberOne": 192.0,
                        "NumberTwo": 3685.64
                    }
                ],
                "name": "randomka"
            },
            {
                "numbers": [],
                "name": "randomop"
            }
        ]
    },
    {
        "masterName": "BBBBB",
        "mainNames": [
            {
                "numbers": [],
                "name": "randomha"
            },
            {
                "numbers": [
                    {
                        "date": "2019-05-17T00:00:00Z",
                        "NumberOne": 31.0,
                        "NumberTwo": 1500.0
                    },
                    {
                        "date": "2019-05-31T00:00:00Z",
                        "NumberOne": 236.0,
                        "NumberTwo": 31819.96
                    }
                ],
                "name": "randomba"
            }
        ]
    }
]

#Creation of dictionary 
temp_data = {
"main": []
}

#Add the original data in the newly created dictionary. We will need the key ("main" in this case) later on.
for item in range(len(data)):
  temp_data['main'].append(data[item])

#Manipulate the arrays to get the mainNames and their masterName
df = pd.concat(
    [
        pd.concat([pd.Series(m) for m in t['mainNames']], axis=1) for t in temp_data['main']
    ], keys=[t['masterName'] for t in temp_data['main']]
)

#Manipulate the arrays to get the metrics for each masterName 
records = ({'teamname': d['masterName'], 'name': name['name'], **num_dct} 
           for d in data
           for name in d['mainNames'] for num_dct in name['numbers'] or [{}])

#Creation of a dataframe in pandas
df = pd.DataFrame(records)

#Chech if data exists in following columns
cols = ['teamname', 'name', 'date']
df=df[cols + df.columns[~df.columns.isin(cols)].tolist()]

print(df)
#Export to CSV
df.to_csv('stack.csv', sep=',', encoding='utf-8', index=False)

