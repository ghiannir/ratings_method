from json import load, dump

OUTFILE = './tests/sum.json'
FILENAMES = [f'./tests/test_{i}.json' for i in range(14,23)]

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
    with open(OUTFILE, 'w') as fp:
        dump(tot, fp)