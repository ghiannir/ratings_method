import pandas as pd
from json import dump

TOT_MATCHES = 150

def eligibility(teams):
    if len(teams) != 20:
        return False
    for key in teams:
        if teams[key] < 6:
            return False
    return True


def find_eligible(df_matches):
    teams = dict()
    eligible = list()
    id = 0
    while not eligibility(teams):
        home = df_matches.at[id, 'HomeTeam']
        away = df_matches.at[id, 'AwayTeam']
        if home not in teams:
            teams[home] = 1
        else:
            teams[home] += 1
        if away not in teams:
            teams[away] = 1
        else:
            teams[away] += 1
        if teams[home] >= 7 and teams[away] >= 7:
            eligible.append(id)
        id += 1
    eligible.extend(i for i in range(id, TOT_MATCHES))
    return eligible
        

def calc_rating(id, df_matches):
    h_name = df_matches.at[id, 'HomeTeam']
    a_name = df_matches.at[id, 'AwayTeam']
    home_rate = 0
    away_rate = 0
    h = 6
    a = 6
    
    while (h > 0 or a > 0) and id >= 0:
        id -= 1
        match  = df_matches.iloc[id]
        if h > 0 and h_name in (match['HomeTeam'], match['AwayTeam']):
            rate = match['FTHG'] - match['FTAG']
            if h_name == match['AwayTeam']:
                rate = -rate
            home_rate += rate
            h -= 1
        if a > 0 and a_name in (match['HomeTeam'] , match['AwayTeam']):
            rate = match['FTHG'] - match['FTAG']
            if a_name == match['AwayTeam']:
                rate = -rate
            away_rate += rate
            a -= 1
    return home_rate - away_rate

if __name__ == '__main__':
    year = input('Year of the end of the season: ')
    df_matches = pd.read_csv(f'./data/{year}.csv')
    df_matches = df_matches[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']]
    print(df_matches)
    #eligible = df_matches[df_matches.index >=60]
    eligible = find_eligible(df_matches)
    coll = dict()
    for id in eligible:
        rating = int(calc_rating(id, df_matches))
        res = df_matches.at[id, 'FTR']
        if rating not in coll:
            coll[rating] = [0, 0, 0]
        if res == 'H':
            coll[rating][0] += 1
        elif res == 'D':
            coll[rating][1] += 1
        else:
            coll[rating][2] += 1
    
    with open(f"./results/{year}.json", 'w') as fp:
        dump(coll, fp)
