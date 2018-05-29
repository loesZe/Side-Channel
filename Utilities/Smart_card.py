#! /usr/bin/env python
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
import random
from smartcard.System import readers

# Numpy is fundamental for scientific computing using python. It deals here with arrays a lot, opens and saves file in CSV form.
import numpy as np
from numpy import genfromtxt
##
# Time will help us to track how long operations take.
import time
start_time = time.time()

# Define the APDUs used in this script
PERFORM_CRYPTO = [0xA0, 0xAA, 0x10, 0x00, 0x08];
END = [0x08];
# Define the APDUs used in this script
LOAD_KEY = [0xA0, 0x0B, 0x00, 0x00, 0x08, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8]
LOAD_KEY_0 = [0xA0, 0x0B, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

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

connection = init_reader_card()
        
nb_inputs = 2
nb_bytes = 8
if (len(sys.argv) > 1):
    nb_inputs = int(sys.argv[1])
inputs = np.zeros( (nb_inputs,nb_bytes), dtype=np.int16 )
for i in range(nb_inputs):
    for idb in range(nb_bytes):
        inputs[i,idb] = random.randint(0,255)

for i in range(2):
    m = list(int(inputs[i,idb])for idb in range(8))
    APDU =  PERFORM_CRYPTO + m + END
    data, sw1, sw2 = connection.transmit(APDU)
    print("encrypted    : %s" % data)
print("------------")    
for i in range(2):
    m = list(int(inputs[i,idb])for idb in range(8))
    APDU =  PERFORM_CRYPTO + m + END
    data, sw1, sw2 = connection.transmit(LOAD_KEY)
    data, sw1, sw2 = connection.transmit(APDU)
    print("encrypted    : %s" % data)
print("------------")    
for i in range(2):
    m = list(int(inputs[i,idb])for idb in range(8))
    APDU =  PERFORM_CRYPTO + m + END
    data, sw1, sw2 = connection.transmit(LOAD_KEY_0)
    data, sw1, sw2 = connection.transmit(APDU)
    print("encrypted    : %s" % data)
print("done.")
