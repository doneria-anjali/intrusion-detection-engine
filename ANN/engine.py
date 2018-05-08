"""
@author: adoneri
"""

import keras_stage2 as stage2
import keras_stage3 as stage3
import keras_ann as ann
import os
import keras_test as test
import numpy
import warnings
warnings.filterwarnings("ignore")

#function to retrieve the saved neural network models
def get_model_list(num_clusters):
    models = []
    for model_ind in range(num_clusters):
        models.append(ann.load_model_from_file("model/model" + str(model_ind) + ".json", "model/model" + str(model_ind) + ".h5"))
    return models

"""
IDS engine code that creates ANN models for Stage II and Stage III, 
trains them, saves them to model/, retrieves them for detecting attacks on
incoming packets/test packets and prepares input for Stage III ANN
"""
def main():        
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    
    #Because we want to categorize packets into Normal and 3 kinds of attacks (DoS, Probe, U2R)
    num_clusters = 4
    
    #1. Train Stage II ANNs
            #-----------------Skip this step if models are stored-------------------#
    stored = False
    if os.path.isfile("model/model0.json"):
        stored = True

    if not stored:
        print("Training " + str(num_clusters) + " ANNs for prediction")
        stage2_ann = stage2.train(num_clusters)
        #save these ANN to a file
        for index in range(num_clusters):
            ann.write_model_to_file(stage2_ann[index], index)
            stored = True

    #2. Prepare input and true labels for training Stage III ANN
    models = []
    if not os.path.isfile("input/inputToStage_3.data"):
        print("Preparing input for final ANN")    
        if stored:
            models = get_model_list(num_clusters)
        else:
            models = stage2_ann

        in_data, out_data = stage3.get_final_data(models)
    else:
        in_data, out_data = ann.get_data("input/inputToStage_3.data","output/combinedFile", False)

    #3. Train Stage III ANN
    if not os.path.isfile("model/final.json"):
        print("Training final ANN")
        final_ann = stage3.get_final_ann(in_data, out_data)
        ann.write_model_to_file_final(final_ann)

    #4. Predict output for test packets
    if os.path.isfile("model/final.json"):
        if not models:
            models = get_model_list(num_clusters)
        
        #generate input test file
        source_attack = test.get_test_data(models)
        
        test_data = numpy.loadtxt(open("input/test_final.data", "r"), delimiter = ",")
        
        #load Stage III ANN and predict for test packets
        loaded_model_final = ann.load_model_from_file('model/final.json', 'model/final.h5')
        prediction = loaded_model_final.predict(test_data, batch_size=10, verbose=0)
        
        test.get_prediction_labels(prediction, source_attack)
    else:
        print("No trained ANN found for final prediction")
        
main()
