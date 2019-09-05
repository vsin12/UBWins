1. CDF_Plot.py - > Should be used to plot CDF Plots for various parameters : 
---------------------------------------------------------------------------
	
	>> Available Plot parameters - SNR,PDP,CIR,FFT_PDP,FFT_CIR,All,TOF
	
	CHANGE THIS PARAMETER AS PER YOUR NEED :  plotparameter = "ALL"
	
	>> ALL,Lat,Rotation,Interference,SpecificLocation
	CHANGE THIS PARAMETER TO FILTER BY LATERAL/ROTATION/INTERFERENCE/ALL MOTIONS : locationParameter = "LabLat"
	
	>>TO FILTER OUT POINTS ON THE BASIS OF low/high snr_drops use this : snrCondition = False [set to TRUE for enabling filtering]

	>>TO FILTER OUT POINTS ON THE BASIS OF low/high tof_drops use this : tofCondition = False

	>>Execution command example :
		** put the script file in the folder directory
		python2.x CDF_Plot.py Locations/ [or Name of the folder which has all the directories data]


2. tput_plot.py --> to generate NA_SNR,BA_RA,BA,RA graphs for particular location :		

	>>Execution command example :
	** put the script file in the folder directory
	python2.x tput_plot.py LocationsFolder/SpecificLocation/position 

3. tput_plot.py --> to generate SNR heatmaps for particular location :		

	>>Execution command example :
	** put the script file in the folder directory
	python2.x heatmap.py LocationsFolder/SpecificLocation/position 
