from json import load, dump

OUTFILE = 'sum.json'
FILENAMES = [f'./results/{i}.json' for i in range(14,24)]

if __name__ == '__main__':
    tot = dict()
    for file in FILENAMES:
        dic = load(file)
        for key in dic:
            if key not in tot:
                tot[key] = dic[key]
            else:
                tot[key] = (tot[key][i] + dic[key][i] for i in range(3))
    with open("./results/total.json", 'w') as fp:
        dump(tot, fp)
    