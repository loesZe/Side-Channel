# -*- coding: utf-8 -*-
#!/usr/bin/python
####################
####################
# This script 
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
import matplotlib.pyplot as plot

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
name1 = "traces_nn"
if (len(sys.argv) > 1):
    name1 = str(sys.argv[1])

name2 = "traces_nn_in"
if (len(sys.argv) > 2):
    name2 = str(sys.argv[2])

    
traces = genfromtxt("Traces/" + name1 + ".dat", delimiter=',')
nb_samples = traces[0].size
nb_inputs = int(traces.size/nb_samples)
print("open traces --- %s seconds ---" % (time.time() - start_time))
step_time = time.time()

inputs = genfromtxt("Data/" + name2 + ".dat", delimiter=',', dtype=np.int16)
nb_candidates = inputs[0].size
print("open leakages --- %s seconds ---" % (time.time() - step_time))
step_time = time.time()

#transpose
power_variance = np.zeros( (nb_samples,nb_inputs), dtype=np.int16  )
power_variance = np.transpose(traces)

leak_variance = np.zeros( (nb_candidates,nb_inputs), dtype=np.int16  )
leak_variance = np.transpose(inputs)

# correlate
corr = np.zeros( (nb_candidates*2,nb_samples))
for idx in range(nb_candidates): # for every key byte
    for idt in range(nb_samples): # for every moment in time
        corr[idx,idt],corr[nb_candidates+(idx),idt] = pearsonr(power_variance[idt],leak_variance[idx])
print("correlations --- %s seconds ---" % (time.time() - step_time))
step_time = time.time()

# Plot the data
x = range(nb_samples)
for i in range(nb_candidates):
    labeli = "byte " + str(i)
    plot.plot(x, corr[i], '-', linewidth=0.5, label=labeli)
plot.legend(loc="upper right", fontsize=8)
plot.title("Pearson correlation")
plot.ylabel("Correlation score")
plot.savefig("Figures/Correlate_" + name1 + "_with_" + name2 + ".png")
plot.show()
