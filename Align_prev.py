####################
####################
# This script is built on top of Characterization_demo.py. It opens the recorded waveform traces (i.e. acquiered using a scope).
# Then an Interval of interest is selected. The traces are cut in this interval and smoothed.
# Then the average trace is calculated and an interval selected. This is the "pattern" that is considered as reference.
# All traces are shifted step by step and the best shift is decided using Pearson correlation against the reference pattern.
####################
# Author : LoesZe
# Date : 14/04/2018
# Last review : 05/05/2018
####################

#####
# Importing libraries
#####
##
from __future__ import print_function
import sys
import os
import subprocess
import random
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
# Matplotlib is use to generate figures :
import matplotlib.colors as colors
import matplotlib.pyplot as plot
from matplotlib.patches import Rectangle

#######################################
### Define some usefull functions : ###
#######################################
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
# MAIN #
nb_inputs = 10
name = "traces_nn"
if (len(sys.argv) > 1):
    nb_inputs = int(sys.argv[1])
if (len(sys.argv) > 2):
    name = str(sys.argv[2])
    
data = genfromtxt("Traces/" + name + ".dat", delimiter=',')
data = data[:nb_inputs]
nb_samples = data[0].size

##################################################
#  generate slide "references and time interval" #
##################################################
x = range(nb_samples)
fig, ax = plot.subplots()
plot.ylabel("Voltage (V)")
plot.xlabel("samples")
for idx in range(nb_inputs):
    labeli = "input " + str(idx)
    ax.plot(x,data[idx], '-', linewidth=0.5, label=labeli)
ax.legend(loc="upper right", fontsize=8)
## save and show
plot.title("Power traces recorded with an oscilloscope - Select time interval:")
a = Annotate()
plot.savefig('Figures/traces_record.png')
plot.show()
plot.close()
X0 = int(a.x0)
X1 = int(a.x1)
## decide a time interval for work
print("-- Interval of interest --")
print("start: %d" % X0)
print("stop: %d" % X1)
first_search = X0
last_search = X1
search_range = last_search - first_search
##################################################
## filter Parameters - can be changed when the human interface gets more visual
cutoff = 1500
fs = 50000
##################################################
# Generating the smoothed input data to remove noise
# for this we use butter_lowpass_filtfilt function
data_smooth = np.zeros( (nb_inputs,search_range), dtype=np.int16  )
for idx in range(nb_inputs):
    data_smooth[idx] = butter_lowpass_filtfilt(data[idx,first_search:last_search], cutoff, fs)  

# Generating the average smoothed traces
# this one will be used as a "fair"-reference
data_smooth_avrg = np.zeros(search_range, dtype=np.int16  )
for idx in range(nb_inputs):
    data_smooth_avrg = data_smooth_avrg+data_smooth[idx]
data_smooth_avrg = data_smooth_avrg/nb_inputs

#######################################################
#  generate slide "before-after smooth and reference" #
#######################################################
x = range(search_range)
fig, ax = plot.subplots()
plot.xlabel("samples (within interval of interest)")
ax.plot(x, data_smooth_avrg, 'b', linewidth=1, color='green',label='reference (average)')
for idx in range(nb_inputs):
    labeli = "input " + str(idx)
    ax.plot(x, data_smooth[idx], '--', linewidth=0.5, label=labeli)
ax.legend(loc="upper right", fontsize=8)
## save and show
plot.title("Smoothed power traces - Select pattern:")
a = Annotate()
plot.savefig('Figures/traces_smoothed.png')
plot.show()
plot.close()
#######################################################
## decide a time interval for the pattern recognition
X0 = int(a.x0)
X1 = int(a.x1)
## decide a time interval for work
print("-- Interval of alignment pattern --")
print("start: %d" % X0)
print("stop: %d" % X1)
first_sample = X0
last_sample = X1
pattern_size = last_sample-first_sample
#######################################################

# generating pattern
pattern = np.zeros(pattern_size, dtype=np.int16  )
pattern = data_smooth_avrg[first_sample:last_sample]

#########################################################
# generate slide "alignement using pearson correlation" #
#########################################################
x = range(pattern_size)
figure_trace = plot.figure()
figure_trace.clf()
## sublopt 1 - raw data :
plot_P_vs_t = plot.subplot("111")
plot_P_vs_t.set_ylabel('Shifted traces')
plot_P_vs_t.set_xlabel('samples (+shift)')
plot_P_vs_t.set_title('Aligning using Pearson correlation demo on first input')
plot_P_vs_t.plot(x, pattern, 'b', linewidth=1, color='green',label='Reference pattern')
#scanning search interval for trace ref
corr = np.zeros( (2,search_range-pattern_size))
ids_best = 0
for ids in range(search_range-pattern_size):
    plot_P_vs_t.plot(x, data_smooth[0,ids:ids+pattern_size], '--', linewidth=0.1)
    corr[0,ids],corr[1,ids]  = pearsonr(pattern,data_smooth[0,ids:ids+pattern_size])
    if (corr[0,ids] > corr[0,ids_best]):
        ids_best = ids
plot_P_vs_t.plot(x, data_smooth[0,ids_best:ids_best+pattern_size], 'b', linewidth=1, color='red',label='After Alignement')
plot_P_vs_t.plot(x, data_smooth[0,first_sample:last_sample], 'b', linewidth=1, color='pink',label='Before alignement')
plot_P_vs_t.legend(loc="upper right", fontsize=8)
plot.savefig('Figures/traces_alignement_demo.png')
plot.show()
plot.close()
#########################################################

# scanning all traces to find the best alignement
ids_best = np.zeros(nb_inputs, dtype=np.int16  )
for idx in range(nb_inputs):
    corr = np.zeros( (2,search_range-pattern_size))
    for ids in range(search_range-pattern_size):
        corr[0,ids],corr[1,ids]  = pearsonr(pattern,data_smooth[idx,ids:ids+pattern_size])
        if (corr[0,ids] > corr[0,ids_best[idx]]):
            ids_best[idx] = ids
            
# generating a new cut, smoothed and aligned data file
data_smooth_aligned = np.zeros( (nb_inputs,search_range-ids_best.max()), dtype=np.int16  )
for idx in range(nb_inputs):
    data_smooth_aligned[idx] = data_smooth[idx,ids_best[idx]:ids_best[idx]+search_range-ids_best.max()]

#######################################################
#  generate slide "before-after smooth and reference" #
#######################################################
x = range(search_range-ids_best.max())
figure_trace = plot.figure()
figure_trace.clf()
plot_PS_vs_t = plot.subplot("111")
#plot_PS_vs_t.set_ylabel('Aligned smoothed power traces')
plot_PS_vs_t.set_xlabel('samples (within interval of interest)')
plot_PS_vs_t.set_title('Smoothed and aligned power traces')
for idx in range(nb_inputs):
    labeli = "input " + str(idx)
    plot_PS_vs_t.plot(x, data_smooth_aligned[idx], '-', linewidth=0.5, label=labeli)
plot_PS_vs_t.legend(loc="upper right", fontsize=8)
## save and show
plot.savefig('Figures/traces_smoothed_aligned.png')
plot.show()
plot.close()
#######################################################

## The pattern is saved to align the full batch of traces.
np.savetxt("Data/pattern_search_%d_%d_smooth_%d_%d_select_%d_%d.csv"%(first_search,last_search,cutoff,fs,first_sample,last_sample), pattern, delimiter=",")
## As weel as the parameter for cut smooth and alignement.
np.savetxt("Data/pattern_info.csv",[first_search,last_search,cutoff,fs,first_sample,last_sample], delimiter=",")
