import sys
import pandas as pd
import os 
import numpy as np
import mysql.connector
from numpy import random
from sklearn.linear_model import LogisticRegression
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

conn = mysql.connector.connect(
    host='dt3.ucorp.io',
    user='root',
    password='G2WN1D2',
    database='test_psia',
    port=33113
)

def load_year(loaded_year, conn):
    '''function to load statistics from a year of choice'''
    
    # file = 'data/wta_matches_' + str(loaded_year) + '.csv' 
    query_select = f"SELECT * FROM tennis_data WHERE tourney_date LIKE '{str(loaded_year)}%'"
    data = pd.read_sql_query(query_select, conn)

    
    # data = pd.read_csv(file)
    # data.describe()

    data_columns = ['winner_id', 'winner_seed',
       'winner_name', 'winner_hand', 'winner_ht', 'winner_age', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
       'w_SvGms', 'w_bpSaved', 'w_bpFaced','winner_rank', 'winner_rank_points','loser_id', 'loser_seed', 'loser_name', 'loser_hand',
       'loser_ht', 'loser_age', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced', 'loser_rank', 'loser_rank_points']

    column_map = {x:"_".join(x.split("_")[1:]) for x in data_columns}


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
    combined_data['rank'] = boxcox(combined_data['rank'], 1)
    combined_data = combined_data.replace(-float('inf'), 1)
    
    # print(combined_data)
    # Check if combined_data is empty after previous operations
    if combined_data.shape[0] == 0:
        print("DataFrame4 is empty. Cannot apply StandardScaler.")
        return None  # or handle the case appropriately
    try:
        
        scl = StandardScaler()
        names = combined_data.columns
        combined_data[names] = scl.fit_transform(combined_data)
        combined_data.columns = names
        combined_data['player_id'] = combined_data.index
        
    except Exception as e:
        print(f"Error during StandardScaler: {e}")
        return None  # or handle the case appropriately

    return combined_data   

    
def read_year(year_predicted):
    '''splits and compares winners and losers for testing by using data until year_predicted'''
    
    combined_years = None
    for year in range(2016, year_predicted):
        
        
        year_data = load_year(year,conn)
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
    
    
    # testing_data = pd.read_csv('data/wta_matches_' + str(year_predicted) + '.csv')
    # win_loss = testing_data[["winner_id", "loser_id"]].values
    query = f"SELECT winner_id, loser_id FROM tennis_data WHERE tourney_date LIKE '{year_predicted}%'"
    testing_data = pd.read_sql_query(query, conn)
    win_loss = testing_data[["winner_id", "loser_id"]].values
    
    x = []
    y = []
    for match in win_loss:
        player_1 = match[0]
        player_2 = match[1]
        try: 
            winner = combined_years.loc[player_1].values
            loser = combined_years.loc[player_2].values
        
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


### fits the logistics regression model on training data from 2017 to 2022
reg = LogisticRegression()

for year in range(2017, 2023):    
    x, y = read_year(year)
    reg.fit(x, y)


#converts player name to player id for use in dataset
def name_convert(full_name):
    first_name, last_name = full_name.split(' ', 1)
    query = f"SELECT player_id FROM players WHERE name_first = '{first_name}' AND name_last = '{last_name}'"
    result = pd.read_sql_query(query, conn)
    if not result.empty:
        return result['player_id'].values[0]
    else:
        return None  # Gérer le cas où aucun joueur n'est trouvé avec le nom complet donné
    
    
#iterates through and compares career match data from 2012 to 2022 for player_1 and player_2
def get_stats(player_1, player_2):
    player_1 = name_convert(player_1)
    player_2 = name_convert(player_2)
    combined_years = None
    
    for year in range(2017, 2023):
        year_data = load_year(year,conn)
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
 
def predict_winner(player_1, player_2):
    player_1= player_1.title()
    player_2= player_2.title()
    
    prediction = reg.predict(get_stats(player_1, player_2))[0]
    if prediction == 0:
        print(player_1)
    elif prediction == 1: 
        print(player_2)
    prediction = reg.predict_proba(get_stats(player_1, player_2))[0]
    print(max(prediction))

#Make sure to spell the name correctly!
Player1 ="Jessica Pegula"
Player2 ="Martina Trevisan"
predict_winner(Player1, Player2)
  
  
  
    

