import pandas as pd

df =pd.read_csv("cleaned_data.csv")
for i in range(1,6):
    df = pd.get_dummies(df, columns=['radiant_player_'+str(i)+'_position'], prefix='radiant_player_'+str(i)+'position')

for i in range(1,6):
    df = pd.get_dummies(df, columns=['dire_player_'+str(i)+'_position'], prefix='diret_player_'+str(i)+'position')

for i in range(1,125):
    df[i]="0"

df =df.copy()
for i in df.iterrows():
    for j in range(1,6):
        df.at[i[0],i[1]['radiant_player_'+str(j)+'_hero']] = 1
        df.at[i[0],i[1]["dire_player_"+str(j)+'_hero']] = -1


for j in range(1,6):
        df.pop("radiant_player_"+str(j)+'_hero')
        df.pop("dire_player_"+str(j)+'_hero')

df.to_csv('cleaned_data_with_encoding.csv', index=False)