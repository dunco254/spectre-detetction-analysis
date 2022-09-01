from keras.models import load_model

import numpy as np
from bcolors import bcolors
import pickle
# this file is loading the model and it is one who is detecting if an attack happend
import pandas as pd
from sklearn.preprocessing import StandardScaler

b = pd.read_csv("spectre.csv")
x = b.drop('label',axis=1)
scaler = StandardScaler()

x=scaler.fit_transform(x)
a = scaler.mean_
b = scaler.scale_


class Detector(object):

    def __init__(self, recv_conn, send_conn):

        self.recv_conn = recv_conn

        self.send_conn = send_conn
        self.scaler = self._create_scaler()


    def _create_scaler(self):
        global a
        global b
        scaler = StandardScaler()
        scaler.mean_ = a
        scaler.scale_ = b
        return scaler


    def start(self):

	    # we are loading the model

        model = pickle.load(open("Logistic_reg.h5","rb"))



        while True:

	        # receiving the values of the counters

            data = self.recv_conn.recv()
            readings = data[1]
            for i in range(len(readings)):
              r = readings[i].tolist()
              r =r + [i*0 for i in range(712-len(r))]
              #print(f"pid:{data[0]} , readings: {readings}")
              r = np.array(r)
              r = r.reshape(1, -1)
              scaled_readings = self.scaler.transform(r)

	            # supply the scaled values to the model
              res = model.predict(scaled_readings) 
              #if np.array2string(res) == "[1.]":

                    #print(f'{bcolors.FAIL}:{data[0][i]}: {readings[i]}')

                    #print("Attack detected")


