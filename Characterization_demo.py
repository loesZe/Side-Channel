####################
# This script opens the recorded waveform traces (i.e. acquiered using a scope). I used Numpy library for that and also in a later stage in order to save the file as a csv file.
# I take a chance here to introduce the Human Interfacing tools I will be using. Matplotlib is one of them. 
####################
# Author : LoesZe
# Date : 15/04/2018
####################

#####
# Importing libraries
#####
##
# Numpy is fundamental for scientific computing using python. It deals here with arrays a lot, opens and saves file in CSV form.
import numpy as np
from numpy import genfromtxt
##
# Matplotlib is use to generate figures :
import matplotlib.colors as colors
import matplotlib.pyplot as plt

##
# This function get the raw data in.
# After reshaping the file is saved as a csv file.
def handle_Traces(path,verbose):
    # Data is made with a C program that just apends the sample value and ','
    # So we get an extra emplty column appended.
    # We get that one removed.
    # Finally the properly formated input is saved in /Data/data.csv
    data = genfromtxt('IN/test.txt', delimiter=',')
    data = data[:,:-1]
    np.savetxt("Data/data.csv", data, delimiter=",")
    
    if verbose :
        nb_samples = data[0].size
        nb_inputs = data.size/nb_samples
        print 'The input data is %d samples long.' % nb_samples
        print 'There are %d inputs.' % nb_inputs
        print 'Hereafter an partial view of this data set:'
        print data
        print 'This data set have been recorded data.csv'

    return data

##
# MAIN #
data = handle_Traces('test.txt',1)
nb_samples = data[0].size
nb_inputs = data.size/nb_samples

################################
#  generate slide "references" #
################################
time = range(nb_samples)
fig = plt.figure()
fig.clf()
fig.suptitle("Traces recorded from scope", fontsize=16)

plot_P_vs_t = plt.subplot("111")
plot_P_vs_t.set_ylabel('Power traces')
plot_P_vs_t.set_xlabel('samples')
#plot_P_vs_t.set_title("Filtered and Aligned Power Traces", fontsize=8)

for idx in range(nb_inputs):
    labeli = "input " + str(idx)
    plot_P_vs_t.plot(time,data[idx], '-', linewidth=0.5, label=labeli)
plot_P_vs_t.legend(loc="upper right", fontsize=8)
plt.savefig('Figures/traces.png')
plt.show()
plt.close()
################################
