1. CDF_Plot.py - > Should be used to plot CDF Plots for various parameters : 
---------------------------------------------------------------------------
	
	a. Available Plot parameters - SNR,PDP,CIR,FFT_PDP,FFT_CIR,All,TOF
	
	CHANGE THIS PARAMETER AS PER YOUR NEED :  plotparameter = "ALL"
	
	b. ALL,Lat,Rotation,Interference,SpecificLocation
	CHANGE THIS PARAMETER TO FILTER BY LATERAL/ROTATION/INTERFERENCE/ALL MOTIONS : locationParameter = "LabLat"
	
	c. TOGGLE THIS TO FILTER OUT POINTS ON THE BASIS OF low/high snr_drops : snrCondition = False

	d. TOGGLE THIS TO FILTER OUT POINTS ON THE BASIS OF low/high TOF_drops : tofCondition = False

	e. Execution command example :
		** put the script file in the folder directory
		python2.x CDF_Plot.py Locations/ [or Name of the folder which has all the directories data]


2. tput_plot.py --> to generate NA_SNR,BA_RA,BA,RA graphs for particular location :		

	a. Execution command example :
	** put the script file in the folder directory
	python2.x tput_plot.py LocationsFolder/SpecificLocation/position 

3. tput_plot.py --> to generate SNR heatmaps for particular location :		

	a. Execution command example :
	** put the script file in the folder directory
	python2.x heatmap.py LocationsFolder/SpecificLocation/position 
