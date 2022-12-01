import pandas as pd
import matplotlib

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
    df_matches = pd.read_csv('23.csv')
    eligible = df_matches[df_matches.index >=60]
    coll = dict()
    s_coll = dict()
    for id in eligible.index:
        rating = calc_rating(id, df_matches)
        res = df_matches.at[id, 'FTR']
        if rating not in coll:
            coll[rating] = [0, 0, 0, 0]
        if res == 'H':
            coll[rating][0] += 1
        elif res == 'D':
            coll[rating][1] += 1
        else:
            coll[rating][2] += 1
        coll[rating][3] += 1
        
        for key in sorted(coll):
            s_coll[key] = coll[key]
    print(s_coll)        
