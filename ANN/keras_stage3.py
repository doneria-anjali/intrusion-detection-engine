"""
@author: vsgarg
"""

import keras_ann as ann
import keras_stage2 as stage2
import numpy

def getMembershipVal(lineNo):
    membershipFile = open('../AFCM/membership.matrix','r')
    for i, line in enumerate(membershipFile):
        if i == (int(lineNo) +1):
            (val1, val2, val3, val4, val5) = line.strip().split(' ')
            return [float(val2), float(val3), float(val4), float(val5)]

def get_final_data(models):
    file_final = open('input/inputToStage_3.data', 'w')
    
    num_clusters = len(models)
    
    for i in range(num_clusters):
        j = str(i)
        inputFile = open('input/cluster_' + j + '_train.csv')
        pointData = []
        currOut = []
        for line in inputFile:
            (col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12) = line.split(',')
            pointData = numpy.asarray([[float(col1), float(col2), float(col3), float(col4), float(col5), float(col6), float(col7), float(col8), float(col9), float(col10), float(col11)]])
            
            membershipValue = getMembershipVal(col12)
            
            #predict output from all ANN for jth data point
            for clusterNum in range(num_clusters):
                curr = models[clusterNum].predict(pointData, batch_size=10, verbose=0)
                currOut.append(curr[0])
            
            #get input for final ANN by multiplication of output of each data point to each ANN 
            #and its corresponding memebership to each cluster
            outputFromFeed = numpy.matmul(numpy.transpose(currOut),numpy.transpose(membershipValue)) 
  
            writeStr = ','.join([str(x) for x in outputFromFeed])
            file_final.write(writeStr)
            currOut=[]
            file_final.write('\n')

    file_final.close()

    filenames = ['output/cluster_0_label.csv', 'output/cluster_1_label.csv', 'output/cluster_2_label.csv', 'output/cluster_3_label.csv']
    with open('output/combinedFile', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

    return ann.get_data("input/inputToStage_3.data","output/combinedFile", False)

def get_final_ann(X, Y):
    #create final ANN
    final_ann = ann.get_model(X, Y, 4, 13, 4)
    
    return final_ann