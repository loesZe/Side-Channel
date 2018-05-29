-------------------------------------------------------------
 Get your Pi ready :
-------------------------------------------------------------
to communicate with card readers:
	sudo apt-get install opensc pcscd libccid
	opensc-tool --list-readers
and, to access it using python:
	sudo apt-get install python-pyscard
and then, to get the scope workng, follow :
	http://scruss.com/blog/2013/12/15/my-raspberry-pi-talks-to-my-oscilloscope/

-------------------------------------------------------------
 Command description :
-------------------------------------------------------------

-- Smart_card.py --
Encrypt a given number of random input messages with different keys loaded. Usefull to run when getting the Oscilloscope ready.

	% cd Utilities/
	% python Smart_card.py
	% cd ..

-- get_traces.py --
Record a data set. The set is made of <number of traces> traces. They are labeled, <file name>.
If no "cut" bondaries, a selection should be made on the figure in order to determine the time interval of interest.
If "cut" is defined with <start> and <stop> values, then a smaller part of traces is recorded.
In this file the key is defined as 0x0102030405060708 :
	nb: LOAD_KEY = [0xA0, 0x0B, 0x00, 0x00, 0x08, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08] 

	% sudo python get_traces.py <number of traces> <file name>

-- correlation.py --
Correlate the traces recorded in the folder Traces/ with leakage hypothesis placed in the folder Data/.

	% sudo python correlation.py <traces> <leakages>

-- align_prev.py --
Align (selection of interval) <number of traces> of cut (selection of interval) and smoothed traces.

	% python align_prev.py <number of traces>  <batch name>

-- align_all.py --
Cut Smooth and Align all traces of <batch name>.

	% python align_all.py <batch name>

-- leak_R.py  --
Calculate leakage during <round number> based on the inputs of the batch (named <batch name>).

	% python leak_R.py <batch name> <round number>

-- key_guess_R --
Try to guess the <round number> round sub_key of the DES.

	% python key_guess_R.py <round number>

-------------------------------------------------------------
 Command flow for acquisitions :
-------------------------------------------------------------

> sudo python get_traces.py 20 traces_prev
	Available readers:  ['OMNIKEY AG 3121 USB 00 00']
	Using: OMNIKEY AG 3121 USB 00 00
	--- 19.4324669838 seconds ---
	press
	release
	start: 3255
	stop: 4906
		
> sudo python get_traces.py 2000 traces_2000 3255 4906
	Available readers:  ['OMNIKEY AG 3121 USB 00 00']
	Using: OMNIKEY AG 3121 USB 00 00
	--- 1775.292732 seconds ---
	
> python correlation.py traces_2000 traces_2000_in
	open traces --- 22.8983068466 seconds ---
	open leakages --- 0.14913392067 seconds ---
	correlations --- 9.36745214462 seconds ---

> python correlation.py traces_outputs traces_2000_out
	open traces --- 22.9663069248 seconds ---
	open leakages --- 0.146953105927 seconds ---
	correlations --- 9.26957798004 seconds ---

-------------------------------------------------------------
 Command flow for data peparation :
-------------------------------------------------------------

> python align_prev.py 10 traces_2000
	press
	release
	-- Interval of interest --
	start: 766
	stop: 912
	press
	release
	-- Interval of alignment pattern --
	start: 31
	stop: 98
	
> python align_all.py traces_2000 0
	round : 0
	get traces: --- 21.021584034 seconds ---
	smooth : 0/2000
	smooth : 100/2000
	[...]
	smooth : 1900/2000
	smoth traces --- 4.0495159626 seconds ---
	get + smoth traces --- 25.0713999271 seconds ---
	aligned : 0/2000
	aligned : 500/2000
	aligned : 1000/2000
	aligned : 1500/2000
	align traces --- 50.0181560516 seconds ---
	get + smoth + align traces --- 75.0896408558 seconds ---
	create new file --- 0.791683912277 seconds ---
	get + smoth + align + save traces --- 75.8813948631 seconds ---

-------------------------------------------------------------
 Command flow for Side channel :
-------------------------------------------------------------

> python leak_R.py traces_2000 0
	round : 0
	open inputs--- 0.18065905571 seconds ---
	sixet_0
	input handeled : 0/2000
	input handeled : 500/2000
	input handeled : 1000/2000
	input handeled : 1500/2000
	last --- 43.8948509693 seconds ---
	[...]
	sixet_7
	input handeled : 0/2000
	input handeled : 500/2000
	input handeled : 1000/2000
	input handeled : 1500/2000
	last --- 46.2623620033 seconds ---
	all --- 365.183845997 seconds ---

> python key_guess_R.py 0
	[...]
	open leakage --- 6.60930919647 seconds ---
	power variance --- 0.000413179397583 seconds ---
	leak variance --- 0.00018310546875 seconds ---
	correlations --- 6.3912320137 seconds ---
	Best score (max): 0.067115
	obtained for key_3
	Worst score (max): -0.042201
	obtained for key_63
	total --- 107.411015987 seconds ---
	best candidate          : 000000000000000000100000000100110010101010000011 
	best candidate2         : 000000000000000000111011110111101101011111110001 
	worst candidate         : 111110111111111111111111111111111111111111111111 

-------------------------------------------------------------
 Results on round key 0 :
-------------------------------------------------------------

best candidate          	: 000000 000000 000000 100000 000100 110010 101010 000011  
the correct sub key is	 	: 000000 000000 000000 000000 000100 110010 101010 000010

-------------------------------------------------------------
 Pre-conclusions :
-------------------------------------------------------------

2000 traces are not enough to find out the first round key. 	:(
But we are seriously close of the correct key.				:)
And we get there that in very limited amount of time.	 			:)

-------------------------------------------------------------
 Command flow for Side channel :
-------------------------------------------------------------

> python leak_R.py traces_2000 1
	round : 1
	open inputs--- 0.178271055222 seconds ---
	sixet_0
	input handeled : 0/2000
	input handeled : 500/2000
	input handeled : 1000/2000
	input handeled : 1500/2000
	last --- 42.6916601658 seconds ---
	[...]
	sixet_7
	input handeled : 0/2000
	input handeled : 500/2000
	input handeled : 1000/2000
	input handeled : 1500/2000
	last --- 43.7192249298 seconds ---
	all --- 344.121645927 seconds ---

python key_guess_R.py 1
	[...]
	open leakage --- 6.68929696083 seconds ---
	power variance --- 0.00048303604126 seconds ---
	leak variance --- 0.000189065933228 seconds ---
	correlations --- 6.42830204964 seconds ---
	Best score (max): 0.088885
	obtained for key_50
	Worst score (max): -0.030319
	obtained for key_63
	total --- 108.789808989 seconds ---
	best candidate          : 110000010100111111110101110001000100010011110010 
	best candidate2         : 011110001011110101100000001100111110101000111001 
	worst candidate         : 111111111111111110111110011101111111111110111111

-------------------------------------------------------------
 Results on round key 1 :
-------------------------------------------------------------

best candidate          	: 110000 010100 111111 110101 110001 000100 010011 110010 
the correct sub key is	 	: 000000 000000 000000 000000 000100 000010 001100 000111

-------------------------------------------------------------
 Almost-conclusions :
-------------------------------------------------------------

some little error became bigger. 	:(

-------------------------------------------------------------
 Command flow to get back to the best key candidate :
-------------------------------------------------------------

> python ##TO DO##

-------------------------------------------------------------
 Questionning :
-------------------------------------------------------------

Maybe another key would have leaked more.
Maybe a better analog filtering would have provide better data set.
Maybe post processing operation fuzzed the leakage over time.
Maybe alignement is to be questioned.
Maybe the input handeling effect over the power consumption should be considered.
	This information can be used to ponderate later correlation with key hypothesis.

					...So many parameters to be played with.

-------------------------------------------------------------
 Command flow for an extra acquisitions ?
-------------------------------------------------------------

> sudo python get_traces.py 20 traces_prev
	Available readers:  ['OMNIKEY AG 3121 USB 00 00']
	Using: OMNIKEY AG 3121 USB 00 00
	--- 19.6282260418 seconds ---
	press
	release
	start: 3709
	stop: 4217

> sudo python get_traces.py 5000 traces_all 3709 4217
	Available readers:  ['OMNIKEY AG 3121 USB 00 00']
	Using: OMNIKEY AG 3121 USB 00 00
	--- 4441.59061003 seconds ---
