from json import load, dump
from matplotlib import pyplot as plt
import numpy as np

INFILE = './results/sum.json'
OUTFILE = './results/coefficients.json'

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
    for key in s_coll:
        sums.append(sum(list(coll[str(key)])))
        h.append(list(coll[str(key)])[0]/sums[-1])
        d.append(list(coll[str(key)])[1]/sums[-1])
        a.append(list(coll[str(key)])[2]/sums[-1])
        ds_coll.extend([key]*sums[-1])
    c_h, sse_h, rank, s_values, rcond = np.polyfit(s_coll, h, 1, full=True)
    c_a, sse_a, rank, s_values, rcond = np.polyfit(s_coll, a, 2, full=True)
    c_d, sse_d, rank, s_values, rcond = np.polyfit(s_coll, d, 2, full=True)
    mean_d = sum(d)/len(d)
    sst_d = sum((d[i]-mean_d)**2 for i in range(len(d)))
    r_d = 1-sse_d[0]/sst_d
    mean_h = sum(h)/len(h)
    sst_h = sum((h[i]-mean_h)**2 for i in range(len(h)))
    r_h = 1-sse_h[0]/sst_h
    mean_a = sum(a)/len(a)
    sst_a = sum((a[i]-mean_a)**2 for i in range(len(a)))
    r_a = 1-sse_a[0]/sst_a
    save = {
        'HomePoly' : list(c_h),
        'AwayPoly' : list(c_a),
        'DrawPoly' : list(c_d),
        'HomeR' : r_h,
        'AwayR' : r_a,
        'DrawR' : r_d
    }
    
    with open(OUTFILE, 'w') as fp:
        dump(save, fp)
