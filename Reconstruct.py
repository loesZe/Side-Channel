# -*- coding: utf-8 -*-
#!/usr/bin/python
####################
####################
# This script is used to reconstruct the entire DES key based on the two first round-key hypothesis .
####################
# Author : LoesZe
# Date : 03/05/2018
# Last review : 05/05/2018
####################

#####
# Importing libraries
#####
# Time will help us to track how long operations take.
import time
start_time = time.time()
##
# Numpy is fundamental for scientific computing using python. It deals here with arrays a lot, opens and saves file in CSV form.
import numpy as np
from numpy import genfromtxt

#####
# Define handy functions
#####
##
# xor bit to bit
def xor(a,b,num_of_bits):
    y = bin(int(a,2) ^ int(b,2))[2:].zfill(num_of_bits)
    return y
# or bit to bit
def bor(a,b,num_of_bits):
    y = ""
    for idi in range(num_of_bits):
        y += str(int(a[idi]) or int(b[idi]))
    return y

#from KEY_SCHEDULE_REVERSE import *
#####
# Define KEY_SCHEDULE_REVERSE variable
#####
# PC1_inv reconstruct the main key[64] wiith bits from key_a[56]. Parity bits will be pad with '0'.
# in first_reroute_reverse().
PC1_inv = [8,16,24,56,52,44,36,0,7,15,23,55,51,43,35,0,6,14,22,54,50,42,34,0,5,13,21,53,49,41,33,0,4,12,20,28,48,40,32,0,3,11,19,27,47,39,31,0,2,10,18,26,46,38,30,0,1,9,17,25,45,37,29,0]
# PC2_inv define from every round key[48], which bits were used from key_b[56]. Replace these bit and pad with '0'.
# in key_schedule_reverse().
PC2_inv = [5,24,7,16,6,10,20,18,0,12,3,15,23,1,9,19,2,0,14,22,11,0,13,4,0,17,21,8,47,31,27,48,35,41,0,46,28,0,39,32,25,44,0,37,34,43,29,36,38,45,33,26,42,0,30,40]    
#####
# Define KEY_SCHEDULE_REVERSE functions
#####
##
# left shift
def shift_left(m,nb_bits):
    o = ""
    for idb in range(nb_bits):
        if (idb == 0):
            o += m[nb_bits-1]
        if (idb > 0 and idb < nb_bits):
            o += m[idb-1]
    return o
##
# The parity bit are padded to '0' and other bits of the key_a[56] are shuffled according to PC1_inv rerouter to form the main key[64].
def first_reroute_reverse(key_a):
    key = ""
    for i in range(64):
        if (i == 100):
            key += "0"
        else :
            key += key_a[PC1_inv[i]-1]
    return key
##
# Key scheduling operation. return the two partial key[64] (padded with '0') from 2 round keys[58] hypothesis.
def key_schedule_reverse(k_r):
    key_b = ["" for x in range(2)]
    for idr in range(2):
        for i in range(56):
            if (i == 8 or i == 17 or i == 21 or i == 24 or i == 34 or i == 37 or i == 42 or i == 53):
                key_b[idr] += "0"
            else :
                key_b[idr] += k_r[idr][PC2_inv[i]-1]
    key_a = ["" for x in range(2)]
    for idr in range(2):
        key_a1 = key_b[idr][0:28]
        key_a2 = key_b[idr][28:56]
        key_a[idr] = shift_left(key_a1,28) + shift_left(key_a2,28)
        if (idr == 1) :
            key_a1 = key_a[idr][0:28]
            key_a2 = key_a[idr][28:56]
            key_a[idr] = shift_left(key_a1,28) + shift_left(key_a2,28)
    key = ["" for x in range(2)]
    for idr in range(2):
        key[idr] = first_reroute_reverse(key_a[idr])  
    return key
           
##
# MAIN #
k_r = ["" for x in range(2)]
file = open("OUT/key_guess_0.dat","r+")
k0 = file.readlines()
file.close()
k_r[0] = k0[0][:-1]
file = open("OUT/key_guess_1.dat","r+")
k1 = file.readlines()
file.close()
k_r[1] = k1[0][:-1]

key = ["" for x in range(2)]
key = key_schedule_reverse(k_r)
key_guess = bor(key[0],key[1],64)
for idr in range(2):
    print ("key_%d   : %s" % (idr,key[idr]))
print ("key     : %s" % key_guess)
K = " ".join("{:02x}".format(int(key_guess[idb*8:(idb+1)*8],2)) for idb in range(8))
print ("key(hex): %s" % K)
    
file = open("OUT/key_guess.dat","w+")
file.write(key_guess+"\n")
file.write(K+"\n")
file.close()   
