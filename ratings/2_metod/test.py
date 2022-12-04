from numpy import poly1d
import pandas as pd
from json import load, dump
from dist_ratings import calc_rating, find_eligible

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
    with open(COEFF_FILE, 'r') as fp:
        coeff = load(fp)
    year = input('Year of the end of the season: ')
    df_matches = pd.read_csv(f'./data/{year}.csv')
    df_matches = df_matches[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'BWH', 'IWH', 'PSH', 'WHH', 'VCH']]
    eligible = find_eligible(df_matches)
    vbs = []
    vbs20 = []
    vbs15 = []
    vbs10 = []
    vbs5 = []
    vbs2 = []
    wins, wins20, wins15, wins10, wins5, wins2 = [0] * 6
    for id in eligible:
        market = df_matches.iloc[id][['B365H', 'BWH', 'IWH', 'PSH', 'WHH', 'VCH']]
        best_odd = max(market)
        vb = value_bet(id, df_matches, coeff, best_odd)
        vb20 = value_bet(id, df_matches, coeff, best_odd, limit=20)
        vb15 = value_bet(id, df_matches, coeff, best_odd, limit=15)
        vb10 = value_bet(id, df_matches, coeff, best_odd, limit=10)
        vb5 = value_bet(id, df_matches, coeff, best_odd, limit=5)
        vb2 = value_bet(id, df_matches, coeff, best_odd, limit=2)
        if vb != '':
            if df_matches.at[id, 'FTR'] == vb:
                wins += best_odd-1
            else:
                wins -= 1
            vbs.append([id, vb, wins])
        if vb20 != '':
            if df_matches.at[id, 'FTR'] == vb20:
                wins20 += best_odd-1
            else:
                wins20 -= 1
            vbs20.append([id, vb20, wins20])
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
        if vb5 != '':
            if df_matches.at[id, 'FTR'] == vb5:
                wins5 += best_odd-1
            else:
                wins5 -= 1
            vbs5.append([id, vb5, wins5])
        if vb2 != '':
            if df_matches.at[id, 'FTR'] == vb2:
                wins2 += best_odd-1
            else:
                wins2 -= 1
            vbs2.append([id, vb2, wins2])
    print(f'Placed: {len(vbs)} bets')
    print(f'Your gain is: {wins:.2f}')
    print(f'Percentage of advantage: {100*wins/len(vbs):.3f}%')
    results = {
        'season' : year,
        'all' : wins,
        'limit-20' : wins20,
        'limit-15' : wins15,
        'limit-10' : wins10,
        'limit-5' : wins5,
        'limit-2' : wins2,
        'bets' : len(vbs),
        'perc-20' : wins20/len(vbs20),
        'perc-15' : wins15/len(vbs15),
        'perc-10' : wins10/len(vbs10),
        'perc-5' : wins5/len(vbs5),
        'perc-2' : wins2/len(vbs2),
        'perc-all' : wins/len(vbs),
    }
    print(results)
    with open(f'./tests/test_{year}g.json', 'w') as fp:
        dump(results, fp)