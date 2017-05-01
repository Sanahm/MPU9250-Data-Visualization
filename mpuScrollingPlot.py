"""
This is a Python script for plotting in real time data of the MPU9250 which are collected on a com port
@author : Mohamed SANA
@contact : Follow me on github.com/Sanahm/
@licence : Under GNU licence
@date : 30/04/2017
"""


import serial
import time
import numpy as np
from matplotlib import pyplot as plt
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import os
import pyqtgraph.console
import PyQt5

pg.setConfigOption('background','w')
pg.setConfigOption('foreground', 'k')
##initialization of Qt
app = QtGui.QApplication([])
## Define a top-level widget to hold everything
w = QtGui.QWidget()
w.setWindowTitle('MPU9250 features acquisition')
#w.resize(1366,768)
wb = QtGui.QWidget(w)
win = pg.GraphicsWindow()

#win.setWindowTitle('MPU9250 features acquisition')
pause = False
def clicked():
    global pause
    pause = not(pause)
    if(pause):
        QtGui.QLineEdit.setText(text,'Pause')
    else:
        QtGui.QLineEdit.setText(text,'running...')

def Quit():
    w.close()

k = 1    
def Save():
    """
    Data between cursors can be save automatically by clicking on this button
    Here is how to save data of screen 12 by using "lr12"
    """
    global k
    QtGui.QLineEdit.setText(text,"datas have been saved!")
    edge = lr12.getRegion()
    edge = (int(edge[0]),int(edge[1]))
    data = np.zeros((10,edge[1]-edge[0]))
    data[0:3,:] = data1[:,edge[0]:edge[1]]
    data[3:6,:] = data2[:,edge[0]:edge[1]]
    data[6:9,:] = data3[:,edge[0]:edge[1]]
    data[9] = tps[edge[0]:edge[1]]-tps[0]
    np.savetxt("./SavedData/data"+str(k)+".csv",data,delimiter = ',')
    k +=1
#win.resize(1366,768)

## Create some widgets to be placed inside
btn1 = QtGui.QPushButton('Pause/Resume')
btn2 = QtGui.QPushButton('Quit')
btn3 = QtGui.QPushButton('Save')
btn1.clicked.connect(clicked)
btn2.clicked.connect(Quit)
btn3.clicked.connect(Save)
text = QtGui.QLineEdit('Enter text')

namespace = {'pg': pg, 'np': np}
texts = """
This is an interactive python console. The numpy and pyqtgraph modules have already been imported 
as 'np' and 'pg'. 

Go, play.
"""
listw = pyqtgraph.console.ConsoleWidget(namespace=namespace, text=texts)

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
wb.setLayout(layout)
wb.setFixedWidth(w.width()/3)

layout1 = QtGui.QGridLayout()
w.setLayout(layout1)
## Add widgets to the layout in their proper positions
layout.addWidget(btn1, 0, 0) # button goes in upper-left
layout.addWidget(btn2, 1, 0)
layout.addWidget(btn3, 2, 0)
layout.addWidget(text, 3, 0) # text edit goes in middle-left
layout.addWidget(listw, 4, 0) # list widget goes in bottom-left
layout1.addWidget(wb, 0,0)# plot goes on right side, spanning 3 rows
layout1.addWidget(win, 0,1)
## Display the widget as a new window
w.show()
win.setFrameStyle(2)

#screens are numeroted like this: lr11 means first ligne and first column
lr11 = pg.LinearRegionItem(values=[30, 80])
lr12 = pg.LinearRegionItem(values=[30, 80])
lr13 = pg.LinearRegionItem(values=[30, 80])
lr21 = pg.LinearRegionItem(values=[30, 80])
lr22 = pg.LinearRegionItem(values=[30, 80])
lr23 = pg.LinearRegionItem(values=[30, 80])
lr31 = pg.LinearRegionItem(values=[30, 80])
lr32 = pg.LinearRegionItem(values=[30, 80])
lr33 = pg.LinearRegionItem(values=[30, 80])

#the idea of crolling plot is to define a matrix of data with fix length and to
#update it each time you receive data

#here the length is set to 300. 3 means the 3-dimension. 
data1 = np.zeros((3,300)); #contains acc_x, acc_y and acc_z 
data2 = np.zeros((3,300)); #contains gyr_x, gyr_y and gyr_z
data3 = np.zeros((3,300)); #contains mag_x, mag_y and mag_z

p11 = win.addPlot()
p11.addLegend(offset=(10,10))
p11.addItem(lr11,name='region11')
label = pg.InfLineLabel(lr11.lines[0], "x2={value:0.2f}", position=0.9, rotateAxis=(1,0), anchor=(1, 1))
label = pg.InfLineLabel(lr11.lines[1], "x1={value:0.2f}", position=0.9, rotateAxis=(1,0), anchor=(1, 1))
p12 = win.addPlot()
p12.addLegend(offset=(10,10))
p12.addItem(lr12,name='region12')
label = pg.InfLineLabel(lr12.lines[0], "x2={value:0.2f}", position=0.9, rotateAxis=(1,0), anchor=(1, 1))
label = pg.InfLineLabel(lr12.lines[1], "x1={value:0.2f}", position=0.9, rotateAxis=(1,0), anchor=(1, 1))
p13 = win.addPlot()
p13.addLegend(offset=(10,10))
p13.addItem(lr13,name='region13')
label = pg.InfLineLabel(lr13.lines[0], "x2={value:0.2f}", position=0.9, rotateAxis=(1,0), anchor=(1, 1))
label = pg.InfLineLabel(lr13.lines[1], "x1={value:0.2f}", position=0.9, rotateAxis=(1,0), anchor=(1, 1))

win.nextRow()

p21 = win.addPlot()
p21.addLegend(offset=(10,10))
p21.addItem(lr21,name='region21')
p22 = win.addPlot()
p22.addLegend(offset=(10,10))
p22.addItem(lr22,name='region22')
p23 = win.addPlot()
p23.addLegend(offset=(10,10))
p23.addItem(lr23,name='region23')

win.nextRow()

p31 = win.addPlot()
p31.addLegend(offset=(10,10))
p31.addItem(lr31,name='region31')
p32 = win.addPlot()
p32.addLegend(offset=(10,10))
p32.addItem(lr32,name='region32')
p33 = win.addPlot()
p33.addLegend(offset=(10,10))
p33.addItem(lr33,name='region33')

curve11 = p11.plot(data1[0],pen = (0,3),name = 'acc[x]')
curve12 = p12.plot(data2[0],pen = (0,3),name = 'gyr[x]')
curve13 = p13.plot(data3[0],pen = (0,3),name = 'mag[x]')

curve21 = p21.plot(data1[1],pen = (1,3),name = 'acc[y]')
curve22 = p22.plot(data2[1],pen = (1,3),name = 'gyr[y]')
curve23 = p23.plot(data3[1],pen = (1,3),name = 'mag[y]')

curve31 = p31.plot(data1[2],pen = (2,3),name = 'acc[z]')
curve32 = p32.plot(data2[2],pen = (2,3),name = 'gyr[z]')
curve33 = p33.plot(data3[2],pen = (2,3),name = 'mag[z]')

com = 'COM3'
speed = 19200
start = time.time()
try:
    serie = serial.Serial(com,speed)
except:
    print("An error occured: unable to open the specified port " +com)
    exit(0)

tps = np.zeros(300) #you need time to, the same lenght as data
if(not(serie.readable())):
    print("unable to read available value on port\n"+com)
def update():
    global data1, curve11,curve12,curve13,data2,curve21,curve22,curve23,data3,curve31,curve32,curve33
    line = str(serie.readline(),'utf-8')
    if(not(pause)):
        acc = []
        gyr = []
        mag = []
        #print(line)
        line = line.split("\t")
        #for each line I collect data like this "acc_x acc_y acc_z gyr_x ... mag_z"
        tab = [float(i) for i in line]
        acc = tab[0:3] #read and store the 3 values of acc according to how you send your data from arduino
        gyr = tab[3:6] #read the 3 values of gyr
        mag = tab[6:9] #read the 3 values of mag
        tps[:-1] = tps[1:]
        tps[-1] = time.time()-start
        data1[:,:-1] = data1[:,1:]  # shift data in the array one sample left
                    # (see also: np.roll)
        data2[:,:-1] = data2[:,1:]
        data3[:,:-1] = data3[:,1:]
        
        data1[:,-1] = acc
        data2[:,-1] = gyr
        data3[:,-1] = mag
        curve11.setData(data1[0])
        curve12.setData(data2[0])
        curve13.setData(data3[0])
        
        curve21.setData(data1[1])
        curve22.setData(data2[1])
        curve23.setData(data3[1])
        
        curve31.setData(data1[2])
        curve32.setData(data2[2])
        curve33.setData(data3[2])


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


##    acc = np.array(acc)
##    gyr = np.array(gyr)
##    mag = np.array(mag)
##plt.plot(tps,acc[:,0])
##plt.show()
##serie.close()
    
            
