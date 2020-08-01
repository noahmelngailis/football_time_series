import pandas as pd
import numpy as np

def assessing_post_season(x):
    """assigns places for different levels of success along the epl results table"""
    
    if x <= 4:
        return 'champions_league'
    elif x <= 8:
        return 'europa_league'
    elif x <= 14:
        return 'mid_table'
    elif x <= 17:
        return'relegation_battle'
    else:
        return 'relegation'


def preprocessing_script(df):
    # assess post season
    df['finish'] = df.place.apply(assessing_post_season)
    
    # make next season points for modeling
    df["next_season_points"] = (df.groupby('team_name')['points'].shift(-1))   
    
    # goal percentage
    df['goal_percentage'] = df.goals_for / (df.goals_for+df.goals_against)

    # win rate
    df['win_rate'] = df.wins / df.losses
    
    # surpluss goals
    df['surpluss_goals'] = df.goal_differential - df.wins

    # points rate
    df['points_rate'] = (df.wins + df.draws) / df.losses
    
    # goals per loss
    df['goals_per_loss'] = df.goals_for/ (df.losses)
    return df