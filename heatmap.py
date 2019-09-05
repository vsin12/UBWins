import os
import re
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import csv
import sys

dic = {}
dic ={'position':[],'TX':[],'RX':[],'SNR':[]}
home_path = sys.argv[1]

save_path = 'figs/' + home_path.split('/')[-2]  + '/heatmaps/'
if 'Rotation' in home_path:
    save_path = 'figs/' + home_path.split('/')[-3] + '/' + home_path.split('/')[-2]  + '/heatmaps/'
if not os.path.exists(save_path):
    os.makedirs(save_path)

directory = sorted([f for f in os.listdir(home_path) if not f.startswith('.')])

for position in directory:
    linelist = []
    print("\n\n---------",position,"started------------")
#     sns.heatmap(df, cbar=False)
    workfile = sorted([f for f in os.listdir(home_path+position) if re.search('workfile', f)])
    fileHandler = open (home_path+position+"/workfile",'r')
    for line in fileHandler:
        linelist.append(line)

    data = np.full((25,25),-9999)
    for line in linelist:
        l = line.strip()
        i = int(l.split(',')[0])
        j = int(l.split(',')[1])
        regex = r"\[(.*?)\]"
        match = re.findall(regex, l)
        list1=[]
        list1 = match[0].split(",")
        sum,avg = 0,0
        for k in range(len(list1)):
            sum += float(list1[k])
        avg = sum/len(list1)
        data[i][j] = avg
        dic['position'].append(position)
        dic['TX'].append(i)
        dic['RX'].append(j)
        dic['SNR'].append(avg)
    k = pd.DataFrame.from_dict(dic)

    df = pd.DataFrame(data, columns=[col for col in range(25)])

    sns.heatmap(df, cbar=True, annot=True, annot_kws={"size": 5}, vmin = -20, vmax = 20)
    # plt.yticks(np.arange(0,24,2))
    name = position + ".pdf"
    sns.set(rc={'figure.figsize':(16,16)})
    plt.title(position)
    plt.xlabel('RX')
    # plt.ylabel('TX')

    plt.savefig(save_path + name)
    plt.clf()
    df.iloc[0:0]

    fileHandler.close()
