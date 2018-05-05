# -*- coding: utf-8 -*-
#!/usr/bin/python
####################
####################
# This script is used in order to confront leakage guess  of different sixet with recorded traces. It returns the best candidate for every sixet of the considered round key.
#   # leak guess is 64 guess long (every 64 possibilities for the sixet round-key) for A INPUT corresponding to a TRACE
#   # "Data/leak_rr_ss.csv"
    ## k0 k1 k2 ..  k65
    #m1
    #m2
    #..
    #m.
#   # a TRACE is as long as define in previous scripts. This lenght have to be checked here.
#   # "Data/traces_smoothed_aligned.csv"
    ## s0 s1 s2 .. s.
    #m1
    #m2
    #..
    #m.
####################
# Author : LoesZe
# Date : 29/04/2018
# Last review : 05/05/2018
####################

#####
# Importing libraries
#####
# sys will be use to grab argument when using command line.
import sys
# Time will help us to track how long operations take.
import time
start_time = time.time()
##
# Numpy is fundamental for scientific computing using python. It deals here with arrays a lot, opens and saves file in CSV form.
import numpy as np
from numpy import pi
from numpy import genfromtxt
##
# SciPy is opeen source software for mathematics, science and engineering. Here it deals with signal processing (i.e. filter). And we may want to use their correlation function.
import scipy as sp
from scipy.stats.stats import pearsonr
# Matplotlib is use to generate figures :
import matplotlib.colors as colors
import matplotlib.pyplot as plt

#####
# Define useful functions
#####
##
# xor bit to bit
def xor(a,b,num_of_bits):
    y = bin(int(a,2) ^ int(b,2))[2:].zfill(num_of_bits)
    return y

##
# MAIN #
start = 0
if (len(sys.argv) > 1):
    if (int(sys.argv[1]) == 1) :   
        start = 1
stop = start+1

traces = genfromtxt("Data/traces_smoothed_aligned.csv", delimiter=',')
nb_samples = traces[0].size
nb_inputs = int(traces.size/nb_samples)
print("open traces --- %s seconds ---" % (time.time() - start_time))
step_time = time.time()

best_candidate = ""
best_candidate_diff = ""
best_candidate_cummul = ""

for ids in range(8):
    leak = genfromtxt("Data/R%d/leak_%d.csv" % (start,ids), delimiter=',', dtype=np.int8)
    nb_guess = leak[0].size
    print("open leakage --- %s seconds ---" % (time.time() - step_time))
    step_time = time.time()

    #transpose
    power_variance = np.zeros( (nb_samples,nb_inputs), dtype=np.int16  )
    power_variance = np.transpose(traces)
    print("power variance --- %s seconds ---" % (time.time() - step_time))
    step_time = time.time()

    leak_variance = np.zeros( (nb_guess,nb_inputs), dtype=np.int16  )
    leak_variance = np.transpose(leak)
    print("leak variance --- %s seconds ---" % (time.time() - step_time))
    step_time = time.time()

    # correlate
    corr = np.zeros( (nb_guess*2,nb_samples))
    for idx in range(nb_guess): # for every key candidate
        for idt in range(nb_samples): # for every moment in time
            corr[idx,idt],corr[nb_guess+(idx),idt] = pearsonr(power_variance[idt],leak_variance[idx])
    print("correlations --- %s seconds ---" % (time.time() - step_time))
    step_time = time.time()

    # best guess based on maximal correlation value
    k_max = 0
    idx_best = 0
    k_max = corr[0].max()  # the max is failing in my case, maybe get also the second best candidate ? or  use another method, like the cumulated leakage ?
    for idx in range(nb_guess): # for every key candidate
        if (corr[idx].max() > corr[idx_best].max()):
            idx_best = idx
            k_max = corr[idx].max()
    print ("Best score (max): %f" % k_max)
    print ("obtained for key_%d" % idx_best)

    num_of_bits = 6
    key = bin(int(idx_best))[2:].zfill(num_of_bits)
    best_candidate +=  key


    ####################
    # diff to mean
    diff_mean = np.zeros( (nb_guess,nb_samples))
    for idt in range(nb_samples): # for every moment in time
        corr_mean = 0
        for idx in range(nb_guess): # for every key candidate
            corr_mean = corr_mean + corr[idx,idt]
        corr_mean = corr_mean / nb_guess
        for idx in range(nb_guess):
            diff_mean[idx,idt] = abs(corr[idx,idt]-corr_mean)
    print("flattening --- %s seconds ---" % (time.time() - step_time))
    step_time = time.time()

    # best guess based on the maximal difference to the mean of correlation values
    k_diff_max = 0
    idx_diff_best = 0
    k_diff_max = diff_mean[0].max()  # the max is failing in my case, maybe get also the second best candidate ? or  use another method, like the cumulated leakage ?
    for idx in range(nb_guess): # for every key candidate
        if (diff_mean[idx].max() > diff_mean[idx_diff_best].max()):
            idx_diff_best = idx
            k_diff_max = diff_mean[idx].max()
    print ("Best score (diff to mean max): %f" % k_diff_max)
    print ("obtained for key_%d" % idx_diff_best)

    num_of_bits = 6
    key_diff = bin(int(idx_diff_best))[2:].zfill(num_of_bits)
    best_candidate_diff +=  key_diff

    ####################
    # cummulative
    k_cummulative = np.zeros((1,nb_guess))
    for idx in range(nb_guess): # for every key candidate
        for idt in range(nb_samples):
            k_cummulative[0,idx] += diff_mean[idx,idt]
    print("cummulating --- %s seconds ---" % (time.time() - step_time))
    step_time = time.time()
    
    k_cummul_max = 0
    idx_cummul_best = 0
    k_cummul_max = k_cummulative[0,0] 
    for idx in range(nb_guess): # for every key candidate
        if (k_cummulative[0,idx] > k_cummulative[0,idx_cummul_best]):
            idx_cummul_best = idx
            k_cummul_max = k_cummulative[0,idx]
    print ("Best score (cummulative  diff to mean): %f" % k_cummul_max)
    print ("obtained for key_%d" % idx_cummul_best)
    
    num_of_bits = 6
    key_cummul = bin(int(idx_cummul_best))[2:].zfill(num_of_bits)
    best_candidate_cummul +=  key_cummul      

    ################################
    #  generate slide "references" #
    ################################
    x = range(nb_samples)
    fig = plt.figure(figsize=(32,18))
    fig.clf()
    fig.suptitle("Best correlation: %d - %s" % (idx_diff_best,key_diff), fontsize=16)

    plot_C_vs_t = plt.subplot("111")
    plot_C_vs_t.set_ylabel('Input byte Correlation')
    plot_C_vs_t.set_xlabel('samples')
    #plot_C_vs_t.set_title("Correlation Inputs - Power traces", fontsize=8)

    for idx in range(nb_guess):
        labelb = "key_" + str(idx)
        plot_C_vs_t.plot(x,corr[idx], '-', linewidth=0.5, label=labelb)
    plot_C_vs_t.legend(loc="upper right")
    #plt.show()
    plt.savefig("Figures/R%d/Correlation_%d.png" % (start,ids))
    plt.close()
    ################################

print("total --- %s seconds ---" % (time.time() - start_time))
print("best candidate          : %s " % best_candidate) 
print("best candidate (max)    : %s " % best_candidate_diff)   
print("best candidate (cummul) : %s " % best_candidate_cummul)

keys = ["" for x in range(3)]
keys[0] = best_candidate
keys[1] = best_candidate_diff
keys[2] = best_candidate_cummul

file = open("OUT/key_guess_%d.dat" % start,"w+")
for i in range(3):
    file.write(keys[i]+"\n")
file.close()        
