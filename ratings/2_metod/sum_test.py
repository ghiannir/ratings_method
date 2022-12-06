from json import load, dump

OUTFILE = './final_test/final1.json'
FILENAMES = [f'./final_test/test_{i}{b}.json' for i in range(14,24) for b in 'ab']

if __name__ == '__main__':
    tot = dict()
    for file in FILENAMES:
        with open(file, 'r') as fp:
            dic = load(fp)
        for key in dic:
            if key not in tot:
                tot[key] = dic[key]
            else:
                tot[key] += dic[key]
    tot['perc-tot'] = f"{100*tot['all']/tot['bets']:.3f}%"
    tot['perc-15'] = f"{100*tot['limit-15']/tot['bets-15']:.3f}%"
    tot['perc-5'] = f"{100*tot['limit-5']/tot['bets-5']:.3f}%"
    tot['perc-2'] = f"{100*tot['limit-2']/tot['bets-2']:.3f}%"

    with open(OUTFILE, 'w') as fp:
        dump(tot, fp)