import json
import bson
import pandas as pd
import numpy as np

df= pd.read_csv('gmm_hero_strengths.csv')

hero_dict = {}

for index,rows in df.iterrows():
    attributes =[]
    for column in df.columns:
        if column != 'Hero':
            attributes.append(rows[column].item())
    
    hero_dict[str(rows['Hero'])] = attributes

json_data = json.dumps(hero_dict)

with open("json_list.txt","w") as file:
    file.write(json_data)


