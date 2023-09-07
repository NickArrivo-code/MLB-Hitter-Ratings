
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:11:59 2023

@author: nickarrivo
"""

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt

# Load the dataset (Make sure it applies for the year we are doing)
df = pd.read_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Savant Yearly Hitters.csv')
df_exit_velocity = pd.read_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Exit Velocity 2023.csv')

df = df[df['year'] == 2023]
df = pd.merge(df, df_exit_velocity, on = 'player_id', how= 'inner')
df = df.drop(columns = [col for col in df.columns if '_y' in col])
#df = df.drop(columns=['Unnamed: 67'], errors='ignore')
df_swing = pd.read_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Swing_Runs_2023.csv')
df_take = pd.read_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Take_Runs_2023.csv')
df_swing_take = pd.merge(df_swing, df_take, on = 'player_id', how = 'inner', suffixes= ('_swing', '_take'))
# Extract the features you're interested in
features = ['xwoba', 'bb_percent', 'exit_velocity_avg', 'whiff_percent', 'hard_hit_percent' , 'max_hit_speed']
data_subset = df[features]

# Handle missing values and scale the data
imputer = SimpleImputer(strategy='mean')
data_imputed = imputer.fit_transform(data_subset)
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_imputed)

# Perform K-means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(data_scaled)
df['Cluster'] = clusters



#On to the contact, discipline, and power scores:
#Read in custom leaderboard merged with exit velocity data
df_merged_improved = df

#Read in swing and take leaderboards from savant


#Merge swing and take leaderboards with the previously merged dataframe
df_merged_improved = pd.merge(df_merged_improved, df_swing_take, on='player_id', how='inner')

#remove duplicate columns
#df_merged_improved = df_merged_improved.drop(columns = ['year_y','last_name', 'first_name'], errors = 'ignore')

#Filtering out players that have less than 100 at bats
df_merged_improved = df_merged_improved[df_merged_improved['ab'] > 100]

df_merged_improved['runs_heart_swing'] = df_merged_improved['runs_heart_swing'] + abs(df_merged_improved['runs_heart_swing'].min())

#Identifying which columns I want to incorporate into the power score
power_columns_corrected = [
    'max_hit_speed', 'ev95percent', 'exit_velocity_avg','runs_heart_swing' , 
    'brl_percent', 'flyballs_percent', 
    'linedrives_percent', 'sweet_spot_percent'
]

#Normalize the data here so each variable is on a scale of 0 to 1
df_normalized = df_merged_improved[power_columns_corrected].apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)

#Assign weights to adjust the importance of each variable in the power score, sum of weights adds to 1
weights = [0.15, 0.15, 0.2, 0.2, 0.1, 0.05, 0.05, 0.1]

#Create new column and make the max score equal to 100
df_merged_improved['power_score'] = df_normalized.dot(weights) * 100  # scaling to have a max value of 60


df_merged_improved = df_merged_improved.sort_values(by = 'power_score', ascending =False)

#Contact Score


df_merged_improved['runs_shadow_swing'] = df_merged_improved['runs_shadow_swing'] + abs(df_merged_improved['runs_shadow_swing'].min())
# Columns for contact score
contact_columns = ['sweet_spot_percent', 'iz_contact_percent', 'runs_shadow_swing', 
                   'whiff_percent', 'k_percent']

# Normalization
df_contact_normalized = df_merged_improved[contact_columns].apply(
    lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)

# Assigning weights
weights_contact = [0.2, 0.2, 0.2, -0.2, -0.2]

# Calculate the weighted sum of the normalized values to get contact score
df_merged_improved['contact_score'] = df_contact_normalized.dot(weights_contact)

# Scale the contact score to range from 0 to 100
df_merged_improved['contact_score'] = ((df_merged_improved['contact_score'] - df_merged_improved['contact_score'].min()) / 
                                       (df_merged_improved['contact_score'].max() - df_merged_improved['contact_score'].min())) * 100






#Creating Discipline score now

df_merged_improved['runs_chase_take'] = df_merged_improved['runs_chase_take'] + abs(df_merged_improved['runs_chase_take'].min())
df_merged_improved['runs_chase_swing'] = df_merged_improved['runs_chase_swing'] + abs(df_merged_improved['runs_chase_swing'].min())
#df_merged_improved['iso_bb'] = df_merged_improved['on_base_percent'] - df_merged_improved['batting_avg']

discipline_columns = ['runs_chase_take', 'oz_swing_percent', 'runs_chase_swing']

df_discipline_normalized_improved = df_merged_improved[discipline_columns].apply(
    lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)


weights_discipline = [ 0.33, -0.33, -0.33]



df_merged_improved['discipline_score'] = df_discipline_normalized_improved.dot(weights_discipline)

df_merged_improved['discipline_score'] = 1 + ((df_merged_improved['discipline_score'] - df_merged_improved['discipline_score'].min()) / 
                                                    (df_merged_improved['discipline_score'].max() - df_merged_improved['discipline_score'].min())) * 99

df_merged_improved = df_merged_improved.sort_values(by = 'discipline_score', ascending= False)




#Creating the final Composite score

# Normalize the scores to a 0-1 scale
df_merged_improved['power_score_normalized'] = (df_merged_improved['power_score'] - df_merged_improved['power_score'].min()) / \
                                              (df_merged_improved['power_score'].max() - df_merged_improved['power_score'].min())

df_merged_improved['contact_score_normalized'] = (df_merged_improved['contact_score'] - df_merged_improved['contact_score'].min()) / \
                                                (df_merged_improved['contact_score'].max() - df_merged_improved['contact_score'].min())

df_merged_improved['discipline_score_normalized'] = (df_merged_improved['discipline_score'] - df_merged_improved['discipline_score'].min()) / \
                                                   (df_merged_improved['discipline_score'].max() - df_merged_improved['discipline_score'].min())

# Calculate penalties for below-average scores
contact_cutoff = .25
discipline_cutoff = .25

high_power_penalty = 0  # You can adjust this value as needed

def calculate_penalty(x):
    if x['power_score'] > 60:
        return high_power_penalty
    else:
        return 0 if x['contact_score_normalized'] >= contact_cutoff else contact_cutoff - x['contact_score_normalized']

df_merged_improved['contact_penalty'] = df_merged_improved.apply(calculate_penalty, axis=1)

df_merged_improved['discipline_penalty'] = df_merged_improved['discipline_score'].apply(lambda x: 0 if x >= discipline_cutoff else discipline_cutoff - x)

# Calculate the composite score
weights = [0.5, 0.333, 0.167]
df_merged_improved['composite_score'] = df_merged_improved['power_score_normalized'] * weights[0] + \
                                       df_merged_improved['contact_score_normalized'] * weights[1] + \
                                       df_merged_improved['discipline_score_normalized'] * weights[2] - \
                                       df_merged_improved['contact_penalty'] - \
                                       df_merged_improved['discipline_penalty']

# Scale the composite score to a range of 1-100
df_merged_improved['composite_score_scaled'] = 1 + (df_merged_improved['composite_score'] - df_merged_improved['composite_score'].min()) / \
                                              (df_merged_improved['composite_score'].max() - df_merged_improved['composite_score'].min()) * 99

#Sort the data by composite score

df_merged_improved = df_merged_improved.sort_values(by = 'composite_score_scaled', ascending= False)


df_trimmed = df_merged_improved[['last_name_x', ' first_name_x', 'player_id','power_score', 'contact_score', 'discipline_score', 'composite_score_scaled', 'batting_avg','on_base_percent', 'slg_percent', 'on_base_plus_slg' , 'woba', 'home_run', 'strikeout', 'walk', 'double','bb_percent', 'k_percent', 'hit'  ]]

df_trimmed.to_csv('/Users/nickarrivo/MLB-Hitter-Ratings/Composite Score Final 2023.csv')





