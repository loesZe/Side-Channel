#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
####################
# This script is use for large (10 000)data set acquisition. The communication is established with the card reader.
# Then random or pre generated input data is send to the card and the encryption performed. Afterward, the power consumption is recorded from the scope for later analysis.
####################
# Author : LoesZe
# Date : 20/04/2018
# Last review : 02/05/2018
####################
from __future__ import print_function
import sys
import os
import subprocess
import random
from smartcard.System import readers
import usbtmc
import matplotlib.pyplot as plot
from matplotlib.patches import Rectangle
# Numpy is fundamental for scientific computing using python. It deals here with arrays a lot, opens and saves file in CSV form.
import numpy as np
from numpy import genfromtxt
##
# Time will help us to track how long operations take.
import time
from time import sleep
start_time = time.time()

# Define the APDUs used in this script
LOAD_KEY = [0xA0, 0x0B, 0x00, 0x00, 0x08, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

PERFORM_CRYPTO = [0xA0, 0xAA, 0x10, 0x00, 0x08];
END = [0x08];

#######################################
### Define some usefull functions : ###
#######################################
##
##
# This function read all card readers connected to the Raspberry pi and select the first one as the main card reader for the experiment.
def init_reader_card():
    # get all the available readers
    r = readers()
    print("Available readers: ", r)

    # by default we use the first reader
    i = 0
    print("Using: %s" % r[i])

    connection = r[i].createConnection()
    connection.connect()
    return connection
##
# This function arm the scope until the trigger mode is actually"single" (waiting to be triggered once).
def arm_scope():  
    instr.write(":RUN")
    sleep(0.2)
##
# This function wait for the scope to be triggered (so there is new data to be read).Then, the data is recorded into a file.
def record_trace():
    # read data
    sleep(0.5)
    instr.write(":STOP")
    instr.write(":WAV:POIN:MODE RAW")
    # first ten bytes are header, so skip
    rawdata = instr.ask_raw(":WAV:DATA? CHAN2")[10:]
    data = np.frombuffer(rawdata, 'B')
    data = data * -1 + 255
    return data

def record_trace_cut(start,stop):
    # read data
    sleep(0.5)
    instr.write(":STOP")
    instr.write(":WAV:POIN:MODE RAW")
    # first ten bytes are header, so skip
    rawdata = instr.ask_raw(":WAV:DATA? CHAN2")[10+start:10+stop]
    data = np.frombuffer(rawdata, 'B')
    data = data * -1 + 255
    return data
class Annotate(object):
    def __init__(self):
        self.ax = plot.gca()
        self.rect = Rectangle((0,0), 1, 1)
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        print ('press')
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        print ('release')
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()
          
##
# MAIN
##
nb_inputs = 10
name = "traces_nn"
start = 0
stop = 0
cut = 0
if (len(sys.argv) > 1):
    nb_inputs = int(sys.argv[1])
if (len(sys.argv) > 2):
    name = str(sys.argv[2])
if (len(sys.argv) > 3):
    start = int(sys.argv[3])
if (len(sys.argv) > 4):
    stop = int(sys.argv[4])
nb_samples = stop-start
if (nb_samples > 0):
    cut = 1
    
# Initialise card reader
connection = init_reader_card()
# Initialise scope
instr =  usbtmc.Instrument(0x1ab1, 0x0588) # Rigol
# Generate inputs
nb_bytes = 8
inputs = np.zeros((nb_inputs,nb_bytes), dtype=np.int16)
for i in range(nb_inputs):
    for idb in range(nb_bytes):
        inputs[i,idb] = random.randint(0,255)
# If there is no cut        
if (cut == 0):
    arm_scope()
    APDU =  PERFORM_CRYPTO + list(int(inputs[i,idb])for idb in range(8))+ END
    connection.transmit(APDU)
    data = record_trace()
    nb_samples = data.size

outputs = np.zeros((nb_inputs,8), dtype=np.int16)
data = np.zeros((nb_inputs,nb_samples), dtype=np.int16)
for i in range(nb_inputs):
    connection.transmit(LOAD_KEY)
    arm_scope()
    APDU =  PERFORM_CRYPTO + list(int(inputs[i,idb])for idb in range(8))+ END
    outputs[i], sw1, sw2 = connection.transmit(APDU)
    if (cut == 0):
        data[i] = record_trace()
    if (cut == 1):
        data[i] = record_trace_cut(start,stop)
np.savetxt("Data/" + name + "_out.dat", outputs, delimiter=",")
np.savetxt("Data/" + name + "_in.dat", inputs, delimiter=",")
np.savetxt("Traces/" + name + ".dat", data, delimiter=",")
print("--- %s seconds ---" % (time.time() - start_time))

# Plot the data
x = range(nb_samples)
fig, ax = plot.subplots()
for i in range(10):
    ax.plot(x, data[i])
plot.title("Power traces")
plot.ylabel("Voltage (V)")
plot.title("Demo set:")
if (cut == 0):
    plot.title("Select where stuff happen:")
    a = Annotate()
plot.savefig("Figures/Get_" + name + ".png")
plot.show()

if (cut == 0):	
    print("start: %d" % int(a.x0))
    print("stop: %d" %int(a.x1))
