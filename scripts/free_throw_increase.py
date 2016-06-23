import pandas as pd
import numpy as np



def boost_wins(df,team='ATL',free_throw=1.0):
    home = df.groupby(['Home','OneisHome','Season','Date']).sum()
    away = df.groupby(['Away','OneisHome','Season','Date']).sum()
    away['Points'] = away['FG']*2 + away['3P'] + away['FT']
    home['Points'] = home['FG']*2 + home['3P'] + home['FT']
    home.loc[(team,1),'Points'] = (home.xs(([team,1]),level=['Home','OneisHome'])['FG']*2 + home.xs(([team,1]),\
        level=['Home','OneisHome'])['3P'] + home.xs(([team,1]),level=['Home','OneisHome'])['FT']+home.xs(([team,1]),\
        level=['Home','OneisHome'])['FTA']*(free_throw-1)).values
    away.loc[(team,0),'Points'] = (away.xs(([team,0]),level=['Away','OneisHome'])['FG']*2 + away.xs(([team,0]),\
        level=['Away','OneisHome'])['3P'] + away.xs(([team,0]),level=['Away','OneisHome'])['FT']+away.xs(([team,0]),\
        level=['Away','OneisHome'])['FTA']*(free_throw-1)).values
    home['Win'] = home.query('OneisHome == 1')['Points'] > home.query('OneisHome == 0')['Points']
    away['Win'] = away.query('OneisHome == 0')['Points'] > away.query('OneisHome == 1')['Points']
    h = home.reset_index()
    a = away.reset_index()
    a = a[a['Away']==team]
    h = h[h['Home']==team]
    home_wins = h.groupby(['Home','Season','Win']).count()
    away_wins = a.groupby(['Away','Season','Win']).count()
    season_wins = home_wins['OneisHome'] + away_wins['OneisHome']
    Actual_wins = season_wins.xs((True), level='Win')
    return Actual_wins

def win_diff(df, team, free_throw=1.0):
    team_boost = boost_wins(df, team, free_throw)
    team_norm = ATLnorm = boost_wins(df, team)
    diff = np.round(np.mean(team_boost)-np.mean(team_norm),2)
    return diff
