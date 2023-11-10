import pandas as pd
import math

df= pd.read_csv('dota2_matches.csv')
df_names = pd.read_csv('hero_names.csv')
hero_names = df_names['localized_name'].tolist()

def replace_win(row):
    if row['winner_id'] == row['radiant_team_id']:
        return 1
    else:
        return 0

def replace(row):
    for col in [
        'radiant_player_1_position',
        'radiant_player_2_position',
        'radiant_player_3_position',
        'radiant_player_4_position',
        'radiant_player_5_position',
        'dire_player_1_position',
        'dire_player_2_position',
        'dire_player_3_position',
        'dire_player_4_position',
        'dire_player_5_position'
    ]:
        if row[col] == 'POSITION_1':
            row[col] = 1
        elif row[col] == 'POSITION_2':
            row[col] = 2
        elif row[col] == 'POSITION_3':
            row[col] = 3
        elif row[col] == 'POSITION_4':
            row[col] = 4
        else:
            row[col] = 5
    for col in [
        'radiant_player_1_networth',
        'radiant_player_2_networth',
        'radiant_player_3_networth',
        'radiant_player_4_networth',
        'radiant_player_5_networth',
        'dire_player_1_networth',
        'dire_player_2_networth',
        'dire_player_3_networth',
        'dire_player_4_networth',
        'dire_player_5_networth'
    ]:
            row[col] = math.floor((row[col] *60) /row['match_duration_seconds'])

    for col in [
        'radiant_player_1_hero',
        'radiant_player_2_hero',
        'radiant_player_3_hero',
        'radiant_player_4_hero',
        'radiant_player_5_hero',
        'dire_player_1_hero',
        'dire_player_2_hero',
        'dire_player_3_hero',
        'dire_player_4_hero',
        'dire_player_5_hero'
    ]:
        row[col] = hero_names.index(row[col]) + 1
    
    return row


df = df[[
    'match_duration_seconds',
    'radiant_team_id',
    'dire_team_id',
    'winner_id',
    'radiant_player_1_hero',
    'radiant_player_1_position',
    'radiant_player_1_networth',
    'radiant_player_1_id',
    'radiant_player_2_hero',
    'radiant_player_2_position',
    'radiant_player_2_networth',
    'radiant_player_2_id',
    'radiant_player_3_hero',
    'radiant_player_3_position',
    'radiant_player_3_networth',
    'radiant_player_3_id',
    'radiant_player_4_hero',
    'radiant_player_4_position',
    'radiant_player_4_networth',
    'radiant_player_4_id',
    'radiant_player_5_hero',
    'radiant_player_5_position',
    'radiant_player_5_networth',
    'radiant_player_5_id',
    'dire_player_1_hero',
    'dire_player_1_position',
    'dire_player_1_networth',
    'dire_player_1_id',
    'dire_player_2_hero',
    'dire_player_2_position',
    'dire_player_2_networth',
    'dire_player_2_id',
    'dire_player_3_hero',
    'dire_player_3_position',
    'dire_player_3_networth',
    'dire_player_3_id',
    'dire_player_4_hero',
    'dire_player_4_position',
    'dire_player_4_networth',
    'dire_player_4_id',
    'dire_player_5_hero',
    'dire_player_5_position',
    'dire_player_5_networth',
    'dire_player_5_id',
]]
df_cleaned =df.dropna()

df_cleaned['winner_id'] = df_cleaned.apply(replace_win, axis=1)
df_cleaned = df_cleaned.apply(replace, axis=1)


df_cleaned.to_csv('cleaned_data.csv', index=False)