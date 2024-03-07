import os
import sys
import mysql.connector
import pandas as pd
import numpy as np
import joblib
from Train_model import load_year




conn = mysql.connector.connect(
    host='dt3.ucorp.io',
    user='root',
    password='G2WN1D2',
    database='test_psia',
    port=33113
)

modele_filename = "./data/model_train.joblib"

if os.path.exists(modele_filename):
    reg = joblib.load(modele_filename)
else:
    print("Fichier model_train.joblib introuvable dans ./data/")


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
    prediction = reg.predict_log_proba(get_stats(player_1, player_2))[0]
    print(round(abs(max(prediction)),3))

#Make sure to spell the name correctly!
Player1 ="Jessica Pegula"
Player2 ="Martina Trevisan"
predict_winner(Player1, Player2)
  
  
  