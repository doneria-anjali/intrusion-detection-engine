"""
@author: adoneri
"""

from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy
from keras import optimizers
from keras import backend as K
from keras.utils.generic_utils import get_custom_objects
from keras.models import model_from_json
import os
import warnings
warnings.filterwarnings("ignore")

#custom activation function for activating hidden layer
class bipolarSigmoid(Activation):
    
    def __init__(self, activation, **kwargs):
        super(bipolarSigmoid, self).__init__(activation, **kwargs)
        self.__name__ = 'bipolar_sigmoid'
        
def custom_bipolar_sigmoid(x):
    return (K.sigmoid(x) * 2) - 1

get_custom_objects().update({'bipolar_sigmoid': bipolarSigmoid(custom_bipolar_sigmoid)})

#load input and output data from files
def get_data(file_in, file_out, cols):
    #get training data
    if cols:
        X = numpy.loadtxt(open(file_in, "r"), delimiter = ",", usecols=(0,1,2,3,4,5,6,7,8,9,10))
    else:
        X = numpy.loadtxt(open(file_in, "r"), delimiter = ",")
    
    #get original labels for training data
    out_file = open(file_out, "r")
    out_list = out_file.readlines()
    out_file.close()

    output_list = []
    for line in out_list:
        labelArr = [-1]*4
        index = int(line[0])
        labelArr[index] = float(1)
        output_list.append(labelArr)

    Y = numpy.asarray(output_list)
    
    return X, Y

#define 3-layer ANN model
def get_model(X, Y, input_nodes, hidden_nodes, out_nodes):
    # fix random seed for reproducibility
    numpy.random.seed(7)

    #create model for 3 layer NN
    model = Sequential()
    model.add(Dense(hidden_nodes, input_dim=input_nodes, activation='bipolar_sigmoid'))
    model.add(Dense(out_nodes, activation='linear'))

    #Compile model
    sgd = optimizers.SGD(lr = 0.01, decay = 0, momentum = 0.2, nesterov = False)
    model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])

    #Fit the model
    model.fit(X, Y, epochs=500, batch_size=10, verbose=0)

    #evaluate the model
    scores = model.evaluate(X, Y)
    print("%s: %.2f%%\n" % (model.metrics_names[1], scores[1]*100))
    
    return model

def write_model_to_file(model, model_ind):
    # serialize model to JSON
    model_json = model.to_json()
    with open("model/model" + str(model_ind) + ".json", "w") as json_file:
        json_file.write(model_json)
    
    # serialize weights to HDF5
    model.save_weights("model/model" + str(model_ind) + ".h5")

def write_model_to_file_final(model):
    # serialize model to JSON
    model_json = model.to_json()
    with open("model/final.json", "w") as json_file:
        json_file.write(model_json)
    
    # serialize weights to HDF5
    model.save_weights("model/final.h5")

def load_model_from_file(json_model, hdf5_file):
    # load json and create model
    json_file = open(json_model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    
    loaded_model = model_from_json(loaded_model_json)
    
    # load weights into new model
    loaded_model.load_weights(hdf5_file)

    # evaluate loaded model on test data
    sgd = optimizers.SGD(lr = 0.01, decay = 0, momentum = 0.2, nesterov = False)
    loaded_model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])
    
    return loaded_model