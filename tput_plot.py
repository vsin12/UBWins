import struct
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import sys
fontsize = '8'

def convert_beam_to_text(beam):
    return '[' + str(beam[0]) + ']_[' + str(beam[1]) + ']_[0]'

def get_best_beam(path):
    linelist = []	
    fileHandler = open(path+"/workfile",'r')
    for line in fileHandler:
        if linelist != []:
            line1 = int(line.split(',')[1])
            lastline = int(linelist[-1].split(',')[1])
            diff = line1-lastline
            if line1-lastline > 1 or line1-lastline == -23:
                exp = line.split(',')[0]
                
                if line1-lastline == -23:
                    exp = int(line.split(',')[0])-1
                    lastline = lastline+1    
                    line2 = str(exp)+","+str(lastline)+",[-9999.0]"
                    linelist.append(line2)
                else:
                    for f in range (0,diff-1):
                        lastline = lastline+1    
                        line2 = str(exp)+","+str(lastline)+",[-9999.0]"
                        linelist.append(line2)
                
                linelist.append(line)
            else:
                linelist.append(line)
        else:
            linelist.append(line)

    print "length : ",len(linelist)

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
            
            data[i][j] = avg 
    return np.unravel_index(np.argmax(data), np.shape(data))

def get_snr(pos, beam_text):
    f = open(pos + '/' + beam_text + '_[ ].snr', "rb")
    sum, avg = 0,0
    list = []
    while True: 
        bits = f.read(8)
        if not bits:
            break
        x = struct.unpack_from('>d',bits)
        if str(x[0]) != 'nan':
            list.append(x)
    for val in list:
        sum += val[0]
    avg = sum/len(list)
    return avg
    
home_path = sys.argv[1]
directory = sorted([f for f in os.listdir(home_path) if not f.startswith('.')])
print directory

save_path = 'figs/' + home_path.split('/')[-2]
if 'Rotation' in home_path:
    save_path = 'figs/' + home_path.split('/')[-3] + '/' + home_path.split('/')[-2]
    directory = ['0','15','30','45','60','75','90','neg15','neg30','neg45','neg60','neg75','neg90']
print save_path
if not os.path.exists(save_path):
    os.makedirs(save_path)


beam_tput_overall = {}
best_init_beam = (-1,-1)
best_init_mcs = -1
max_tput = -1
best_beam_dict = {}
for position in directory:
    print position
    best_beam = get_best_beam(home_path+position)
    best_beam_dict[position] = best_beam
    if best_init_beam == (-1,-1):
        best_init_beam_text = convert_beam_to_text(best_beam)

    print "---------",position,"started------------"
    pos_throughput = sorted([f for f in os.listdir(home_path+position) if re.search('.tput', f)])
    #print(pos_throughput)
    beam_tput = {}
    
    for tput in pos_throughput:
        print tput[:-9]
        f = open(home_path +position +'/'+ tput, "rb")
        sum, avg = 0, 0
        list = []
        while True: 
            bits = f.read(8)
            if not bits:
                break
            x = struct.unpack_from('>d',bits)
            if str(x[0]) != 'nan':
                list.append(x)
        for val in list:
            sum += val[0]
        avg = sum/len(list)
        if best_init_beam_text in tput and best_init_beam == (-1,-1):
            #print tput
            if avg > max_tput:
                best_init_mcs = tput[-11:-10]
                max_tput = avg
                # print best_init_mcs
                # print max_tput
        beam_tput[tput[:-9]] = avg
    
    if best_init_beam == (-1,-1):
        best_init_beam = best_beam
        print best_init_beam
        print best_beam
        best_init_beam_text = '[' + str(best_init_beam[0]) + ']_[' + str(best_init_beam[1]) + ']_[0]'
        best_init_beam_mcs = best_init_beam_text + '_[' + best_init_mcs + ']'
    beam_tput_overall[position] = beam_tput
    
positions = sorted(beam_tput_overall.keys())
pos_labels = positions
if 'Rotation' in home_path:
    positions = ['neg90','neg75','neg60','neg45','neg30','neg15','0','15','30','45','60','75','90']
    pos_labels = ['-90','-75','-60','-45','-30','-15','0','15','30','45','60','75','90']
    plt.rcParams["figure.figsize"] = (20,10)

print positions

# Beam adaptation
tput_val = []
label = []
for pos in positions:
    tput = beam_tput_overall[pos][convert_beam_to_text(best_beam_dict[pos]) + '_[' + best_init_mcs + ']']
    tput_val.append(tput)
    label.append(convert_beam_to_text(best_beam_dict[pos]) + '_[' + best_init_mcs + ']')

tput_val_ba = tput_val[:]
label_ba = label[:]

fig, ax = plt.subplots()
ax.bar(positions,tput_val_ba)
ax.set_xticklabels(pos_labels)
rects = ax.patches
for rect, label in zip(rects, label):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
            ha='center', va='bottom', fontsize=fontsize , color = 'red')

plt.savefig(save_path + '/BA.pdf')
plt.close()

# Rate adaptation
tput_val = []
label = []
for pos in positions:
    max_tput = -1
    for beam_text, tput in beam_tput_overall[pos].items():
        if best_init_beam_text in beam_text:
            if tput > max_tput:
                max_beam_text = beam_text
                max_tput = tput
    tput_val.append(max_tput)
    label.append(max_beam_text)

tput_val_ra = tput_val[:]
label_ra = label[:]

fig, ax = plt.subplots()
ax.bar(positions,tput_val)
ax.set_xticklabels(pos_labels)
rects = ax.patches
for rect, label in zip(rects, label):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
            ha='center', va='bottom', fontsize = fontsize, color = 'red')

plt.savefig(save_path + '/RA.pdf')
plt.close()

# BA + RA
tput_val = []
label = []
for pos in positions:
    max_tput = -1
    for beam_text, tput in beam_tput_overall[pos].items():
        if convert_beam_to_text(best_beam_dict[pos]) in beam_text:
            if tput > max_tput:
                max_beam_text = beam_text
                max_tput = tput
    tput_val.append(max_tput)
    label.append(max_beam_text)

tput_val_ba_ra = tput_val[:]
label_ba_ra = label[:]

fig, ax = plt.subplots()
ax.bar(positions,tput_val)
ax.set_xticklabels(pos_labels)
rects = ax.patches
for rect, label in zip(rects, label):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
            ha='center', va='bottom', fontsize = fontsize, color = 'red')

plt.savefig(save_path + '/BA_RA.pdf')
plt.close()

# (BA + RA) - BA
tput_val = []
label = []

tput_val = [i - j for i, j in zip(tput_val_ba_ra, tput_val_ba)]
label = [i + ' - ' + j for i, j in zip(label_ba_ra, label_ba)]

winner = []
for tput_ra, tput_ba in zip(tput_val_ra, tput_val_ba):
    tput = tput_ba - tput_ra
    # print tput_ba, tput_ra
    # print tput
    if tput < -100:
        winner.append('RA')
    elif tput > 100:
        winner.append('BA')
    else:
        winner.append('BA = RA')

fig, ax = plt.subplots()
ax.bar(positions,tput_val)
ax.set_xticklabels(pos_labels)
rects = ax.patches
for rect, label in zip(rects, label):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, 0, label,
            ha='center', va='bottom', fontsize = fontsize, rotation = 'vertical',color = 'red')

plt.savefig(save_path + '/BA_RA-BA.pdf')
plt.close()

# No adaptation
tput_val = []
snr_val = []
# print best_init_beam_mcs
for pos in positions:
    #print beam_tput_overall[pos].keys()
    tput_val.append(beam_tput_overall[pos][best_init_beam_mcs])
    snr_val.append(get_snr(home_path + pos, best_init_beam_mcs))

fig, ax = plt.subplots()
ax.bar(positions,tput_val)
ax.set_xticklabels(pos_labels)
rects = ax.patches
label = [best_init_beam_mcs] * len(positions)
for rect, label in zip(rects, label):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
            ha='center', va='bottom', fontsize = fontsize, color = 'red')

plt.savefig(save_path + '/NA.pdf')
plt.close()

fig, ax = plt.subplots()
ax.bar(positions,snr_val)
ax.set_xticklabels(pos_labels)
rects = ax.patches
label = winner
for rect, label in zip(rects, label):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, label,
            ha='center', va='bottom', fontsize = fontsize, color = 'red')

plt.savefig(save_path + '/NA_SNR.pdf')
plt.close()