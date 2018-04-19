# Side-Channel---2---Data-Processing

In this project, we are going to analyse waveforms recorded during DES encryptions using an oscilloscope.
The goal is to find the secret key that was used to encrypt known input data.

In the folder "IN/" some fils can be found :
- inputs.csv contains all the input data send to a smart card in order to be encrypted using a DES algorithm,
- traces.txt contains all the traces (waveforms) recorded during the coresponding encryption,
- traces_demo.txt contains a few number of recorded traces in order to familiarize with our data set, define the time interval of interest and the pattern to be use for alignement. 

A first script "Characterization_demo.py" is used to simply visualize the small data set. It is not necessary to use it.
Then, "Align_demo.py" is built on top of the latter one. This script output a reference "pattern" and a time interval of interest to find this pattern. These information will be used to align all other traces.
Once the interval of interest and the reference patern are selected, the alignement of ALL traces can be done using... "Align_ALL.py". Be careful, in order to perform side channel it is better to have A LOT of traces, which mean also a lot of time to process them. (The script needs 465 seconds to deal with 10,000 traces)
