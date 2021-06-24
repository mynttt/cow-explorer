import datetime
import pandas as pd
import json

csv = pd.read_csv('midlocA.csv')

s = 1816
e = 2010
d = 1816

i = 0
dict = {}

tl = 0

def process_results(csv, date_var):
    p = 0
    for i, row in enumerate(csv.itertuples(), 1):
        y = date_var
        st = getattr(row, 'styear')
        en = getattr(row, 'endyear')

        if(y == st or y == en):
            print("IN/OUT: {} | {} -> {}".format(y, st, en))
            p = p+1

        if(y > st and y < en):
            p = p+1
            print("DIFF: {} | {} -> {}".format(y, st, en))
    return p

while True:
    if(d > e):
        break

    print(d)
    dict[d] = process_results(csv, d)
    tl = tl + dict[d]

    d = d + 1
    i = i + 1

with open("hist_war.csv", "w") as f:
    f.write("date,value\n")
    for x in range(1816, 2011):
        for i in range(0, dict[x]):
            f.write("{},1\n".format(x))