from numpy import poly1d
import pandas as pd
from json import load, dump
from dist_ratings import calc_rating, find_eligible
import time

COEFF_FILE = './results/coefficients.json'

def value_bet(id, df_matches, coeff, best_odd, limit=40):
    rating = calc_rating(id, df_matches)
    if rating in range(-limit, limit+1):
        h = list(coeff['HomePoly'])[0]*rating + list(coeff['HomePoly'])[1]
        #h = 0.0156*rating + 0.4647
        # a = list(coeff['AwayPoly'])[0]*rating**2 + list(coeff['AwayPoly'])[1]*rating + list(coeff['AwayPoly'])[0]
        # d = 1 - (a+h)
        h = 1/h
        # a = 1/a
        # d = 1/d

        if best_odd > h + 0.5:
            return 'H'
        # if df_matches.at[id, 'B365A'] > a:
        #      return 'A'
        # if df_matches.at[id, 'B365D'] > d:
        #     return 'D'
    return ''


if __name__ == '__main__':
    print(time.asctime())
    with open(COEFF_FILE, 'r') as fp:
        coeff = load(fp)
    year = list(i for i in range(14, 24))
    for s in '','b':
        for y in year:
            df_matches = pd.read_csv(f'./data/{y}{s}.csv')
            df_matches = df_matches[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'WHH', 'BWH', 'PSH', 'IWH', 'VCH']]
            eligible = find_eligible(df_matches)
            vbs = []
            vbs15 = []
            vbs10 = []
            vbs2 = []
            wins, wins15, wins10, wins2 = [0] * 4
            for id in eligible:
                best_odd = max(df_matches.iloc[id][['B365H', 'WHH', 'BWH', 'PSH', 'IWH', 'VCH']])
                vb = value_bet(id, df_matches, coeff, best_odd)
                vb15 = value_bet(id, df_matches, coeff, best_odd, limit=15)
                vb10 = value_bet(id, df_matches, coeff, best_odd, limit=7)
                vb2 = value_bet(id, df_matches, coeff, best_odd, limit=2)
                if vb != '':
                    if df_matches.at[id, 'FTR'] == vb:
                        wins += best_odd-1
                    else:
                        wins -= 1
                    vbs.append([id, vb, wins])
                if vb15 != '':
                    if df_matches.at[id, 'FTR'] == vb15:
                        wins15 += best_odd-1
                    else:
                        wins15 -= 1
                    vbs15.append([id, vb15, wins15])
                if vb10 != '':
                    if df_matches.at[id, 'FTR'] == vb10:
                        wins10 += best_odd-1
                    else:
                        wins10 -= 1
                    vbs10.append([id, vb10, wins10])
                if vb2 != '':
                    if df_matches.at[id, 'FTR'] == vb2:
                        wins2 += best_odd-1
                    else:
                        wins2 -= 1
                    vbs2.append([id, vb2, wins2])    
            results = {
                'season' : y,
                'all' : wins,
                'limit-15' : wins15,
                'limit-5' : wins10,
                'limit-2' : wins2,
                'bets' : len(vbs),
                'bets-15' : len(vbs15),
                'bets-5' : len(vbs10),
                'bets-2' : len(vbs2),
            }
            if s == '':
                s = 'a'
            print(f'Done: {y}{s} Time: {time.asctime()}')
            with open(f'./final_test/test_{y}{s}.json', 'w') as fp:
                dump(results, fp)
            if s == 'a':
                s = ''
    