####################
# This script performs a DES encryption.
# It is a direct translation of http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm into a python.
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

#####
# Define DES_CORE variables
#####
##
# IP define the new order of the bits from input messages in initial_permutation().
IP = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
# E1 redefine bit order of half of the shuffled message[32] into a sbox selector[48] in festel_leak().
E1 = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
# S are the S-Box of the DES. 48 bit input block define the output value set on a 32 bit output block.  8 groups of 6-bits Sixet.
# in festel().
S = np.zeros( (8,64), dtype=np.int8  )
S[0] = [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
S[1] = [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
S[2] = [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
S[3] = [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
S[4] = [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
S[5] = [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
S[6] = [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
S[7] = [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]       
# P redefine the bit order of the 32 bit output block in festel().
P = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
# IPR redefine a very last time in final_permutation().
IPR = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
#####
# Define DES_CORE functions
#####
##
# Ihe Initial permutation of the DES is performed.
def initial_permutation(message):
    m = ["" for x in range(2)]
    for idb in range(64):
        if (idb < 32):
            m[0]+= message[IP[idb]-1]
        if (idb >= 32):
            m[1] += message[IP[idb]-1]
    return m
##
# DES festel function need to be define for the DES Cipher.
def festel(m_r,k_r):
    m_e = ""
    for idb in range(48):
        m_e += m_r[E1[idb]-1]
    ##    m_e message extended
    m_x = ""    
    m_x = xor(m_e,k_r,48)
    ##    m_x xored with round key
    m_s = ""
    for idb in range(8):
        i = int(m_x[idb*6] + m_x[(idb*6)+5],2)
        j = int(m_x[(idb*6)+1] + m_x[(idb*6)+2] + m_x[(idb*6)+3] + m_x[(idb*6)+4],2)
        m_s += bin(int(S[idb][i*16+j]))[2:].zfill(4)
    ##    m_s after the s_box
    m_p = ""
    for idb in range(32):
        m_p += m_s[P[idb]-1]
    ##    m_p after permutation
    return m_p
##
# Ihe Final permutation of the DES is performed.
def final_permutation(m):
    c = ""
    for idb in range(64):
        c += m[IPR[idb]-1]
    return c
##
# DES Ciper 64-bit message and 64-bit key
def DES(message,key):
    ##
    # First all the sub key are calculated.
    k_r = ["" for x in range(16)]
    k_r = key_schedule(key)
    ##
    # Ihe Initial permutation of the DES is performed.
    m = initial_permutation(message)
    ##
    # The festel structure is built and performed.
    m_l = ["" for x in range(17)]
    m_r = ["" for x in range(17)]
    m_l[0] = m[0]
    m_r[0] = m[1]
    for idr in range(16):
        m_l[idr+1] = m_r[idr] 
        m_r[idr+1] =  xor(m_l[idr],festel(m_r[idr],k_r[idr]),32) 
    ##
    # Ihe Final permutation of the DES is performed.
    m_f = ""    
    m_f = m_r[16] + m_l[16]
    return final_permutation(m_f)
           
##
# MAIN #
scale = 16 ## equals to hexadecimal
num_of_bits = 64
              
K = "0102030405060708"
key = bin(int(K, scale))[2:].zfill(num_of_bits)

M = "a7f3cc8788ba6890"
message = bin(int(M, scale))[2:].zfill(num_of_bits)

C = "8a725fca097b46c9"
good = bin(int(C, scale))[2:].zfill(num_of_bits)

print ("key     : %s" % key)
print ("message : %s" % message)
cipher = ""
cipher = DES(message,key)
print ("--------")

toprint = cipher
print ("cipher  : %s" %toprint)
print( "xor     : %s"%(xor(toprint,good,64)))  
