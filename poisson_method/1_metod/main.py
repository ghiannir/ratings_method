import pandas as pd
from scipy.stats import poisson
from math import sqrt

MAXGOAL = 7

def avg_calculator(collector):
    l = len(collector)
    avg_home = sum(collector[i][0] for i in range(l))/l
    avg_away = sum(collector[i][2] for i in range(l))/l
    avg_draw = sum(collector[i][1] for i in range(l))/l
    avg_over = sum(collector[i][3] for i in range(l))/l
    return avg_home, avg_draw, avg_away, avg_over

def probs(lamb):
    prob_home, prob_away, prob_draw = 0, 0, 0
    prob_over = 0
    for i in range(MAXGOAL + 1):
        for j in range(MAXGOAL + 1):
            p = poisson.pmf(i, lamb[0]) * poisson.pmf(j, lamb[1])
            if i == j:
                prob_draw += p
            elif i > j:
                prob_home += p
            else:
                prob_away += p

            if i + j >= 2.5:
                prob_over += p

    return prob_home, prob_draw, prob_away, prob_over

def calculate_lambda(df_matches, df):
    home = df['HomeTeam']
    away = df['AwayTeam']
    date = df['Date']
    df_home = df_matches[df_matches['HomeTeam']==home]
    df_home = df_home[df_home['Date'] < date]
    df_away = df_matches[df_matches['AwayTeam']==away]
    df_away = df_away[df_away['Date'] < date]
    df_home = df_home.rename(columns={'HomeTeam' : 'Team', 'FTHG' : 'GoalsScored', 'FTAG' : 'GoalsConceded'})
    df_away = df_away.rename(columns={'AwayTeam' : 'Team', 'FTAG' : 'GoalsScored', 'FTHG' : 'GoalsConceded'})
    df_home = df_home.groupby('Team').mean(numeric_only = True)
    df_away = df_away.groupby('Team').mean(numeric_only = True)
    lamb_home = df_home.at[home, 'GoalsScored']*df_away.at[away, 'GoalsConceded']
    lamb_away = df_home.at[home, 'GoalsConceded']*df_away.at[away, 'GoalsScored']
    return lamb_home, lamb_away

def bookmaker_probs(df_matches, id):
    prob_home = 1/df_matches.at[id, 'B365CH']
    prob_away = 1/df_matches.at[id, 'B365CA']
    prob_draw = 1/df_matches.at[id, 'B365CD']
    prob_over = 1/df_matches.at[id, 'B365C>2.5']
    prob_under = 1/df_matches.at[id, 'B365C<2.5']
    s_1X2 = prob_home + prob_away + prob_draw
    s_uo = prob_over + prob_under
    prob_home = prob_home/s_1X2
    prob_away = prob_away/s_1X2
    prob_draw = prob_draw/s_1X2
    prob_over = prob_over/s_uo
    return prob_home, prob_draw, prob_away, prob_over

outname = input("Where do you want to fail? ")

df_matches = pd.read_csv(input("Where is the csv? "))
df_matches['Date'] = pd.to_datetime(df_matches['Date'], dayfirst=True)

model_collector = []
result_collector = []
b365_collector = []

eligible = df_matches[df_matches.index > 30]

outfile = open(outname , 'w')
for id in eligible.index:
    lamb = calculate_lambda(
        df_matches, 
        df_matches.iloc[id]
    )
    model_collector.append(probs(lamb))

    b365_collector.append(bookmaker_probs(df_matches, id))

    h = int(df_matches.at[id, 'FTR'] == 'H')
    a = int(df_matches.at[id, 'FTR'] == 'A')
    d = int(df_matches.at[id, 'FTR'] == 'D')
    o = int(df_matches.at[id, 'FTHG']+df_matches.at[id, 'FTAG'] > 2.5)

    result_collector.append((h, d, a, o))

model_avg = avg_calculator(model_collector)
result_avg = avg_calculator(result_collector)
b365_avg = avg_calculator(b365_collector)

model_error = sqrt(sum((model_avg[i]-result_avg[i])**2 for i in range(4)))
b365_error = sqrt(sum((b365_avg[i]-result_avg[i])**2 for i in range(4)))

print(f"""
{result_avg}
{model_avg}
{b365_avg}""")

print(f"""
Model mean square error: {model_error}
B365 mean square error: {b365_error}""")

outfile.write(f"""{outname}
{result_avg}
{model_avg}
{b365_avg}
Model mean square error: {model_error}
B365 mean square error: {b365_error}""")
    
outfile.close()
