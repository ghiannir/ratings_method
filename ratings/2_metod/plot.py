from json import load
from matplotlib import pyplot as plt

INFILE = './results/sum.json'

if __name__ == '__main__':
    with open(INFILE, 'r') as fp:
        coll = load(fp)
    s_coll = list()
    for key in coll:
        s_coll.append(int(key))
    s_coll = sorted(s_coll)
    ds_coll = list()
    sums = list()
    h = list()
    a = list()
    d = list()
    i = 0
    for key in s_coll:
        sums.append(sum(list(coll[str(key)])))
        h.append(list(coll[str(key)])[0]/sums[-1])
        d.append(list(coll[str(key)])[1]/sums[-1])
        a.append(list(coll[str(key)])[2]/sums[-1])
        ds_coll.extend([key]*sums[-1])
        i += 1
    # num_bins = len(s_coll)
    # n, bins, patches = plt.hist(ds_coll, num_bins, color='green', alpha=0.7, density=1)
    # plt.xlabel('Ratings')
    # plt.ylabel('Overall matches')
    # plt.title('Results')
    # plt.show()
    plt.plot(s_coll, h, 'bo')
    plt.show()
    plt.plot(s_coll, d, 'go')
    plt.show()
    plt.plot(s_coll, a, 'ro')
    plt.show()