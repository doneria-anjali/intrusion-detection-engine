"""
@author: adoneri
"""

import keras_ann as ann

def train(num_clusters):
    models = []
    for i in range(num_clusters):
        j = str(i)
        file_in = "input/cluster_" + j + "_train.csv"
        file_out = "output/cluster_" + j + "_label.csv"
        
        in_data, out_data = ann.get_data(file_in, file_out, True)
        models.append(ann.get_model(in_data, out_data, 11, 14, 4))
        
    return models