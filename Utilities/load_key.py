#! /usr/bin/env python
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
from smartcard.System import readers

# Numpy is fundamental for scientific computing using python. It deals here with arrays a lot, opens and saves file in CSV form.
import numpy as np
from numpy import genfromtxt
##

# Define the APDUs used in this script
LOAD_KEY = [0xA0, 0x0B, 0x00, 0x00, 0x08, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8]

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
    if len(sys.argv) > 1:
        i = int(sys.argv[1])
    print("Using: %s" % r[i])

    connection = r[i].createConnection()
    connection.connect()
    return connection


#
## MAIN
connection = init_reader_card()
data, sw1, sw2 = connection.transmit(LOAD_KEY)
print("Load Key: %02X %02X" % (sw1, sw2))
print("------- done -------")
