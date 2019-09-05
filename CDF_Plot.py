import struct
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
from scipy import stats

##TOF Values - Manually taken at each point - START
lobbyDiagonal = [1880325.87,1880326.5,sys.maxint,1880328.62]
lobbyBackward = [1880325.87,1880326.75,1880327.75,1880328.75]
lobbyBackwardExtra = [1756229.62,1756231.24,1756231.87,1756232.5,1756233.75,1756234.5,1756235.25,1756236,1756236.75]
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
corridor = [1835631.87,1835632.655,1835633.5,1835634.345,1835635.19,1835636.035,1835636.88,1835637.725,1835638.57,1835639.415,1835640.26,1835641.105,1835641.95,1835642.795,1835643.64,1835644.485,1835645.33]
corridorRotation_Pos5 = [1740825.87,1740825.87,1740826,1740825.87,1740825.87,sys.maxint,sys.maxint,1740825.87,1740825.87,1740825.87,1740825.87,sys.maxint,sys.maxint]
frontCorridor_part1 = [1368529.12,1368529.87,1368530.62,1368531.37,1368532.12,1368533.25,1368533.75,1368534.62,1368535.62,1368536.25,1368537.12]
frontCorridor_part2 = [383181.75,383182.62,383183.37,383184.25,383185,383185.75,383186.87,383187.37,383188.25,383189,383189.87]
##TOF Values - Manually taken at each point -- END

##Blockage_TOF_Values
conference_blockage_lat_1 = [329637.62,329637.75,329637.62,329637.62]
conference_blockage_lat_7 = [329641.5,329642,329641.5,329641.62]
corridor_blockage_lat_5 = [544585.12,544589.37,544585.12,544585.12]
corridor_blockage_lat_10 = [544589.25,544589.37,544589.37,544589.25]
corridor_blockage_lat_12_5 = [544592.12,544592.25,544592.25,544592.12]
front_corridor_1_lat_10 = [331383,331383.25,331383,331383.25]
front_corridor_2_lat_10 = [138589.5,138589.75,138589.62,138589.62]
lab_blockage_2 = [224003.37,224003.37]
lobby_blockage_1_1 = [289863.37,0,0,0]
lobby_blockage_1_10 = [289865.25,289865.62,0,289865.25]
lobby_blockage_2_3 = [1756229.62,0,1756229.62,1756229.87]
##

##Interference_TOF_Value
interference_front_corridor_1 = [1365626.66,1365626.66,1365626.66,1365626.66]
interference_front_corridor_2 = [777806.5,777806.5,777806.5,777806.5]
interference_back_corridor_5 = [601599,601599,601599,601599]
interference_back_corridor_10 = [226865.5,226865.5,226865.5,226865.5]
interference_back_corridor_12_5 = [1592995.37,1592995.37,1592995.37,1592995.37]
interference_lobby_1_1 = [8692995.5,8692995.5,8692995.5,8692995.5]
interference_lobby_1_10 = [1152820.87,1152820.87,1152820.87,1152820.87]
interference_lobby_2_3 = [1996526.5,1996526.5,1996526.5,1996526.5]
interference_conference_1 = [1395190.75,1395190.75,1395190.75,1395190.75]
interference_conference_7 = [274307.62,274307.62,274307.62,274307.62]
interference_lab = [343844.87,343844.87,343844.87,343844.87]


## SNR,PDP,CIR,FFT_PDP,FFT_CIR,All,TOF
plotparameter = "ALL"
## ALL,Lat,Rotation,Interference,SpecificLocation
locationParameter = "LabLat"
snrCondition = False
tofCondition = False
labelTxtForSNR = ""
labelTxtForTOF = ""

if snrCondition:
    labelTxtForSNR = "_With_SNR_Condition"
if tofCondition:
    labelTxtForTOF = "_With_TOF_Condition"

##fontsize in plots for x,y - labels
fontsize = '8'

##HANDle division by zero error in matplot
np.seterr(divide='ignore', invalid='ignore')


##ba/ra/ba=ra lists
list_ba = []
list_ra = []
list_baplusra = []
list_ba_ra = []

##ALL
pdp_list = []
cir_list = []
ftt_pdp_list = []
ftt_cir_list= []

##LocationList
locList = []

##Locations where pdp/cir files are not proper
##Same are also being written to a .txt file
corrupt_pdp_locations = []
corrupt_cir_locations = []

##pdp-threshold for selecting peaks
pdpthreshold = 0.001
cirthreshold = 0.01

def writeCorruptLocationsToFile(errorlist,corruptfilename):
    fd = open("errorLocations.txt", "w")
    str0 = plotparameter +"\n"
    str1 = ''.join(errorlist)
    str2 = str(len(errorlist))
    fd.write("Files Corrupt : " + corruptfilename + "\n\n" + str1 + "\n\n" + "Number of files : " +  str2)
    fd.close()

def plotIncludingLocations(x_list,y_list):
    labeltext = "PDP Similarity at : "+locationParameter
    plt.plot(x_list,y_list,label = labeltext)
    plt.grid(True)
    plt.legend(loc="upper left")
    plt.xticks(fontsize=3)
    plt.xlabel("Locations", fontsize=8)
    plt.savefig("PDP_Similarity"+"_"+locationParameter+".pdf")
    plt.close()


def plotCDFForAllParameters():
    parameter = 0
    for n in [pdp_list,cir_list,ftt_pdp_list,ftt_cir_list]:
        temp  = np.sort(n)
        yvals = np.arange(len(n))/float(len(n)-1)
        if parameter == 0:
            labeltext = "PDP Similarity"
            parameter = 1
        elif parameter == 1:
            labeltext = "CIR Similarity"
            parameter = 2
        elif parameter == 2:
            labeltext = "PDP Similarity - FFT"
            parameter = 3
        elif parameter == 3:
            labeltext = "CIR Similarity - FFT"
        else:
            break;
        plt.plot(temp,yvals,label=labeltext)
    
    plt.grid(True)
    plt.legend(loc="upper left")
    plt.xticks(np.arange(0,1,0.1))
    plt.xlabel(plotparameter, fontsize=14)
    plt.savefig("AllParameters_CDF"+"_"+locationParameter+".pdf")
    plt.close()
    if len(corrupt_pdp_locations) > 0:
        writeCorruptLocationsToFile(corrupt_pdp_locations,"PDP")
    if len(corrupt_cir_locations) > 0:
        writeCorruptLocationsToFile(corrupt_cir_locations,"CIR")

def plotCDFUsingList():
    count = 1
    for n in [list_ba,list_ra,list_baplusra,list_ba_ra]:
        temp  = np.sort(n)
        yvals = np.arange(len(n))/float(len(n)-1)
        if count == 1:
            labeltext = "BA"+" ("+str(len(temp)) + ")"
            plt.plot(temp,yvals,label=labeltext)
            count = 2
        else:
            if count == 2:
                labeltext = "RA"+" ("+str(len(temp)) + ")"
                plt.plot(temp,yvals,label=labeltext)
                count = 3
            elif count == 3:
                labeltext = "BA+RA"+" ("+str(len(temp)) + ")"
                plt.plot(temp,yvals,label=labeltext)
                count = 4
            else:
                labeltext = "BA = RA"+" ("+str(len(temp)) + ")"
                plt.plot(temp,yvals,label=labeltext)
    
    plt.grid(True)
    if plotparameter == "TOF":
        plt.xlim((-20,20))
    plt.legend(loc="upper left")
    plt.xlabel(plotparameter, fontsize=14)
    plt.savefig("BAvsRA_" + plotparameter +"Location_"+ locationParameter + labelTxtForSNR + labelTxtForTOF + ".pdf")
    plt.close()
    print "\n"
    if len(corrupt_pdp_locations) > 0:
        writeCorruptLocationsToFile(corrupt_pdp_locations,"PDP")
    if len(corrupt_cir_locations) > 0:
        writeCorruptLocationsToFile(corrupt_cir_locations,"CIR")

def convert_beam_to_text(beam):
    return '[' + str(beam[0]) + ']_[' + str(beam[1]) + ']_[0]'

def get_best_beam(path):
    try:
        initialflag = 1
        linelist = []
        fileHandler = open(path+"/workfile",'r')
        for line in fileHandler:
            linelist.append(line)
        
        # print len(linelist)
        data = np.full((25,25),-9999.0)
        # print data
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
        
        # print path
        # print np.unravel_index(np.argmax(data), np.shape(data))
        return np.unravel_index(np.argmax(data), np.shape(data))
    except:
        print len(linelist),path,"error reading workfile"

def get_pdp_AND_snr(pos, beam_text):
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
            bits = f.read(4)
            if not bits:
                break
            x = struct.unpack_from('>i',bits)
            if x[0] == 0:
                continue
            for i in range(0,x[0]):
                bits = f.read(8)
                num += 1
                x = struct.unpack_from('>d',bits)
                if(math.isnan(x[0])):
                    list.append(0)
                else:
                    list.append(x[0])
            listoflist.append(list)

        lengthOfList = len(listoflist)

        for i in range(0,1024):
            sum = 0
            avg = 0
            for k in range(0,lengthOfList):
        	       sum = sum + listoflist[k][i]
            avg = float(sum)/lengthOfList
            finalList.append(avg)

        ##SNR Calculation from PDP 
        first100 = 0
        for n in range (0,100):
            first100 = first100 +  finalList[n]
        last100 = 0
        for n in range (924,1024):
            last100 =  last100 + finalList[n]
        noiseEstimate  = (first100 + last100)/200.0

        signalPowerEstimate = 0
        for n in range(0,1024):
            signalPowerEstimate = signalPowerEstimate + finalList[n]

        signalPowerEstimate = signalPowerEstimate/1024.0
        signalPowerEstimate = signalPowerEstimate - noiseEstimate
        snrEstimate = signalPowerEstimate/noiseEstimate
        return finalList,np.log10(snrEstimate) * 10
    except Exception as e:
        print "PDP : Exception - ",e
        corrupt_pdp_locations.append(pos + " - " + beam_text + "\n")
        return [],-10

def get_crc(pos,beam_text):
    count_success = 0
    count_failure = 0
    f = open(pos + '/' + beam_text + '_[ ].crcpattern', "rb")
    while True:
        bits = f.read(4)
        if not bits:
            break
        a = struct.unpack_from('>i',bits)
        bits = f.read(4)
        b = struct.unpack_from('>i',bits)
        for i in range(a[0] * b[0]):
            bits = f.read(1)
            x = struct.unpack_from('>?',bits)
            if not x[0]:
                count_success = count_success + 1
            else:
                count_failure = count_failure + 1
        
    return float(count_success)/(count_success+count_failure)

def get_phase(pos,beam_text):
    listoflist = []
    finalList  = []
    f = open(pos + '/' + beam_text + '_[ ].phase', "rb")
    num = 0
    total = 0
    while True:
        flag = 0
        list = []
        total += 1
        bits = f.read(4)
        if not bits:
            break
        a = struct.unpack_from('>i',bits)
        bits = f.read(4)
        b = struct.unpack_from('>i',bits)
        for i in range(a[0] * b[0]):
            bits = f.read(8)
            num += 1
            x = struct.unpack_from('>d',bits)
            if(math.isnan(x[0])):
                list.append(0)
            else:
                list.append(x[0])
        listoflist.append(np.average(list[:22]))

    return np.average(listoflist)

def get_cir(pos,beam_text):
    try:
        listoflist = []
        finalList  = []
        f = open(pos + '/' + beam_text + '_[ ].impulseresponse', "rb")
        num = 0
        total = 0
        while True:
    		flag = 0
    		list = []
    		total += 1
    		bits = f.read(4)
    		if not bits:
    			break
    		a = struct.unpack_from('>i',bits)
    		bits = f.read(4)
    		b = struct.unpack_from('>i',bits)
    		for i in range(a[0] * b[0]):
    			bits = f.read(8)
    			num += 1
    			x = struct.unpack_from('>d',bits)
    			if(math.isnan(x[0])):
    				list.append(0)
    			else:
    				list.append(x[0])
    		listoflist.append(list[:1024])

        lengthOfList = len(listoflist)

        for i in range(0,1024):
            sum = 0
            avg = 0
            for k in range(0,lengthOfList):
        	       sum = sum + listoflist[k][i]
            avg = float(sum)/lengthOfList
            finalList.append(avg)

        return finalList
    except Exception as e:
        print "CIR : Exception - ",e
        corrupt_cir_locations.append(pos + " - " + beam_text + "\n")
        return []

def getPDPSimilarity(initialpdpvalues,currentpositionpdpvalues):
    currentmin = 0
    currentmax = 0
    temporaryList = []
    for n in [initialpdpvalues,currentpositionpdpvalues]:
        for i in n:
            if i > pdpthreshold:
                temporaryList.append(n.index(i))

    currentmin = min(temporaryList)
    currentmax = max(temporaryList)
    return initialpdpvalues[currentmin:currentmax+1],currentpositionpdpvalues[currentmin:currentmax+1]

def getCIRSimilarity(initialcirvalues,currentpositioncirvalues):
    currentmin = 0
    currentmax = 0
    temporaryList = []
    for n in [initialcirvalues,currentpositioncirvalues]:
        for i in n:
            if i > cirthreshold:
                temporaryList.append(n.index(i))

    currentmin = min(temporaryList)
    currentmax = max(temporaryList)
    return initialcirvalues[currentmin:currentmax+1],currentpositioncirvalues[currentmin:currentmax+1]

def getPeaksFromPDP(pdpValueList):
    peaks = 0
    for n in pdpValueList:
        if n > pdpthreshold:
            peaks = peaks + 1
    return peaks

def get_list_for_cdf_plots(beam_tput_overall,best_beam_dict,max_tput,best_init_mcs,best_init_beam,path,test_pos):
    # print test_pos
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
    cir_values = []
    phase_values = []
    crc_values = []

    for pos in positions:
        tput_val.append(beam_tput_overall[pos][best_init_beam_mcs])
        pdp, snr = get_pdp_AND_snr(path + pos, best_init_beam_mcs)
        pdp_values.append(pdp)
        snr_values.append(snr)
        cir_values.append(get_cir(path + pos, best_init_beam_mcs))
        phase_values.append(get_phase(path + pos, best_init_beam_mcs))
        crc_values.append(get_crc(path + pos, best_init_beam_mcs))

    if plotparameter != "ALL":

        if path.find("ConferenceRoom_Lat") > 0 :
            locationList = conferenceRoom
        elif path.find("ConferenceRotation/Pos1") > 0:
            locationList = conferenceRoomRotation_Pos1_1_1
        elif path.find("ConferenceRotation/Pos5") > 0:
            locationList = conferenceRoomRotation_Pos5
        elif path.find("CoridoorRotation/pos5") > 0:
            locationList = corridorRotation_Pos5
        elif path.find("CoridoorRotation/pos15") > 0:
            locationList = []
        elif path.find("CoridoorRotation/pos25") > 0:
            locationList = []
        elif path.find("CorridorLat") > 0:
            locationList = corridor
        elif path.find("LabRotation/Pos3") > 0:
            locationList = labRotation_Pos3
        elif path.find("LabRotation/Pos6") > 0:
            locationList = labRotation_Pos6
        elif path.find("LabRotation/Pos9") > 0:
            locationList = labRotation_Pos9
        elif path.find("LabLat") > 0:
            locationList = lab
        elif path.find("Lobby_Lat_Backward") > 0:
            locationList = lobbyBackward
        elif path.find("Lobby_Lat_Diagonal") > 0:
            locationList = lobbyDiagonal
        elif path.find("Lobby_Lateral") > 0:
            locationList = lobbyLateral
        elif path.find("Lobby_Rotation/Pos10") > 0:
            locationList = lobbyRotation_10
        elif path.find("Lobby_Rotation/Pos12") > 0:
            locationList = lobbyRotation_12
        elif path.find("Lobby_Lat_2"):
            locationList = lobbyBackwardExtra
        elif path.find("Front_Corridor_back_Lat"):
            locationList = frontCorridor_part2
        elif path.find("Front_CorridorLat"):
            locationList = frontCorridor_part1
        elif path.find("Conference_Blockage_Lat/pos1"):
            locationList = conference_blockage_lat_1
        elif path.find("Conference_Blockage_Lat/pos7"):
            locationList = conference_blockage_lat_7
        elif path.find("Corridor_Blockage_Lat/pos5"):
            locationList = corridor_blockage_lat_5
        elif path.find("Corridor_Blockage_Lat/pos10"):
            locationList = corridor_blockage_lat_10
        elif path.find("Corridor_Blockage_Lat/pos12_5"):
            locationList = corridor_blockage_lat_12_5
        elif path.find("FrontCorridor_1_Blockage_Lat"):
            locationList = front_corridor_1_lat_10
        elif path.find("FrontCorridor_2_Blockage_Lat"):
            locationList = front_corridor_2_lat_10
        elif path.find("Lab_Blockage_Lat"):
            locationList = lab_blockage_2
        elif path.find("Lobby_2_Blockage_lat"):
            locationList = lobby_blockage_2_3
        elif path.find("Lobby_Blockage_Lat/pos1"):
            locationList = lobby_blockage_1_1
        elif path.find("Lobby_Blockage_Lat/pos10"):
            locationList = lobby_blockage_1_10
        elif path.find("X60_Interference/Back_Corridor/pos5"):
            locationList = interference_back_corridor_5
        elif path.find("X60_Interference/Back_Corridor/pos10"):
            locationList = interference_back_corridor_10
        elif path.find("X60_Interference/Back_Corridor/pos12_5"):
            locationList = interference_back_corridor_12_5
        elif path.find("X60_Interference/Conference/pos1"):
            locationList = interference_conference_1
        elif path.find("X60_Interference/Conference/pos7"):
            locationList = interference_conference_7
        elif path.find("X60_Interference/Front_Corridor_1/pos10"):
            locationList = interference_front_corridor_1
        elif path.find("X60_Interference/Front_Corridor_2/pos10"):
            locationList = interference_front_corridor_2
        elif path.find("X60_Interference/Lab/pos2"):
            locationList = interference_lab
        elif path.find("X60_Interference/Lobby_1/pos1"):
            locationList = interference_lobby_1_1
        elif path.find("X60_Interference/Lobby_1/pos10"):
            locationList = interference_lobby_1_10
        elif path.find("X60_Interference/Lobby_2/pos1"):
            locationList = interference_lobby_2_3
        else:
            locationList = []

        flag = 1
        list_val = tput_val_ra
        initialTOFValue = 0
        initial_snr = 0
        initial_tput = 0
        initial_pdp = 0
        initial_cir = 0
        initial_phase = 0
        tempPDPval = []
        tempCIRval = []

        for pdp_val,tput_ra, tput_ba,tput_baplusra, snr_val,cir_val,phase_val,crc_val,tof_val,currentPosition in zip(pdp_values,list_val, tput_val_ba,tput_val_ba_ra,snr_values,cir_values,phase_values,crc_values,locationList,positions):
            # print "Inside"
            if flag == 1:
                initial_snr = snr_val
                initial_pdp = pdp_val
                initial_cir = cir_val
                initialTOFValue = tof_val
                initial_phase = phase_val
                initial_crc = crc_val
                flag = 0
                continue
            if pdp_val == [] and (plotparameter == "PDP" or plotparameter == "FFT_PDP"):
                continue

            ##TOF Condition
            if (initialTOFValue - tof_val > -0.5 or initialTOFValue - tof_val < -15) and tofCondition == True:
                continue

            ##condition for low snr drops
            if initial_snr - snr_val >= 12 and snrCondition == True:
                continue

            ##difference between ba AND ra throughput
            tput = tput_ba - tput_ra

            ##Phase similarity
            if plotparameter == "PHASE":
                plotvalue = initial_phase - phase_val

            if plotparameter == "CRC":
                plotvalue = initial_crc - crc_val

            ## similarity between two pdp vectors using pearson coeff.
            if plotparameter == "PDP":
                plotvalue = stats.pearsonr(initial_pdp, pdp_val)
                plotvalue = plotvalue[0]
                formatted_list = [ '%.6f' % elem for elem in tempPDPval ]
                formatted_list = [ '%.6f' % elem for elem in pdp_val ]

            ## similarity between two pdp vectors using pearson coeff.
            if plotparameter == "CIR":
                plotvalue = stats.pearsonr(initial_cir, cir_val)
                plotvalue = plotvalue[0]

            if plotparameter == "PEAK":
                peaksininitialpos = getPeaksFromPDP(initial_pdp)
                peaksatcurrentpos = getPeaksFromPDP(pdp_val)
                plotvalue = peaksininitialpos - peaksatcurrentpos

            ## snr drop
            if plotparameter == "SNR":
                plotvalue = initial_snr - snr_val

            #TOF Drop
            if plotparameter == "TOF":
                plotvalue = initialTOFValue - tof_val

            if plotparameter == "FFT_PDP":
                fftinitialpos = abs(np.fft.fft(initial_pdp))
                fftcurrentpos = abs(np.fft.fft(pdp_val))
                plotvalue = stats.pearsonr(fftinitialpos,fftcurrentpos)
                plotvalue = plotvalue[0]

            if plotparameter == "FFT_CIR":
                cirinitialpos = abs(np.fft.fft(initial_cir))
                circurrentpos = abs(np.fft.fft(cir_val))
                plotvalue = stats.pearsonr(cirinitialpos,circurrentpos)
                plotvalue = plotvalue[0]

            if tput >= 100:
                list_ba.append(plotvalue)
            elif tput <= -100:
                list_ra.append(plotvalue)
            elif tput_ba < 100 and tput_ra < 100 and tput_baplusra >= 100:
                list_baplusra.append(plotvalue)
            else:
                list_ba_ra.append(plotvalue)

        print "\nlen(list_ba)",len(list_ba)
        print "len(list_ra)",len(list_ra)
        print "len(list_ba+ra)",len(list_baplusra)
        print "len(list_ba_ra)",len(list_ba_ra)
    else:
        flag = 1
        initial_pdp = 0
        initial_cir = 0
        initial_snr = 0
        print test_pos
        for pdp_val,snr_val,cir_val,position in zip(pdp_values,snr_values,cir_values,positions):

            if flag == 1:
                initial_pdp = pdp_val
                initial_cir = cir_val
                initial_snr = snr_val
                flag = 0
                continue

            ##condition for low snr drops
            if initial_snr - snr_val >= 12 and snrCondition == True:
                continue
            
            if pdp_val != []:
                pdp_list.append(stats.pearsonr(initial_pdp,pdp_val)[0])
                if test_pos.find("Rotation")>0:
                    tempStr = (test_pos.split("-")[1]+"_"+position).replace("Pos","")
                    locList.append(tempStr.replace("neg","-"))
                else:
                    if position.find("9_1")>0:
                        locList.append(position.replace("9_1","10"))
                    else:
                        locList.append(position)
                fftinitialpos = abs(np.fft.fft(initial_pdp))
                fftcurrentpos = abs(np.fft.fft(pdp_val))
                plotvalue = stats.pearsonr(fftinitialpos,fftcurrentpos)
                ftt_pdp_list.append(plotvalue[0])

            cir_list.append(stats.pearsonr(initial_cir,cir_val)[0])
            cirinitialpos = abs(np.fft.fft(initial_cir))
            circurrentpos = abs(np.fft.fft(cir_val))
            plotvalue = stats.pearsonr(cirinitialpos,circurrentpos)
            ftt_cir_list.append(plotvalue[0])

        print "\nlen(pdp_list) : ",len(pdp_list)
        print "len(cir_list) : ",len(cir_list)


home_path = sys.argv[1]
if locationParameter != "ALL":
    directory = sorted([f for f in os.listdir(home_path) if locationParameter in  f])
else:
    directory = sorted([f for f in os.listdir(home_path) if "" in  f])


print "Directories considered : ",directory

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

    elif dir.find("Blockage") > 0 or dir.find('Interference') >= 0:

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
            # print best_beam
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

if plotparameter != "ALL":
    plotCDFUsingList()
elif plotparameter == "ALL":
    plotCDFForAllParameters()
else:
    ##locatinoWise pdp - similarity
    plotIncludingLocations(locList,pdp_list)
    