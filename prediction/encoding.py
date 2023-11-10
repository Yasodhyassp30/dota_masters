import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df =pd.read_csv("cleaned_data.csv")
df = df[df['match_duration_seconds']>2400]

print(len(df))
total = []
for i in range(1,6):
    
    unique = df['radiant_player_'+str(i)+'_id'].unique()
    
    unique2 = df['dire_player_'+str(i)+'_id'].unique()

    combined = list(unique)+list(unique2)
    total +=combined

unique_df = pd.DataFrame({'Unique_Values': total})
unique_values = unique_df['Unique_Values'].unique()

unique_df = pd.DataFrame({'Unique_Values': unique_values})
for i in range(1,6):
     for index,row in unique_df.iterrows():
          matching_values = df[df['radiant_player_'+str(i)+'_id'] == row['Unique_Values']]
          average_value = matching_values.mean()['radiant_player_'+str(i)+'_networth']
          df.loc[df['radiant_player_'+str(i)+'_id'] == row['Unique_Values'], 'radiant_player_'+str(i)+'_networth'] = average_value
          matching_values = df[df['dire_player_'+str(i)+'_id'] == row['Unique_Values']]
          average_value = matching_values.mean()['dire_player_'+str(i)+'_networth']
          df.loc[df['dire_player_'+str(i)+'_id'] == row['Unique_Values'], 'dire_player_'+str(i)+'_networth'] = average_value

corr_matrix = df.corr()

plt.figure(figsize=(10, 8))  # Adjust the figure size as needed
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()
for i in range(1,6):
    df = pd.get_dummies(df, columns=['radiant_player_'+str(i)+'_position'], prefix='radiant_player_'+str(i)+'position')

for i in range(1,6):
    df = pd.get_dummies(df, columns=['dire_player_'+str(i)+'_position'], prefix='diret_player_'+str(i)+'position')

for i in range(1,249):
    df[i]="0"

df =df.copy()

for i in df.iterrows():
    for j in range(1,6):
        df.at[i[0],i[1]['radiant_player_'+str(j)+'_hero']] = 1
        df.at[i[0],i[1]["dire_player_"+str(j)+'_hero']+124] = 1


for j in range(1,6):
        df.pop("radiant_player_"+str(j)+'_hero')
        df.pop("dire_player_"+str(j)+'_hero')

df.to_csv('cleaned_data_with_encoding.csv', index=False)