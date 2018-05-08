# Intrusion Detection in Cloud Systems Using Alternative Fuzzy C-Means Clustering and Artificial Neural Networks

This is the codebase for the project by Group#4 developed as a part of course CSC 724 (Advanced Distributed Systems) for credits. The dataset selected is KDD Cup '99 Dataset, which was developed by The Cyber Systems and Technology Group (formerly the DARPA Intrusion Detection Evaluation Group) of MIT Lincoln Laboratory.

We propose to use Alternative Fuzzy C-means Clustering (AFCM) and Artificial Neural Networks (ANN) for building a robust intrusion detection engine. As the part of the project, we modified the open-source implementation provided at https://github.com/HosseinAbedi/FCM/tree/master/fcm, which provides a C implementation for Fuzzy C-mean Clustering (FCM) to integrate the code for AFCM. 3-layer ANN models are developed using the Keras library which provides Sequential models for building these neural networks. We added a custom activation function for 'bipolar sigmoid activation function' by extending the open-source Keras code for our purpose.

The task distribution for the project is as follows:
  1. Algorithm Design (adoneri, dnag) - The AFCM-ANN framework that is developed as part of this project was designed collaboratively. dnag shortlisted the final algorithm to be used for building the IDS with inputs by adoneri for using AFCM as the clustering algorithm.
        
  2. Algorithm Implementation (adoneri, dnag, vsgarg) - dnag implemented the Stage I of the AFCM-ANN framework (afcm.c); adoneri developed the Stage II (keras_ann.py, keras_stage2.py) and intrusion detection engine code for training and testing the framework (engine.py); vsgarg was responsible for developing the Stage III (keras_stage3.py, calcMembershipValues.py) for the framework.
        
  3. Environment Set-up (dnag, vsgarg) - vsgarg created the VMs and dnag created the test scripts (testscript.sh, runIds.sh, generateTrainingData.sh). Code from this repository https://github.com/inigoperona/tcpdump2gureKDDCup99 was modified to suit our requirements of transforming data captured by tcpdump into a format understood by the IDS.
  
  4. Experiment Design (dnag) - dnag designed the test cases and two sets of experiments
  
  5. Experiment Evaluation (adoneri, dnag, vsgarg) - dnag created script to get kdd cup data (generateTestingData.sh), anjali created keras_test.py for outputing results and vsgarg created the script for mounting the attacks using hping3. 
  
  6. Documentation (adoneri, dnag, vsgarg) - dnag wrote the Abstract, Experiments and Limitations sections of the final report; adoneri wrote the Introduction, AFCM section of Design and Algorithm, and Results & Discussion sections of the final report; vsgarg wrote the ANN and Fuzzy Aggregation sections of Design and Algorithm, Related Work & References of the final report. The final editing, graphs and tables were collaboratively done.
  
The entire code is created, compiled and run on Ubuntu 16.04.4 LTS version. 
  
STEPS to create and run Intrusion Detection Engine

Step 1:- ./generateTrainingData.sh   (from dataPreparation folder)

Step 2:- make  (from AFCM folder)

Step 3:- ./afcm train.data  (from AFCM folder)

Step 4:- Install bro using following commands

        4.1:- sudo apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python-dev swig zlib1g-dev 
        (this is for debian based systems)
        
        4.2:- git clone --recursive git://git.bro.org/bro
        
        4.3:- cd bro
        
        4.4:- ./configure
        
        4.5:- make
        
        4.6:- sudo make install
     
Step 5:- Install python libraries

        5.1:- sudo pip install numpy
        
        5.2:- sudo pip install scipy
        
        5.3:- sudo pip install tensorflow
        
        5.4:- sudo pip install scikit-learn
        
        5.5:- sudo pip install h5py

        5.6:- sudo pip install keras
                
Step 6:- python engine.py 

(from ANN folder) this would train and create the models for stage 2 and 3. (since there is no input file it would give an error that cap.txt doesn't exist. On first run the accuracies of each model is printed on screen).
         
Step 7:- create VM environment 

Step 8:- sudo ./runIds.sh

(from ANN folder) The code will launch the engine every 1000 connections and display the percentage distribution of normal and attack packets. "cap.txt" (processed pcap file for input to python is created at this stage for every run). The backup of this cap for future reference is stored in the backup_test folder with a timestamp as the filename. The predictions for this cap_timestamp.txt file is in the log folder with the name cap_predictions_timestamp.txt.
  
Anjali Doneria (adoneri), Dipanjan Nag (dnag), Varun Garg (vsgarg)


Department of Computer Science, North Carolina State University, Raleigh, NC
