import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

def strip_team_name(season):
    """Cleaning up team name field"""
    """Need to insert code for programatic 4 char team init names e.g. WOLV """
    for x in season.index:
        if x >= 9:
            season['team_name'][x] = season['team_name'][x][2:]
        else:
            season['team_name'][x] = season['team_name'][x][1:]
        season['team_name'][x] = season['team_name'][x][3:]
        if season['team_name'][x] == "VWolverhampton Wanderers" or season['team_name'][x] == "TSouthampton":
            season['team_name'][x] = season['team_name'][x][1:]

def epl_year_aq(year):
    """Pulls a single year from espn table of premier league results adds necessary table and cleans data"""
    url = f'https://www.espn.com/soccer/standings/_/league/ENG.1/season/{year}'
    espn_table = pd.read_html(url)
    season = pd.DataFrame(espn_table[0].join(espn_table[1]))
    season['year'] = year
    season = season.rename(columns={f'{year}-{year+1}':'team_name'})
    season['place'] = season.index + 1
    strip_team_name(season)
    return season

def rename_columns(df):
    """ renames columns to pythonic script """
    df = df.rename(columns=({'GP': 'games_played',
                            'W': 'wins',
                            'D': 'draws',
                            'L': 'losses',
                            'F': 'goals_for',
                            'A': 'goals_against',
                            'GD': 'goal_differential',
                            'P': 'points'
    }
    ))
    return df

def make_number_seasons(df):
    """makes column for number of seasons a team is in the epl"""
    seasons_series = df.groupby('team_name').draws.count()
    df2 = pd.DataFrame(seasons_series)
    df2 = df2.rename(columns={'draws':'seasons_in_epl'})
    df = df.set_index('team_name').join(df2)
    
    return df

def epl_aq_all():
    """Acquires all years of EPL standings and returns one Data Frame Takes this year as range"""
    import datetime as d
    this_year = d.datetime.now().year
    df = epl_year_aq(2002)
    for year in range(2003,this_year):
        df = pd.concat([df, epl_year_aq(year)])
    df = rename_columns(df)
    df = make_number_seasons(df)
    df.reset_index(inplace=True)
    df.to_csv('epl_years.csv')
    return df