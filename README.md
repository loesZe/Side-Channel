# Side-Channel---2---Data-Processing
# Author : LoesZe 
---------------------			RaspberryPi 3B
 Usual command flow:		
---------------------		time(second)	time(minute)
% python Align_prev.py 		-
% python Align_all.py 		538.5		9
% python Leak_R.py 0		1790.9		30
% python Key_guess_R.py 0	668.7		11
% python Leak_R.py 1		1796.9		30
% python Key_guess_R.py 1	648.5		11
% python Reconstruct.py		-
---------------------			total:	> 1h30m
-------------------
 Flow Description:
-------------------
In this project, I will get some input data recoreded in Side-Channel---1---Data-Acquisition. 
An IN/ folder consist of: 
	Inputs.dat	% N inputs 8bytes messages. 
	Traces.txt	% N power traces recorded during a the DES encryption of corresponding input.
	Traces_prev.txt	% M power traces recorded during a DES encryptions. Used to have have an overview of the main data set (Inputs.dat and Traces.txt)

First Align_prev.py can be run.
It shows the demo data set Traces_prev.txt and ask for a first "Interval of interest".
This time interval must picture confortable pattern for alignment and information leakage from the DES encryption.
It shows then, the preview data set cut and smoothed (together with an averaged traces) and ask for an "Interval of alignment".
This time interval must picture a pattern for the alignement that will be stored.
> Data/pattern_info.csv contain the time interval selection WW-XX and YY-ZZ
> Data/pattern_search_WW_XX_smooth_1500_50000_select_YY_ZZ.csv

Example:
% python Align_prev.py 
	The input data is 480 samples long.
	There are 50 inputs.
	Hereafter an partial view of this data set:
	[[ 11.  10.   9. ...,  -4.  -7.  -5.]
	 [  6.   3.   0. ...,  -6.  -8. -10.]
	 [ 11.   9.   6. ...,  -5.  -6. -27.]
	 ..., 
	 [ 20.  24.  25. ...,  -9.  -7.  -4.]
	 [ 21.  21.  19. ...,   5.   2.  -3.]
	 [-14. -16. -18. ..., -22. -17. -13.]]
	-- Interval of interest --
	first: (50)50
	last: (300)300
	-- Interval of alignment pattern --
	first: (42)42
	last: (202)202
> Data/pattern_info.csv
> Data/pattern_search_50_300_smooth_1500_50000_select_42_202.csv

Then Align_all.py can be run for all other power traces to be aligned with the previously defined pattern.
This script opens the main data set Traces.txt and apply the same transformations previously applyed to the demo data set when running Align_prev.py.
> Data/traces_smoothed_aligned.csv

Example:
% python Align_all.py 
	The input data is 480 samples long.
	There are 10000 inputs.
	Hereafter an partial view of this data set:
	[[ -8.  -5.  -7. ..., -11. -11. -11.]
	 [  7.   4.   3. ..., -17. -13. -10.]
	 [  3.   1.  -1. ..., -14. -34. -29.]
	 ..., 
	 [  2.  15.  19. ...,  -8.  -6.  -5.]
	 [ 33.  54.  45. ...,  -1.  -1.  -4.]
	 [ 23.  23.  12. ...,  -5.  -1.  -1.]]
	get traces: --- 26.4998211861 seconds ---
	smooth : 0/10000
	smooth : 100/10000
	% [...] %
	smooth : 9900/10000
	smoth traces --- 30.8046917915 seconds ---
	get + smoth traces --- 57.3046681881 seconds ---
	aligned : 0/10000
	aligned : 500/10000
	% [...] %
	aligned : 9500/10000
	align traces --- 483.703071833 seconds ---
	get + smoth + align traces --- 541.00785017 seconds ---
	create new file --- 6.84966492653 seconds ---
	get + smoth + align + save traces --- 547.857644081 seconds ---
> Data/traces_smoothed_aligned.csv	

Now, the information leakage need to be interpreted into an actual readable value: the secret key.

If we considere the very first round of the DES, 2^6 = 64 round key hypothesis can be made for every sixets.
Together with a known input message, these round key hypothesis lead to 64 different sets of data being processed.   
Based on a pre-define power leakage model a leakage score can be given to every key hypothesis.

Taaadaa, Leak_R.py calculates the hypothetical leakage for a specific round (0 or 1) of the DES encryption for all input messages.
The sixets constinuting the round_key are processed one after the other.
For every input (m1, m2, .., m.), 64 different sixet hypothesis (k0 k1 k2 ..  k65) are considered in order to calculate the corresponding leakage score.
a result file leak_(sixet).csv is built as follow:
	## k0 k1 k2 ..  k65
   	#m1
   	#m2
    	#..    leak(..,..)
    	#m.
When the second round of the DES (round=1) is considered, the previous round key need to be guessed. 
> Data/R(round)/leak_(sixet).csv

Example:
% python Leak_R.py 0
	open inputs--- 0.660098075867 seconds ---
	sixet_0
	input handeled : 0/10000
	input handeled : 500/10000
	% [...] %
	input handeled : 9500/10000
	last --- 230.646135092 seconds ---
	all until now --- 231.306571007 seconds ---
	sixet_1
	input handeled : 0/10000
	% [...] %
	input handeled : 9500/10000
	last --- 228.093240023 seconds ---
	all until now --- 1834.94464707 seconds ---
	all --- 1834.94467998 seconds ---
> Data/R0/leak_0.csv
> Data/R0/leak_1.csv
> Data/R0/leak_2.csv
> Data/R0/leak_3.csv
> Data/R0/leak_4.csv
> Data/R0/leak_5.csv
> Data/R0/leak_6.csv
> Data/R0/leak_7.csv

Then, for every sixet, Key_guess_R.py get the N traces and N times 64 leakage scores.
The N traces represents the actual power leakage of the DES encrypting N input messages.
The leakage model considered depends on the 64 possible sixet values. 
Key_guess_R.py returns which sixet value correlate best with the actual leakage.
> OUT/key_guess_(round).dat

Example:
% python Key_guess_R.py 0
	open traces --- 12.3247048855 seconds ---
	open leakage --- 4.87338399887 seconds ---
	power variance --- 0.00322890281677 seconds ---
	leak variance --- 0.00116205215454 seconds ---
	correlations --- 89.46946311 seconds ---
	Best score (max): 0.097303
	obtained for key_0
	flattening --- 0.0892448425293 seconds ---
	Best score (diff to mean max): 0.097295
	obtained for key_0
	cummulating --- 0.0540328025818 seconds ---
	Best score (cummulative  diff to mean): 6.336449
	obtained for key_0
	open leakage --- 13.9158899784 seconds ---
	% [...] %
	obtained for key_2
	total --- 832.727024794 seconds ---
	best candidate          : 000000000000000000000000000100110010101010000010 
	best candidate (max)    : 000000000000000000000000000100110010101010000010 
	best candidate (cummul) : 000000000000000000000000000100110010101010000010
> OUT/key_guess_0.dat

Now that we have a candidate for the first round key, the hypothetical leakage for next round can be calculated using Leak_R.py.
And these leakage scores can be used to predicte the next best round key candidate using Key_guess_R.py.

Example:
% python Leak_R.py 1
% python Key_guess_R.py 1

> Data/R1/leak_0.csv
> Data/R1/leak_1.csv
> Data/R1/leak_2.csv
> Data/R1/leak_3.csv
> Data/R1/leak_4.csv
> Data/R1/leak_5.csv
> Data/R1/leak_6.csv
> Data/R1/leak_7.csv
> OUT/key_guess_1.dat

Finally, Reconstruct.py makes the results -maybe more readable- and certainly more dramatic.
Combinating key_guess_0.dat and key_guess_1.dat, the SECRET KEY can be reconstructed!!
> OUT/key_guess.dat

Example:
% python Reconstruct.py
	key_0   : 0000000000000010000000100000010000000100000000100000011000001000
	key_1   : 0000000000000010000000100000010000000000000001100000011000000000
	key     : 0000000000000010000000100000010000000100000001100000011000001000
	key(hex): 00 02 02 04 04 06 06 08
> OUT/key_guess.dat
-------------------
NOTE : 0x"00 02 02 04 04 06 06 08" and 0x"01 02 03 04 05 06 07 08" will both lead to key(hex) = 0x"00 02 02 04 04 06 06 08".
Because the parity bit is not used, every last bit of every byte of the key can be changed without impact on the encryption result.
---------------
 Dependencies:
---------------
Numpy
Scipy
Matplotlib
-
I might use Tkinter to select a file in a near future. But it is commented out for now.