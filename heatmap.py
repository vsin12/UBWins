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
print save_path
if not os.path.exists(save_path):
    os.makedirs(save_path)

directory = sorted([f for f in os.listdir(home_path) if not f.startswith('.')])
print(directory)

for position in directory:
    linelist = []
    print("\n\n---------",position,"started------------")
#     sns.heatmap(df, cbar=False)
    workfile = sorted([f for f in os.listdir(home_path+position) if re.search('workfile', f)])
    print(workfile)
    fileHandler = open (home_path+position+"/workfile",'r')
    for line in fileHandler:
        if linelist != []:
            line1 = int(line.split(',')[1])
            lastline = int(linelist[-1].split(',')[1])
            # print "lastline :",lastline
            # print "diff :",line1-lastline
            # print "line : ",line
            if line1-lastline > 1 or line1-lastline == -23:
                exp = line.split(',')[0]
                
                if line1-lastline == -23:
                    exp = int(line.split(',')[0])-1
                    # print "exp :",exp

                lastline = lastline+1    
                line2 = str(exp)+","+str(lastline)+",[-9999.0]"
                # print "inserted if:",line2
                linelist.append(line2)
                # print "inserted if:",line
                linelist.append(line)
            else:
                # print "inserted else:",line
                linelist.append(line)
        else:
            linelist.append(line)

    data = np.zeros((25,25))
    startlen = 0
    for i in range(25):
        for j in range(25):
            line = linelist[startlen]
            startlen = startlen+1
            l = line.strip()
            regex = r"\[(.*?)\]"
            match = re.findall(regex, l)
            list1=[]
            list1 = match[0].split(",")
            sum,avg = 0,0
            for k in range(len(list1)):
                sum += float(list1[k])
            avg = sum/len(list1)
#             print(list1,sum,avg)
            
            #print "avg :",avg
            data[i][j] = avg 
            dic['position'].append(position)
            dic['TX'].append(i)
            dic['RX'].append(j)
            dic['SNR'].append(avg)
    k = pd.DataFrame.from_dict(dic)
    
    df = pd.DataFrame(data, columns=[col for col in range(25)])
    sns.heatmap(df, cbar=True, annot=True, annot_kws={"size": 5}, vmin = -20, vmax = 20)
    name = position + ".pdf"
#     plt.figure(figsize=(5,5))
    sns.set(rc={'figure.figsize':(16,16)})
    plt.title(position)
    plt.xlabel('RX')
    plt.ylabel('TX')

    plt.savefig(save_path + name)
    plt.clf()
    df.iloc[0:0]

    fileHandler.close()   
    
