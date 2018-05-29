#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
####################
# This script 
####################
# Author : LoesZe
# Date : 06/05/2018
# Modified : 06/05/2018
####################
from __future__ import print_function
import sys
import os
import subprocess
import usbtmc
import time
import numpy
import matplotlib.pyplot as plot

# initialise device
instr =  usbtmc.Instrument(0x1ab1, 0x0588) # Rigol DS1102E

# read data
instr.write(":STOP")
instr.write(":WAV:POIN:MODE RAW")
# first ten bytes are header, so skip
rawdata = instr.ask_raw(":WAV:DATA? CHAN2")[10:]
data_size = len(rawdata)

# get metadata
sample_rate = float(instr.ask_raw(':ACQ:SAMP?'))
timescale = float(instr.ask_raw(":TIM:SCAL?"))
timeoffset = float(instr.ask_raw(":TIM:OFFS?"))
voltscale = float(instr.ask_raw(':CHAN1:SCAL?'))
voltoffset = float(instr.ask_raw(":CHAN1:OFFS?"))
 
# show metadata
print ("Data size:      ", data_size)
print ("Sample rate:    ", sample_rate)
print ("Time scale:     ", timescale)
print ("Time offset:    ", timeoffset)
print ("Voltage offset: ", voltoffset)
print ("Voltage scale:  ", voltscale)
 
# convert data from (inverted) bytes to an array of scaled floats
# this magic from Matthew Mets
data = numpy.frombuffer(rawdata, 'B')
data = data * -1 + 255
data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale
 
# creat array of matching timestamps
time = numpy.linspace(timeoffset - 6 * timescale, timeoffset + 6 * timescale,num=len(data))
 
# scale time series and label accordingly
if (time[-1] < 1e-3):
    time = time * 1e6
    tUnit = "µS"
elif (time[-1] < 1):
    time = time * 1e3
    tUnit = "mS"
else:
    tUnit = "S"
 
# Plot the data
plot.plot(time, data)
plot.title("Oscilloscope Channel 1")
plot.ylabel("Voltage (V)")
#plot.xlabel("Time (" + tUnit + ")")
plot.xlim(time[0], time[-1])
plot.show()
