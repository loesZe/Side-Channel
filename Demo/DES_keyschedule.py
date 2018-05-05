####################
# This script performs a DES key schedule.
# I use it when I know the correct key and I need to generate its corresponding round keys for verification purposes.
####################
# Author : LoesZe
# Date : 28/04/2018
# Modified : 04/05/2018
####################

#####
# Importing libraries
#####
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

#####
# Define KEY_SCHEDULE variables
#####
##
# PC1 refine the bit order of the key in first_reroute().
PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
# r define for every round's left-shift the number of shift in key_schedule().
r = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
# PC2 define for every round key[48], which bits are used from key_b[56]in key_schedule().
PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
#####
# Define KEY_SCHEDULE functions
#####
##
# right shift
def shift_right(m,nb_bits):
    o = ""
    for idb in range(nb_bits):
        if (idb < nb_bits-1):
            o += m[idb+1]
        if (idb == nb_bits-1):
            o += m[0]
    return o
##
# The parity bit of the key are dropped and other bits are shuffled according to PC1 rerouter.
def first_reroute(key):
    key_a = ""
    for idb in range(56):
        key_a += key[PC1[idb]-1]
    return key_a
# Key scheduling operation. return the 16 round keys needed for DES encryption.
def key_schedule(key):
    key_a=""
    key_a = first_reroute(key)
    k_r = ["" for x in range(16)]
    for idr in range(16):
        key_b=""
        key_a1 = key_a[0:28]
        key_a2 = key_a[28:56]
        if (r[idr] == 1):
            key_b = shift_right(key_a1,28) + shift_right(key_a2,28)  
        if (r[idr] == 2):            
            key_b = shift_right(key_a1,28) + shift_right(key_a2,28)  
            key_a1 = key_b[0:28]
            key_a2 = key_b[28:56]
            key_b = shift_right(key_a1,28) + shift_right(key_a2,28)
        key_a = key_b
        for idb in range(48):
            k_r[idr] += key_b[PC2[idb]-1]
    return k_r
          
##
# MAIN DEMO FOR KEY SCHEDULE #
K = "0002020404060608"
K = "1122334455667788"
scale = 16 ## equals to hexadecimal
num_of_bits = 64
key = bin(int(K, scale))[2:].zfill(num_of_bits)
print ("key     : %s" % key)
##
# First all the sub key are calculated.
k_r = ["" for x in range(16)]
k_r = key_schedule(key)
print ("--------")
for idr in range(16):
    print ("kr_%d  : %s" % (idr,k_r[idr]))
    

