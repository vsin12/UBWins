import struct
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
from scipy import stats

##fontsize in plots for x,y - labels
fontsize = '8'
plt.figure(figsize=(10,8))
plt.grid(True)

##Handle division by zero error in matplot
np.seterr(divide='ignore', invalid='ignore')

##TOF Values - Manually taken at each point - START
lobbyDiagonal = [1880325.87,1880326.5,sys.maxint,1880328.62]
lobbyBackward = [1880325.87,1880326.75,1880327.75,1880328.75]
lobbyLateral =  [1880325.87,1880325.87,1880326.25,1880326.62,1880327.12,1880327.62]
lobbyRotation_10 = [576247.37,576247.37,576247.37,576247.5,576247.5,sys.maxint,sys.maxint,576247.37,576247.75,576247.5,576247.5,576252.5,sys.maxint]
lobbyRotation_12 = [576248.25,576248.25,576248.25,sys.maxint,576248.25,576248.25,576248.25,576248.25,576248.25,sys.maxint,576249.75,576249.75,576249.75]
conferenceRoom = [1129091.37,1129091.25,1129091.5,sys.maxint,1129091.89,1129091.76,1129091.64,1129091.64]
conferenceRoomRotation_Pos1_1_1 = [639285.75,639285.75,639285.75,639285.75,639285.75,639285.75,639285.75,639285.75,639285.75,639285.75,639285.75,639285.75,639285.75]
conferenceRoomRotation_Pos5 = [639289.37,639289.37,639289.37,639289.37,sys.maxint,sys.maxint,sys.maxint,639289.37,639289.37,639289.37,639289.25,639289.25,639289.25]
lab = [280073.12,280073.25,sys.maxint,280074.5,280075,280076,280076.62,280077.37,280078.12,280079.10]
labRotation_Pos3 =[801884.75,801884.75,801884.75,801884.75,801884.75,801884.75,801884.75,801884.62,801884.62,801884.62,801884.62,801884.62,801884.75]
labRotation_Pos6 =[801886.62,801886.62,801886.62,801886.62,801888.25,801888.25,801889.12,801886.62,801886.62,801886.62,801886.62,801886.62,801886.62]
labRotation_Pos9 =[801888.37,801888.37,sys.maxint,sys.maxint,sys.maxint,sys.maxint,sys.maxint,801888.37,sys.maxint,sys.maxint,sys.maxint,sys.maxint,sys.maxint]
corridor = [1835631.87,1835633.5,1835635,1835636.62,1835638.5]
corridorRotation_Pos5 = [1740825.87,1740825.87,1740826,1740825.87,1740825.87,sys.maxint,sys.maxint,1740825.87,1740825.87,1740825.87,1740825.87,sys.maxint,sys.maxint]
##TOF Values - Manually taken at each point -- END

##ba/ra/ba=ra lists
list_ba = []
list_ra = []
list_ba_ra = []

##Locations where pdp files are not proper
##Same are also being written to a .txt file
corrupt_pdp_locations = []

##pdp-threshold for selecting peaks
pdpthreshold = 0.001
def plotCDFUsingList():
    count = 1
    for n in [list_ba,list_ra,list_ba_ra]:
        temp  = np.sort(n)
        yvals = np.arange(len(n))/float(len(n)-1)
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

    if plotparameter == "TOF":
        plt.xlim((-20,20))
    plt.xlabel(plotparameter + " Drop", fontsize=14)
    plt.savefig("BAvs" + plot + "_" + plotparameter  + ".pdf")
    list_ba.sort()
    list_ra.sort()
    list_ba_ra.sort()

    print "\nBA List ",list_ba
    print "\nRA List ",list_ra
    print "\nBA_RA List ",list_ba_ra

    print "\n .pdf File saved successfully !!"

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

def get_pdp(pos, beam_text):
    if pos.find("Test_cdf/CoridoorRotation/pos15_0/neg45") >= 0 or pos.find("Test_cdf/ConfRotation/Pos5/90") >= 0 or pos.find("Test_cdf/ConferenceRoom/pos7") >= 0 or pos.find("Test_cdf/LabRotation/Pos6/75") >= 0 or pos.find("Test_cdf/Lobby_Rotation/Pos10/75") >= 0 or pos.find("Test_cdf/Lobby_Diagonal/Pos4") >= 0 or pos.find("Test_cdf/Lobby_Rotation/Pos12/neg45") >= 0 or pos.find("Test_cdf/Lobby_Rotation/Pos10/90") >= 0:
        return []
    try:

        listoflist = []
        finalList  = []
        f = open(pos + '/' + beam_text + '_[ ].pdp', "rb")
        num = 0
        total = 0
        while True:
    		flag = 0
    		list = []
    		total += 1
    		f.read(4)
    		for i in range(0,1024):
    			bits = f.read(8)
    			num += 1
    			if not bits:
    				flag = 1
    				break
    			x = struct.unpack_from('>d',bits)
    			if(math.isnan(x[0])):
    				list.append(0)
    			else: list.append(x[0])
    		if flag==1:
    			break
    		listoflist.append(list)

        lengthOfList = len(listoflist)

        for i in range(0,1024):
            sum = 0
            avg = 0
            for k in range(0,lengthOfList):
        	       sum = sum + listoflist[k][i]
            avg = float(sum)/lengthOfList
            finalList.append(avg)

        return finalList
    except:
        corrupt_pdp_locations.append(pos+" - "+beam_text)
        return []

def getPDPSimilarity(initialpdpvalues,currentpositionpdpvalues):
    currentmin = 0
    currentmax = 0
    temporaryList = []
    count = 0
    for n in [initialpdpvalues,currentpositionpdpvalues]:
        for i in n:
            if i > pdpthreshold:
                temporaryList.append(n.index(i))

    currentmin = min(temporaryList)
    currentmax = max(temporaryList)
    return initialpdpvalues[currentmin:currentmax+1],currentpositionpdpvalues[currentmin:currentmax+1]

def getPeaksFromPDP(pdpValueList):
    peaks = 0
    for n in pdpValueList:
        if n > pdpthreshold:
            peaks = peaks + 1
    return peaks

def get_list_for_cdf_plots(beam_tput_overall,best_beam_dict,max_tput,best_init_mcs,best_init_beam,path,test_pos):
    positions = sorted(beam_tput_overall.keys())

    if 'Rotation' in path:
        positions = ['0', '15', '30', '45', '60', '75', '90', 'neg15', 'neg30', 'neg45', 'neg60', 'neg75', 'neg90']

    # Beam adaptation
    tput_val = []
    label = []
    for pos in positions:
        tput = beam_tput_overall[pos][convert_beam_to_text(best_beam_dict[pos]) + '_[' + best_init_mcs + ']']
        tput_val.append(tput)
        label.append(convert_beam_to_text(best_beam_dict[pos]) + '_[' + best_init_mcs + ']')
    tput_val_ba = tput_val[:]
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
    snr_values = []
    locationList = []
    pdp_values = []

    for pos in positions:
        tput_val.append(beam_tput_overall[pos][best_init_beam_mcs])
        if plotparameter == "PDP" or plotparameter == "PEAK":
            pdp_values.append(get_pdp(path + pos, best_init_beam_mcs))
        snr_values.append(get_snr(path + pos, best_init_beam_mcs))

    if plotparameter == "TOF":
        if path.find("ConferenceRoom") > 0 :
            locationList = conferenceRoom
        elif path.find("ConfRotation/Pos1_1_1") > 0:
            locationList = conferenceRoomRotation_Pos1_1_1
        elif path.find("ConfRotation/Pos5") > 0:
            locationList = conferenceRoomRotation_Pos5
        elif path.find("CoridoorRotation/pos5") > 0:
            locationList = corridorRotation_Pos5
        elif path.find("CoridoorRotation/pos15_0") > 0:
            locationList = []
        elif path.find("CoridoorRotation/pos25_0") > 0:
            locationList = []
        elif path.find("Coridoor") > 0:
            locationList = corridor
        elif path.find("LabRotation/Pos3") > 0:
            locationList = labRotation_Pos3
        elif path.find("LabRotation/Pos6") > 0:
            locationList = labRotation_Pos6
        elif path.find("LabRotation/Pos9") > 0:
            locationList = labRotation_Pos9
        elif path.find("Lab") > 0:
            locationList = lab
        elif path.find("Lobby_Backward") > 0:
            locationList = lobbyBackward
        elif path.find("Lobby_Diagonal") > 0:
            locationList = lobbyDiagonal
        elif path.find("Lobby_Lateral") > 0:
            locationList = lobbyLateral
        elif path.find("Lobby_Rotation/Pos10") > 0:
            locationList = lobbyRotation_10
        elif path.find("Lobby_Rotation/Pos12") > 0:
            locationList = lobbyRotation_12
        else:
            locationList = []

    flag = 1
    list_val = tput_val_ra
    initialTOFValue = 0
    initial_snr = 0
    initial_tput = 0
    initial_pdp = 0
    tempPDPval = []

    if plot == "BA_RA":
        list_val = tput_val_ba_ra

    if plotparameter != "TOF":
        locationList = [0] * len(snr_values)

    if plotparameter != "PDP":
        if plotparameter != "PEAK":
            pdp_values = [0] * len(snr_values)

    for pdp_val,tput_ra, tput_ba,snr_val,currentPosition,TOF_val in zip(pdp_values,list_val, tput_val_ba, snr_values,positions,locationList):

        if flag == 1:
            initial_snr = snr_val
            initial_pdp = pdp_val
            initialTOFValue = TOF_val
            flag = 0
            continue
        if tput_ba < 100 and tput_ra < 100:
            continue
        if pdp_val == [] and (plotparameter == "PDP" or plotparameter == "PEAK"):
            continue
        # if snr_val < -10:
        #     continue

        #condition for low snr drops
        # if (((initial_snr - snr_val)/initial_snr) * 100 ) > 70:
        #     continue

        ##difference between ba and ra throughput
        tput = tput_ba - tput_ra

        ## similarity between two pdp vectors using pearson coeff.
        if plotparameter == "PDP":
            tempPDPval,pdp_val = getPDPSimilarity(initial_pdp,pdp_val)
            plotvalue = stats.pearsonr(tempPDPval, pdp_val)
            plotvalue = plotvalue[0]
            # if plotvalue > 0.95:
            print "\n ------Current Position or Angle ------- : ",currentPosition
            print "\nLength of list at initial position : ",len(tempPDPval)
            my_formatted_list = [ '%.6f' % elem for elem in tempPDPval ]
            print "PDP List at initial position : ",my_formatted_list
            print "Len current pos ",len(pdp_val)
            my_formatted_list = [ '%.6f' % elem for elem in pdp_val ]
            print "Current Pos : ",my_formatted_list
            print "Similarity at this position  : ",plotvalue


        ## number of peaks using pdp values
        if plotparameter == "PEAK":
            peaksininitialpos = getPeaksFromPDP(initial_pdp)
            peaksatcurrentpos = getPeaksFromPDP(pdp_val)
            plotvalue = peaksininitialpos - peaksatcurrentpos

        ## snr drop
        if plotparameter == "SNR":
            plotvalue = ((initial_snr - snr_val)/initial_snr)*100

        ##TOF Drop
        if plotparameter == "TOF":
            plotvalue = initialTOFValue - TOF_val

        if tput >= 100:
            list_ba.append(plotvalue)
        elif tput <= -100:
            list_ra.append(plotvalue)
        else:
            list_ba_ra.append(plotvalue)

    # print plotvariable
    print "\nlen(list_ba)",len(list_ba)
    print "len(list_ra)",len(list_ra)
    print "len(list_ba_ra)",len(list_ba_ra)

home_path = sys.argv[1]
plot = sys.argv[2]
plotparameter = sys.argv[3]

directory = sorted([f for f in os.listdir(home_path) if not f.startswith('.')])

for dir in directory:
    print "\n---------------------"
    print "Dir : ",dir
    print "---------------------"

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
                absolute_path = home_path + dir
                best_beam = get_best_beam(home_path + dir + "/" + subdir + "/" + position)
                best_beam_dict[position] = best_beam
                if best_init_beam == (-1,-1):
                    best_init_beam_text = convert_beam_to_text(best_beam)

                pos_throughput = sorted([f for f in os.listdir(home_path + dir + "/" + subdir + "/" + position) if re.search('.tput', f)])
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
            get_list_for_cdf_plots(beam_tput_overall,best_beam_dict,max_tput,best_init_mcs,best_init_beam,path,dir+"-"+subdir)
    else:
        beam_tput_overall = {}
        best_init_beam = (-1,-1)
        best_init_mcs = -1
        max_tput = -1
        best_beam_dict = {}
        subdirectory = sorted([f for f in os.listdir(home_path + dir) if not f.startswith('.')])
        for position in subdirectory:
            best_beam = get_best_beam(home_path + dir + "/" + position)
            best_beam_dict[position] = best_beam
            if best_init_beam == (-1,-1):
                best_init_beam_text = convert_beam_to_text(best_beam)

            pos_throughput = sorted([f for f in os.listdir(home_path + dir + "/" + position) if re.search('.tput', f)])
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
        get_list_for_cdf_plots(beam_tput_overall,best_beam_dict,max_tput,best_init_mcs,best_init_beam,path,dir)

plotCDFUsingList()

def writeCorruptPDPLocationToFile():
    fd = open("errorLocations.txt", "w")
    str1 = ''.join(corrupt_pdp_locations)
    str2 = str(len(corrupt_pdp_locations))
    fd.write(str1 + "-" + str2)
    fd.close()
