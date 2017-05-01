# MPU9250-Data-Visualization
A useful tool to visualize at real time data of the MPU9250 sent through a COM port, using pyqtgraph and PyQt5

The MPU-9250 is a sensor from Invensense Inc that combine in one package both accelerometer, gyroscope and magnetometer. It embeds also a thermometer and other useful things. [The datasheet can be found here.](https://store.invensense.com/ProductDetail/MPU-9250-InvenSense-Inc/487537/pid=1135)

Repository Contents
-------------------

* **/Libraries** &mdash; An Arduino library from [sparkfun](./Libraries/Arduino/README.md)
* **/acq_mpu9250** &mdash; The Arduino code to send data to a COM port
* **mpuScrollingPlot.py** &mdash; A Python script for "scrolling plotting"
* **mpuPlotSavedData.py** &mdash; to visualize saved data

Required Python Package
-----------------------

- import serial
- import time
- import numpy as np
- from matplotlib import pyplot as plt
- import pyqtgraph as pg
- from pyqtgraph.Qt import QtCore, QtGui
- import os
- import pyqtgraph.console
- import PyQt5

Sending data to a COM port
--------------------------

I use an Arduino board. Here is how I do it

![How to connect?](https://github.com/Sanahm/MPU9250-Data-Visualization/blob/master/images/wiring.png)

Results
-------
Here is the interface. It allows you to visualize data. you can also save the data between cursors and plot them later.
![Data's visualization interface](https://github.com/Sanahm/MPU9250-Data-Visualization/blob/master/images/visu.PNG)

The script **mpuPlotSavedData.py** allows you to plot the saved data using matplotlib

![Plotting saved data](https://github.com/Sanahm/MPU9250-Data-Visualization/blob/master/images/plotSaved.png)

Resources
----------

- [Where you can get the MPU-9250 module](https://www.banggood.com/fr/GY-9250-MPU-9250-Module-9-Axis-Sensor-Module-I2C-SPI-Communication-p-1059005.html?rmmds=search)
- [Another Arduino project](https://create.arduino.cc/projecthub/mitov/arduino-accelerometer-gyroscope-compass-mpu9250-i2c-sensor-79f5bf)
