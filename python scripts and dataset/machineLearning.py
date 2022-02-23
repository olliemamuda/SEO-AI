import tensorflow as tf
import pandas as pd
import numpy as np

#inputs the name of the dataset, outputs the tensorflow tensor that will be used for training
def importData():
    #puts together the path of where csv is located
    fileName = 'Dataset-05-01-21.csv'
    filePath = 'C:/Users/ollie/OneDrive/Documents/Ollies Docs/home/a-level computing/project/python scripts and dataset/'+fileName

    #reads the csv (skipping metadata) and seperates features and labels
    csv = pd.read_csv(filePath, skiprows=1, header=None).to_numpy()

    features = []
    labels = []
    for i in range(len(csv)):
        features.append(csv[i, 1:12])
        labels.append(csv[i, 0])

    features = np.array(features)
    labels = np.array(labels)

    return features, labels

#creates a fully connected, 6 layer MLP
def createModel():
    #defines and adds the input layer to the model
    model = tf.keras.Sequential()
    model.add(tf.keras.Input(shape=(11,)))

    #hidden layers
    for i in range(4):
        model.add(tf.keras.layers.Dense(15, activation=tf.nn.relu))

    #output layer
    model.add(tf.keras.layers.Dense(1))
    return model

def trainModel(model, features, labels):
    model.compile(loss = tf.losses.MeanSquaredError(), optimizer = tf.optimizers.Adam())
    model.fit(x=features, y=labels, epochs=50, batch_size=5, validation_split=0.2)
    return model

def run():
    features, labels = importData()
    model = trainModel(createModel(), features, labels)

    model.save('C:/Users/ollie/OneDrive/Documents/Ollies Docs/home/a-level computing/project/python scripts and dataset/models/')
    