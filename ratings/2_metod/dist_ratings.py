import pandas as pd
from json import dump

MAX_MATCHES = 500
MIN_TEAMS = 19

def eligibility(teams):
    if len(teams) < MIN_TEAMS:
        return False
    for key in teams:
        if teams[key][0] < 4 or teams[key][1] < 4:
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
            teams[home] = [1, 0]
        else:
            teams[home][0] += 1
        if away not in teams:
            teams[away] = [0, 1]
        else:
            teams[away][1] += 1
        if teams[home][0] > 4 and teams[home][1] > 4 and teams[away][0] > 4 and teams[away][1] > 4:
            eligible.append(id)
        id += 1
    eligible.extend(i for i in range(id, max(df_matches.index)))
    return eligible
        

def calc_rating(id, df_matches):
    h_name = df_matches.at[id, 'HomeTeam']
    a_name = df_matches.at[id, 'AwayTeam']
    home_rate = 0
    away_rate = 0
    h_h, a_a, h_a, a_h = 4, 4, 4, 4
    while h_a + h_h + a_h + a_a > 0:
        id -= 1
        match = df_matches.iloc[id]
        if h_h > 0 and h_name == match['HomeTeam']:
            home_rate += match['FTHG'] - match['FTAG']
            h_h -= 1
        if h_a > 0 and h_name == match['AwayTeam']:
            home_rate += (match['FTAG'] - match['FTHG'])/2
            h_a -= 1
        if a_h > 0 and a_name == match['HomeTeam']:
            away_rate += (match['FTHG'] - match['FTAG'])/2
            a_h -= 1
        if a_a > 0 and a_name == match['AwayTeam']:
            away_rate += match['FTAG'] - match['FTHG']
            a_a -= 1
    return home_rate - away_rate

if __name__ == '__main__':
    year = list(i for i in range(14,24))
    for s in ('','b'):
        for y in year:
            df_matches = pd.read_csv(f'./data/{y}{s}.csv')
            df_matches = df_matches[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']]
            eligible = find_eligible(df_matches)
            coll = dict()
            print(y, eligible)
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
                    
            with open(f"./results/{y}{s}.json", 'w') as fp:
                dump(coll, fp)
