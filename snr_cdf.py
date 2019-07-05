import struct
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import sys
import math

fontsize = '8'
list_ba = []
list_ra = []
list_ba_ra = []

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

def get_list_for_cdf_plots(beam_tput_overall,best_beam_dict,max_tput,best_init_mcs,best_init_beam,path):
    positions = sorted(beam_tput_overall.keys())

    if 'Rotation' in path:
        positions = ['neg90','neg75','neg60','neg45','neg30','neg15','0','15','30','45','60','75','90']

    # Beam adaptation
    tput_val = []
    label = []
    for pos in positions:
        tput = beam_tput_overall[pos][convert_beam_to_text(best_beam_dict[pos]) + '_[' + best_init_mcs + ']']
        tput_val.append(tput)
        label.append(convert_beam_to_text(best_beam_dict[pos]) + '_[' + best_init_mcs + ']')

    tput_val_ba = tput_val[:]
    # print tput_val_ba
    label_ba = label[:]

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
    # print tput_val_ra
    label_ra = label[:]

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

    # (BA + RA) - BA
    tput_val = []
    label = []

    tput_val = [i - j for i, j in zip(tput_val_ba_ra, tput_val_ba)]
    label = [i + ' - ' + j for i, j in zip(label_ba_ra, label_ba)]

    # No adaptation
    tput_val = []
    snr_val = []
    for pos in positions:
        tput_val.append(beam_tput_overall[pos][best_init_beam_mcs])
        snr_val.append(get_snr(path + pos, best_init_beam_mcs))


    flag = 1
    list_val = tput_val_ra
    if plot == "BA_RA":
        list_val = tput_val_ba_ra
    for tput_ra, tput_ba, snr_v in zip(list_val, tput_val_ba,snr_val):
        if flag == 1:
            flag = 0
            continue
        if tput_ba < 100 and tput_ra < 100:
            continue
        tput = tput_ba - tput_ra
        print "\ntput :",tput
        if tput >= 100:
            list_ba.append(snr_v)
        elif tput <= -100:
            list_ra.append(snr_v)
        elif tput == 0:
            list_ba_ra.append(snr_v)

    print "\nlen(list_ba)",len(list_ba)
    print "len(list_ra)",len(list_ra)
    print "len(list_ba_ra)",len(list_ba_ra)

home_path = sys.argv[1]
plot = sys.argv[2]
directory = sorted([f for f in os.listdir(home_path) if not f.startswith('.')])

for dir in directory:
    print "\n---------------------"
    print "Dir : ",dir
    print "---------------------"

    # print "Homepath :",home_path
    if 'Rotation' in dir:
        subdirectory = sorted([f for f in os.listdir(home_path + dir) if not f.startswith('.')])
        for subdir in subdirectory:
            beam_tput_overall = {}
            best_init_beam = (-1,-1)
            best_init_mcs = -1
            max_tput = -1
            best_beam_dict = {}

            print "\n****************"
            print "Subdir : ",subdir
            print "****************"
            subdirect = sorted([f for f in os.listdir(home_path + dir + "/" + subdir) if not f.startswith('.')])
            for position in subdirect:
                print "\nPosition :",position
                # dir = dir + "/"
                absolute_path = home_path + dir
                # print "home_path + dir + position : ",home_path + dir + "/" + subdir + "/" + position
                best_beam = get_best_beam(home_path + dir + "/" + subdir + "/" + position)
                best_beam_dict[position] = best_beam
                if best_init_beam == (-1,-1):
                    best_init_beam_text = convert_beam_to_text(best_beam)

                # and not f.startswith('[12]_[12]_') -- for excluding [12]_* files
                pos_throughput = sorted([f for f in os.listdir(home_path + dir + "/" + subdir + "/" + position) if re.search('.tput', f)])
                print "Length of pos_throughput : ",len(pos_throughput)
                # print "pos_throughput : ",pos_throughput

                beam_tput = {}

                for tput in pos_throughput:
                    f = open(home_path + dir + "/" + subdir + "/" + position + "/" + tput, "rb")
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
                        if avg > max_tput:
                            best_init_mcs = tput[-11:-10]
                            max_tput = avg
                    beam_tput[tput[:-9]] = avg

                if best_init_beam == (-1,-1):
                    best_init_beam = best_beam
                    best_init_beam_text = '[' + str(best_init_beam[0]) + ']_[' + str(best_init_beam[1]) + ']_[0]'
                    best_init_beam_mcs = best_init_beam_text + '_[' + best_init_mcs + ']'
                beam_tput_overall[position] = beam_tput

            path = home_path + dir +"/" + subdir + "/"
            print best_init_mcs
            get_list_for_cdf_plots(beam_tput_overall,best_beam_dict,max_tput,best_init_mcs,best_init_beam,path)

    else:
        beam_tput_overall = {}
        best_init_beam = (-1,-1)
        best_init_mcs = -1
        max_tput = -1
        best_beam_dict = {}
        subdirectory = sorted([f for f in os.listdir(home_path + dir) if not f.startswith('.')])
        for position in subdirectory:
            print "\nPosition :",position
            best_beam = get_best_beam(home_path + dir + "/" + position)
            best_beam_dict[position] = best_beam
            if best_init_beam == (-1,-1):
                best_init_beam_text = convert_beam_to_text(best_beam)

            # and not f.startswith('[12]_[12]_') -- for excluding [12]_* files
            pos_throughput = sorted([f for f in os.listdir(home_path + dir + "/" + position) if re.search('.tput', f)])
            print "Length of pos_throughput : ",len(pos_throughput)
            # print "pos_throughput : ",pos_throughput

            beam_tput = {}

            for tput in pos_throughput:
                f = open(home_path + dir + "/" + position +'/'+ tput, "rb")
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
                    if avg > max_tput:
                        best_init_mcs = tput[-11:-10]
                        max_tput = avg
                beam_tput[tput[:-9]] = avg

            if best_init_beam == (-1,-1):
                best_init_beam = best_beam
                best_init_beam_text = '[' + str(best_init_beam[0]) + ']_[' + str(best_init_beam[1]) + ']_[0]'
                best_init_beam_mcs = best_init_beam_text + '_[' + best_init_mcs + ']'
            beam_tput_overall[position] = beam_tput

        path = home_path + dir + "/"
        get_list_for_cdf_plots(beam_tput_overall,best_beam_dict,max_tput,best_init_mcs,best_init_beam,path)


print "\nlist_ba ",list_ba,"\n\nlist_ra ",list_ra,"\n\nlist_ba=ra ",list_ba_ra

plt.figure(figsize=(10,8))
count = 1
for n in [list_ba,list_ra,list_ba_ra]:
    temp = np.sort(n)
    yvals=np.arange(len(n))/float(len(n)-1)
    if count == 1:
        labeltext = "BA"
        count = count + 1
    elif count == 2 and plot == "RA":
        labeltext = "RA"
        count = count + 1
    elif count == 2 and plot == "BA_RA":
        labeltext = "BA_RA"
        count = count + 1
    elif count == 3 and plot == "RA":
        labeltext = "BA = RA"
    else:
        labeltext = "BA = BA_RA"
    plt.plot(temp,yvals,label=labeltext)
    plt.legend(loc="upper left")

start,end = plt.xlim()
plt.xticks(np.arange(math.ceil(start),math.ceil(end), 2))
# plt.grid(True)
plt.xlabel('SNR Values', fontsize=14)
# plt.show()
plt.savefig("BAvs" + plot + ".pdf")
print "\n .pdf File saved successfully !!"
