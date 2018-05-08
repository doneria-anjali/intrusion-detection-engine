"""
@author: adoneri
"""

from keras.models import Sequential
from keras.layers import Dense
import calcMembershipValues as membership
import numpy
import time

tstamp = time.time()
file_name = 'cap_' + str(tstamp) + '.txt'

def get_test_data(models):
    num_clusters = len(models)
    
    inputFile = open('cap.txt')
    
    file_final = open('input/test_final.data', 'w')
    
    backup_file = open('backup_test/' + file_name, 'w')
   
    source_attack = []
    for line in inputFile:
        (col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13) = line.split(' ')
        pointData = numpy.asarray([[float(col3), float(col4), float(col5), float(col6), float(col7), float(col8), float(col9), float(col10), float(col11), float(col12), float(col13)]])
        
        source_attack.append([col1, col2])
        
        membershipValue = membership.getMembershipValues(pointData)

        #predict output from all ANN for test data point
        currOut=[]
        for clusterNum in range(num_clusters):
            curr = models[clusterNum].predict(pointData, batch_size=10, verbose=0)
            currOut.append(curr[0])

        outputFromFeed = numpy.matmul(numpy.transpose(currOut),numpy.transpose(membershipValue[0]))
        
        writeStr = ','.join([str(x) for x in outputFromFeed])
        file_final.write(writeStr)
        file_final.write('\n')
        
        #write data to new file
        backup_file.write(line)
        backup_file.write('\n')
         
    file_final.close()
    backup_file.close()
    
    return numpy.asarray(source_attack);
    
def get_attack_index(prediction):
    posValue = float(0.90)
    index = int(0)
    #print(prediction)
    for ind in range(len(prediction)):
        if(prediction[ind] > posValue):
            index = ind
            posValue = prediction[ind]
            
    return index
    
def get_prediction_labels(predictions, source_attack):
    name = 'cap_predictions_' + str(tstamp) + '.txt'
    file_final = open('log/' + name, 'w')
    
    prediction_file = open('log/all_predictions.log', 'a+')
    
    attack = ['normal', 'DoS', 'probe', 'U2R']
    
    normal = 0.0
    dos = 0.0
    probe = 0.0
    u2r = 0.0
    
    total = len(predictions)
    
    for index in range(total):
        attack_ind = get_attack_index(predictions[index])
   
        if attack_ind == 0:
            normal+=1
        if attack_ind == 1:
            dos+=1
        if attack_ind == 2:
            probe+=1
        if attack_ind == 3:
            u2r+=1
            
        ts = time.time()
        readable = time.ctime(ts)
        
        string = [] 
        string.append(readable)
        string.append(" ".join(source_attack[index]))
        string.append(attack[attack_ind])
        
        file_final.write(" ".join(string))
        file_final.write('\n')
        
        prediction_file.write(" ".join(string))
        prediction_file.write('\n')
        prediction_file.write(",".join([str(x) for x in predictions[index]]))
        prediction_file.write('\n')
            
    file_final.close()
    prediction_file.close()
   
    if normal > 0:
        print("Fraction of Normal packets = " + str(normal/total))
    if dos > 0:
        print("Fraction of DoS packets detected = " + str(dos/total))
    if probe > 0:
        print("Fraction of Probe packets detected = " + str(probe/total))
    if u2r > 0:
        print("Fraction of U2R packets = " + str(u2r/total))