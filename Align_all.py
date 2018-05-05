####################
####################
# This script looks like Align_prev.py. However it opens ALL the recorded waveform traces (i.e. acquiered using a scope) as weel as the first alignment results obtained previously on the smaller data set.
# Based on the reference pattern all trace are filtered and aligned.
# 465 seconds are needed to handle 10,000 traces.
# File selection is made selectable so the demo data set can be use for shorter computation.
####################
# Author : LoesZe
# Date : 18/04/2018
# Modified : 05/05/2018
####################

#####
# Importing libraries
#####
##
# Numpy is fundamental for scientific computing using python. It deals here with arrays a lot, opens and saves file in CSV form.
import numpy as np
from numpy import pi
from numpy import genfromtxt
##
# SciPy is opeen source software for mathematics, science and engineering. Here it deals with signal processing (i.e. filter). And we may want to use their correlation function.
import scipy as sp
from scipy.signal import butter, lfilter, freqz, filtfilt
from scipy.stats.stats import pearsonr
#undertest
import scipy.spatial as spatial
# Matplotlib is use to generate figures.
import matplotlib.colors as colors
import matplotlib.pyplot as plt
# Tkinter will provide file selection dialog.
##import Tkinter as tk
##from Tkinter import filedialog
# Time will help us to track how long operations take.
import time
start_time = time.time()
#######################################
### Define some usefull functions : ###
#######################################
##
# This function get the raw data in.
# After reshaping the file is saved as a csv file.
def handle_Traces(path,verbose):
    # Data is made with a C program that just apends the sample value and ','
    # So we get an extra emplty column appended.
    # We get that one removed.
    # Finally the properly formated input is saved in /Data/data.csv
    data = genfromtxt(path, delimiter=',')
    data = data[:,:-1]
    #np.savetxt("Data/data.csv", data, delimiter=",")
    if verbose :
        nb_samples = data[0].size
        nb_inputs = data.size/nb_samples
        print ('The input data is %d samples long.' % nb_samples)
        print ('There are %d inputs.' % nb_inputs)
        print ('Hereafter an partial view of this data set:')
        print (data)
    return data
##
# This is a lowpass filter that I need to investigate.
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filtfilt(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

##
# MAIN #
# select file containing all traces
file_path = "IN/Traces.txt"
# and open it.
data = handle_Traces(file_path,1)
nb_samples = data[0].size
nb_trace = int(data.size/nb_samples)

print("get traces: --- %s seconds ---" % (time.time() - start_time))
step_time = time.time()

# get info from alignment perfomed on smaller data set
[first_search,last_search,cutoff,fs,first_sample,last_sample] = genfromtxt('Data/pattern_info.csv', delimiter=',', dtype=np.int32  )
search_range = last_search - first_search

# cut and smooth traces
row_smooth = np.zeros( (nb_trace,search_range), dtype=np.int16  )
for idx in range(nb_trace):
    if (not(idx % 100)):
        print ("smooth : %d/%d"%(idx,nb_trace))
    row_smooth[idx] = butter_lowpass_filtfilt(data[idx,first_search:last_search], cutoff, fs)  

print("smoth traces --- %s seconds ---" % (time.time() - step_time))
print("get + smoth traces --- %s seconds ---" % (time.time() - start_time))
step_time = time.time()

# generating pattern
pattern = genfromtxt("Data/pattern_search_%d_%d_smooth_%d_%d_select_%d_%d.csv"%(first_search,last_search,cutoff,fs,first_sample,last_sample), delimiter=',')
pattern_size = last_sample - first_sample

# aligning all traces
ids_best = np.zeros(nb_trace, dtype=np.int16  )
for idx in range(nb_trace):
    if (not(idx % 500)):
        print ("aligned : %d/%d"%(idx,nb_trace))
    corr = np.zeros( (2,search_range-pattern_size))
    for ids in range(search_range-pattern_size):
        corr[0,ids],corr[1,ids]  = pearsonr(pattern,row_smooth[idx,ids:ids+pattern_size])
        if (corr[0,ids] > corr[0,ids_best[idx]]):
            ids_best[idx] = ids

print("align traces --- %s seconds ---" % (time.time() - step_time))
print("get + smoth + align traces --- %s seconds ---" % (time.time() - start_time))
step_time = time.time()

# generating a new cut, smoothed and aligned data file
data_smooth_aligned = np.zeros( (nb_trace,search_range-ids_best.max()), dtype=np.int16  )
for idx in range(nb_trace):
    data_smooth_aligned[idx] = row_smooth[idx,ids_best[idx]:ids_best[idx]+search_range-ids_best.max()]
np.savetxt("Data/traces_smoothed_aligned.csv", data_smooth_aligned, delimiter=",")

print("create new file --- %s seconds ---" % (time.time() - step_time))
print("get + smoth + align + save traces --- %s seconds ---" % (time.time() - start_time))
