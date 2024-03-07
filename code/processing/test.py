import sys
import pandas as pd
import os 
import numpy as np
from numpy import random
# from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import plotly.express as px
from scipy.stats import boxcox
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

os.listdir("data")

import io

def load_year(loaded_year):
    '''function to load statistics from a year of choice'''

    def read_csv_with_encoding(file_path, encoding='utf-8'):
        try:
            with open(file_path, encoding=encoding) as file:
                content = file.read()
            return pd.read_csv(io.StringIO(content))
        except UnicodeDecodeError:
            print(f"Error decoding file: {file_path}")
            return None

    
    file1 = 'data/wta_matches_' + str(loaded_year) + '.csv'
    file2 = 'data/wta_matches_qual_itf_' + str(loaded_year) +'.csv'
    
    data1 = pd.read_csv(file1)
    data2 = read_csv_with_encoding(file2, encoding='latin1')
    # data2 = pd.read_csv(file2)

    # Concaténer les deux DataFrames
    data = pd.concat([data1, data2], ignore_index=True)
    
    # data.describe()

    data_columns = ['winner_id', 'winner_seed',
       'winner_name', 'winner_hand', 'winner_ht', 'winner_age', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
       'w_SvGms', 'w_bpSaved', 'w_bpFaced','winner_rank', 'winner_rank_points','loser_id', 'loser_seed', 'loser_name', 'loser_hand',
       'loser_ht', 'loser_age', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced', 'loser_rank', 'loser_rank_points']

    column_map = {x:"_".join(x.split("_")[1:]) for x in data_columns}

    # win_data = data[[ 'draw_size', 'tourney_level', 'winner_id',
    #    'winner_name', 'winner_hand', 'winner_ht', 'winner_age','score', 'best_of', 'round',
    #    'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
    #    'w_SvGms', 'w_bpSaved', 'w_bpFaced','winner_rank']].groupby(["winner_id"]).mean()


    win_data = data[[ 'draw_size', 'tourney_level', 'winner_id',
       'winner_name', 'winner_hand', 'winner_ht', 'winner_age','score', 'best_of', 'round',
       'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
       'w_SvGms', 'w_bpSaved', 'w_bpFaced','winner_rank']]
    
    win_cat_columns = ['winner_name','winner_hand','tourney_level', 'score', 'round']

    for col in win_cat_columns:
        win_data[col] = pd.to_numeric(win_data[col], errors='coerce').replace(np.NaN, 0)
    # print(win_data)
    
    win_data = win_data.groupby(["winner_id"]).mean()
    # print(win_data)

    # lose_data = data[['draw_size', 'tourney_level',
    #    'loser_id','loser_name', 'loser_hand',
    #    'loser_ht', 'loser_age', 'score', 'best_of', 'round',
    #    'minutes', 'l_ace', 'l_df', 'l_svpt',
    #    'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced', 'loser_rank']].groupby(["loser_id"]).mean()

    lose_data = data[['draw_size', 'tourney_level',
       'loser_id','loser_name', 'loser_hand',
       'loser_ht', 'loser_age', 'score', 'best_of', 'round',
       'minutes', 'l_ace', 'l_df', 'l_svpt',
       'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced', 'loser_rank']]

    lose_cat_columns=['loser_name', 'loser_hand', 'tourney_level', 'score', 'round']


     # Replace NaN values with mean in the original DataFrame
    for col in lose_cat_columns:
        lose_data[col] = pd.to_numeric(lose_data[col], errors='coerce').replace(np.NaN, 0)
    # Group by "loser_id" and apply mean to each column
    lose_data = lose_data.groupby(["loser_id"]).mean()
    
    combined_data = (win_data.rename(columns = column_map) + lose_data.rename(columns = column_map))/2
       
    
    # print(combined_data)
    # Check if combined_data is empty
    if combined_data.shape[0] == 0:
        print("DataFrame1 is empty. Cannot apply StandardScaler.")
        return None  # or handle the case appropriately

    combined_data = combined_data[combined_data.isnull().sum(axis = 1)<=0]
    
    if combined_data.shape[0] == 0:
        print("DataFrame2 is empty. Cannot apply StandardScaler.")
        return None  # or handle the case appropriately
    combined_data = combined_data[~combined_data.ht.isnull()]
    if combined_data.shape[0] == 0:
        print("DataFrame3 is empty. Cannot apply StandardScaler.")
        return None  # or handle the case appropriately
    combined_data['rank'] = boxcox(combined_data['rank'], 0)
    # print(combined_data)
    # Check if combined_data is empty after previous operations
    if combined_data.shape[0] == 0:
        print("DataFrame4 is empty. Cannot apply StandardScaler.")
        return None  # or handle the case appropriately
    try:
        scl = StandardScaler()
        names = combined_data.columns
        sys.exit(combined_data)
        combined_data[names] = scl.fit_transform(combined_data)
        combined_data['player_id'] = combined_data.index
    except Exception as e:
        print(f"Error during StandardScaler: {e}")
        return None  # or handle the case appropriately

    return combined_data

def read_year(year_predicted):
    '''splits and compares winners and losers for testing by using data until year_predicted'''
    
    combined_years = None
    for year in range(2016, year_predicted):
            year_data = load_year(year)
            if year_data is None:
                print(f"Data not loaded for year {year}")
                continue
                
            year_data["years_played"] = 1
            if combined_years is None:
                combined_years = year_data
            else: 
                combined_years = pd.concat([combined_years, year_data], ignore_index = True)   

    if combined_years is None:
        print("No data loaded for any year.")
        return None  # or handle this case accordingly
        
    combined_years = combined_years.groupby(['player_id'], as_index = 0).sum()        
    combined_years.index = combined_years.player_id
    combined_years = combined_years.div(combined_years.years_played, axis = 0).drop('years_played', axis = 1)
    # print(combined_years)
    
    
    testing_data = pd.read_csv('data/wta_matches_' + str(year_predicted) + '.csv')
    win_loss = testing_data[["winner_id", "loser_id"]].values
    x = []
    y = []
    for match in win_loss:
        player_1 = match[0]
        player_2 = match[1]
        try: 
            winner = combined_years.loc[player_1].values
            loser = combined_years.loc[player_2].values
            # try:
            #     winner = combined_years.loc[player_1].values
            # except KeyError:
            #     print(f"Player '{player_1}' not found in the DataFrame.")
            # # winner = combined_years.loc[player_1].values
            # # loser = combined_years.loc[player_2].values
            # try:
            #      loser = combined_years.loc[player_2].values
            # except KeyError:
            #     print(f"Player '{player_2}' not found in the DataFrame.")
            if np.random.random()>0.5:
                x.append(winner - loser) 
                y.append(0)
            else:
                x.append(loser - winner)
                y.append(1)
            

        except:
            continue
   
    x = np.stack(x)   
    return x, y

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dropout, Dense
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


# Load and preprocess data for training
X_train_combined = None
y_train_combined = []

for year in range(2017, 2023):
    x, y = read_year(year)

    if X_train_combined is None:
        X_train_combined = x
    else:
        X_train_combined = np.concatenate((X_train_combined, x), axis=0)

    y_train_combined.extend(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train_combined, y_train_combined, test_size=0.33, random_state=42)

# Convert the data to TensorFlow tensors
X_train_tensor = tf.convert_to_tensor(X_train, dtype=tf.float32)
X_test_tensor = tf.convert_to_tensor(X_test, dtype=tf.float32)
y_train_tensor = tf.convert_to_tensor(y_train, dtype=tf.float32)
y_test_tensor = tf.convert_to_tensor(y_test, dtype=tf.float32)

# Use keras API to define the model
model = Sequential()

# Determine the number of input features
n_features = X_train_tensor.shape[1]

# Define the model architecture
model.add(Dense(100, activation='relu', kernel_initializer='he_normal', input_shape=(21,)))
model.add(Dropout(0.4))
model.add(Dense(100, activation='relu', kernel_initializer='he_normal'))
model.add(Dropout(0.6))
model.add(Dense(50, activation='relu', kernel_initializer='he_normal'))
model.add(Dropout(0.6))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(X_train_tensor, y_train_tensor, epochs=500, batch_size=128)
test_loss, test_acc = model.evaluate(X_test_tensor, y_test_tensor)


#converts player name to player id for use in dataset
def name_convert(full_name):
    wta_names = pd.read_csv('data/wta_players.csv')
    wta_names['name_full'] = wta_names.name_first + ' ' + wta_names.name_last
    return wta_names[wta_names.name_full == full_name].player_id.values[0]
    
    
#iterates through and compares career match data from 2012 to 2022 for player_1 and player_2
def get_stats(player_1, player_2):
    player_1 = name_convert(player_1)
    player_2 = name_convert(player_2)
    combined_years = None
    for year in range(2017, 2023):
        year_data = load_year(year)
        year_data["years_played"] = 1
        if combined_years is None:
            combined_years = year_data
        else: 
            combined_years = pd.concat([combined_years, year_data], ignore_index = True)
    combined_years = combined_years.groupby(['player_id'], as_index = 0).sum()        
    combined_years.index = combined_years.player_id
    combined_years = combined_years.div(combined_years.years_played, axis = 0).drop('years_played', axis = 1)
    
    winner = combined_years.loc[player_1].values
    loser = combined_years.loc[player_2].values
    return (winner - loser).reshape (1,-1)



import numpy as np

def predict_winner(player_1, player_2, model):
    '''Predicts winner between player_1 and player_2 using a Keras model'''
    
    stats = get_stats(player_1, player_2)
    x = np.array(stats).reshape(1, -1)  # Reshape to match the input shape expected by the model
    prediction = model.predict(x)[0]

    if prediction > 0.5:
        print(player_1)
    else:
        print(player_2)

    probability = max(prediction)
    print(f"Probability of winning: {probability}")



Player1 ="Jessica Pegula"
Player2 ="Martina Trevisan"
predict_winner(Player1, Player2)
  