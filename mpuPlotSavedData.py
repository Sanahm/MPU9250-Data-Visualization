"""
This is a Python script for visualizing saved data 
@author : Mohamed SANA
@contact : Follow me on github.com/Sanahm/
@licence : Under GNU licence
@date : 30/04/2017
"""




import numpy as np
from matplotlib import pyplot as plt

def LoadData(file,delimiter):
    data = np.genfromtxt(file,delimiter=delimiter)
    acc = data[0:3]
    gyr = data[3:6]
    mag = data[6:9]
    tps = data[9]
    return tps,acc,gyr,mag

def PlotData(tps,acc,gyr,mag):
    # Create figure with 3x3 sub-plots.
    plt.subplot(331),plt.plot(tps,acc[0]),plt.title("acc[x]"),plt.xlabel("time[s]"),plt.ylabel("mg")
    plt.subplot(332),plt.plot(tps,gyr[0]),plt.title("gyr[x]"),plt.xlabel("time[s]"),plt.ylabel("deg/s")
    plt.subplot(333),plt.plot(tps,mag[0]),plt.title("mag[x]"),plt.xlabel("time[s]"),plt.ylabel("mG")
    plt.subplot(334),plt.plot(tps,acc[1]),plt.title("acc[y]"),plt.xlabel("time[s]"),plt.ylabel("mg")
    plt.subplot(335),plt.plot(tps,gyr[1]),plt.title("gyr[y]"),plt.xlabel("time[s]"),plt.ylabel("deg/s")
    plt.subplot(336),plt.plot(tps,mag[1]),plt.title("mag[y]"),plt.xlabel("time[s]"),plt.ylabel("mG")
    plt.subplot(337),plt.plot(tps,acc[2]),plt.title("acc[z]"),plt.xlabel("time[s]"),plt.ylabel("mg")
    plt.subplot(338),plt.plot(tps,gyr[2]),plt.title("gyr[z]"),plt.xlabel("time[s]"),plt.ylabel("deg/s")
    plt.subplot(339),plt.plot(tps,mag[2]),plt.title("mag[z]"),plt.xlabel("time[s]"),plt.ylabel("mG")
    #plt.xticks([])
    #plt.yticks([])
    plt.subplots_adjust(hspace = 0.5,wspace=0.3)
    plt.show()


#exemple of use
tps_m,acc_m,gyr_m,mag_m = LoadData("./SavedData/data1.csv",delimiter=',')
PlotData(tps_m,acc_m,gyr_m,mag_m)

