from phe import paillier
import pickle
import sys
sys.path.append('..')
from helper import *
import pandas as pd
import time
from sklearn import datasets


""" GENERATING PUBLIC PRIVATE KEY PAIR AND STORING IN A FILE """
public_key, private_key = paillier.generate_paillier_keypair(n_length=1024)
with open('../secrets1024.pkl' ,mode='wb') as f : 
    pickle.dump(public_key,f)
    pickle.dump(private_key,f)


def run_sample_dataset() : 

    """ SAMPLE DATASET GENRATION AND ENCRYPTION """
    start = time.time()

    sample_data = [[1, 2, 3 , 0], [4, 5, 6 , 0], [7, 8, 9 , 0] , [1,5,6,1] , [2,5,8,1] , [3,7,1,1] , [9,4,6,1]]
    sample_query = [2, 3, 6]
    sample_model = SampleDataset(sample_data ,sample_query ,public_key)
    sample_model.process()
    sample_model.encrypt()

    end = time.time()
    print(f'Finished processing sample in {end-start} second(s)')

    with open('../edb1024.pkl' ,mode='wb') as f : 
        pickle.dump(sample_model,f)


def run_iris_dataset() : 

    """ IRIS DATASET GENRATION AND ENCRYPTION """
    start = time.time()

    iris_dataset = datasets.load_iris()

    iris_model = IrisDataset(iris_dataset)
    iris_model.process(iris_dataset)
    iris_model.encrypt(public_key)

    end = time.time()
    print(f'Finished processing iris in {end-start} second(s)')

    with open('../edb1024.pkl' ,mode='wb') as f : 
        pickle.dump(iris_model,f)


def run_breast_cancer_dataset() : 

    """ BREAST CANCER DATASET GENRATION AND ENCRYPTION """
    start = time.time()

    breast_cancer_enn = pd.read_csv('../datasets/breast_cancer_SMOTE_ENN.csv', index_col=None)

    breast_cancer_model = BreastCancerDataset(breast_cancer_enn)
    breast_cancer_model.process()
    breast_cancer_model.encrypt(public_key)

    end = time.time()
    print(f'Finished processing breast cancer in {end-start} second(s)')

    with open('../edb1024.pkl' ,mode='ab') as f : 
        pickle.dump(breast_cancer_model,f)



def run_arrhythmia_dataset() : 

    """ ARRHYTHMIA DATASET GENRATION AND ENCRYPTION """
    start = time.time()

    arrhythmia = pd.read_csv('../datasets/arrhythmia_pca_BDS.csv', index_col=None)

    arrhythmia_model = ArrhythmiaDataset(arrhythmia)
    arrhythmia_model.process()
    arrhythmia_model.encrypt(public_key)

    end = time.time()
    print(f'Finished processing arryhtmia in {end-start} second(s)')

    with open('../edb1024.pkl' ,mode='ab') as f : 
        pickle.dump(arrhythmia_model,f)

def run_car_dataset() : 

    """ CAR DATASET GENRATION AND ENCRYPTION """
    start = time.time()

    car = pd.read_csv('../datasets/car.csv', index_col=None)

    car_model = CarDataset(car)
    car_model.process()
    car_model.encrypt(public_key)

    end = time.time()
    print(f'Finished processing car in {end-start} second(s)')

    with open('../edb1024.pkl' ,mode='ab') as f : 
        pickle.dump(car_model,f)


if __name__ == '__main__' : 
    with open('../edb1024.pkl', 'wb') as f:
        pickle.dump({}, f)

    run_iris_dataset()
    run_breast_cancer_dataset()
    run_arrhythmia_dataset()
    run_car_dataset()
