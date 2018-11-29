import sys
import tensorflow as tf
import numpy as np
import pandas as pd
import os
import gc
from sklearn.metrics import confusion_matrix
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import SimpleRNN,LSTM
from keras.optimizers import RMSprop
from keras.models import load_model
from keras import backend as K
from sklearn.metrics import roc_auc_score

# AUC for a binary classifier  
def auc(y_true, y_pred):  
    ptas = tf.stack([binary_PTA(y_true,y_pred,k) for k in np.linspace(0, 1, 1000)],axis=0)  
    pfas = tf.stack([binary_PFA(y_true,y_pred,k) for k in np.linspace(0, 1, 1000)],axis=0)  
    pfas = tf.concat([tf.ones((1,)) ,pfas],axis=0)  
    binSizes = -(pfas[1:]-pfas[:-1])  
    s = ptas*binSizes  
    return K.sum(s, axis=0)  
# PFA, prob false alert for binary classifier  
def binary_PFA(y_true, y_pred, threshold=K.variable(value=0.5)):  
    y_pred = K.cast(y_pred >= threshold, 'float32')  
    # N = total number of negative labels  
    N = K.sum(1 - y_true)  
    # FP = total number of false alerts, alerts from the negative class labels  
    FP = K.sum(y_pred - y_pred * y_true)  
    return FP/N  
# P_TA prob true alerts for binary classifier  
def binary_PTA(y_true, y_pred, threshold=K.variable(value=0.5)):  
    y_pred = K.cast(y_pred >= threshold, 'float32')  
    # P = total number of positive labels  
    P = K.sum(y_true)  
    # TP = total number of correct alerts, alerts from the positive class labels  
    TP = K.sum(y_pred * y_true)  
    return TP/P  
def np_float32_to_int32(x):
    y = []
    y = np.array(y, dtype=np.int32)
    for i in x:
        if i > 0.5:
            y = np.append(y,1)
        else:
            y = np.append(y,0)
    return y

def toImageSet(x,height):
    num = len(x[:,0])
    #height = 100
    width = len(x[0])
    out = np.zeros((num,height,width), dtype='int8')

    for n in range(num):
        for i in range(width):
            count = int(x[n,i] * height)
            out[n, height-count: height, i] = 1
    return out	

def main():
    if len(sys.argv) < 2:
        print ("\nUsage: %s need a file name\n" % sys.argv[0])
        sys.exit(1)

    inputFileName = sys.argv[1]
       
    K.clear_session()

    model = load_model('VGG16_5485_For5.h5')
    height = 128

    outputFileName = os.path.splitext(inputFileName)[0] + ".out.csv"

    df = pd.read_csv(inputFileName, header=None)
    df.round(5)

    x_input = df.iloc[:,0:1800].values.astype('float32')
    #print (x_input.shape)
    x_Img = toImageSet(x_input,height)
    #print(x_Img.shape)
    x_Img = x_Img.reshape(x_Img.shape[0], height, 1800, 1).astype('float32')

    y_pred = model.predict(x_Img)

    K.clear_session()

    y_pred = np_float32_to_int32(y_pred)
    y_pred = np.reshape(y_pred,(y_pred.size,1)) 

    outCombine = np.append(x_input, y_pred, axis = 1)
    out_csv = pd.DataFrame(outCombine)

    out_csv.to_csv(outputFileName, header=False, index=False)
    gc.collect()

if __name__ == "__main__":
    main()
