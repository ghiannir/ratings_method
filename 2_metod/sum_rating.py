from json import load, dump

OUTFILE = './results/sum.json'
FILENAMES = [f'./results/{i}.json' for i in range(14,24)]+ [f'./results/{i}b.json' for i in range(14,24)]

if __name__ == '__main__':
    tot = dict()
    for file in FILENAMES:
        with open(file, 'r') as fp:
            dic = load(fp)
        for key in dic:
            if key not in tot:
                tot[key] = list(dic[key])
            else:
                for i in range(3):
                    tot[key][i] += list(dic[key])[i]
    with open(OUTFILE, 'w') as fp:
        dump(tot, fp)
    