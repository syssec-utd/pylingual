from pandas import DataFrame
import pandas as pd
fread = open('./data/final_report_UW1', 'r')
fread2 = open('./data/map_standard', 'r')
d = {}
for line in fread2.readlines():
    line = line.strip().split('\t')
    d[str(line[1])] = str(line[0])
d_df = {'species': [], 'hits': [], '0': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': []}
for line in fread.readlines():
    line = line.strip().split('\t')
    d_df['species'].append(d[str(line[0])])
    d_df['hits'].append(int(line[1]))
    id_list = [str(k) for k in range(10)]
    flag = 0
    for i in range(2, len(line), 2):
        id = str(line[i])
        num = int(line[i + 1])
        id_list.remove(id)
        d_df[str(id)].append(num)
        flag += 1
    for j in id_list:
        d_df[j].append(0)
        flag += 1
df = DataFrame(d_df)
sorted = df.sort_values(by='hits', ascending=False)
print(sorted.head(20))