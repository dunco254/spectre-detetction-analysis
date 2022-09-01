from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import numpy as np
from bcolors import bcolors
import pickle
class Detector(object):
    def __init__(self, recv_conn, send_conn):
        self.recv_conn = recv_conn
        self.send_conn = send_conn
        self.scaler = self._create_scaler()

    def _create_scaler(self):
        scaler = StandardScaler()
        scaler.mean_ = np.array([1.25175536e+08, 6.29212692e+05, 2.57803834e+06])
        scaler.scale_ = np.array([2.98552228e+08, 1.40878524e+06, 6.23308105e+06])
        return scaler

    def start(self):
        model =  pickle.load(open("new_model.pkl","rb"))
        while True:
            data = self.recv_conn.recv()
            pids = data[0]
            readings = data[1]
            scaled_readings = self.scaler.transform(readings)
            m = scaled_readings.tolist()
            l=[]
            for i in range(len(m)):
               r = m[i]
               r = np.array(r).reshape(1,3)
               res = model.predict_proba(r)[:, 1]
               res = res.tolist()
               l.append(res[0])
            c = sum(l)/len(l)
            if c>0.08:
               print(f'{bcolors.FAIL} A spectre attack has been detected')
               print(f'{bcolors.FAIL}{pids[i]}: {readings[i]}')
            else:
               print(f"{pids[i]}: {readings[i]}")
             
