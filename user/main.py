import pickle
import requests

IRIS_QUERY = [6.0,4.8, 5.2,3,1]

BREAST_CANCER_QUERY = [541.0, 14.47, 24.99, 95.81, 656.4, 0.08837, 0.123, 0.1009, 0.0389, 0.1872, 0.06341, 0.2542, 1.079, 2.615, 23.11, 0.007138, 0.04653, 0.03829, 0.01162, 0.02068, 0.006111, 16.22, 31.73, 113.5, 808.9, 0.134, 0.4202, 0.404, 0.1205, 0.3187, 0.1023]

ARRHYTHMIA_QUERY = [-33.898987062977106, -83.76270133382012, -50.9525413890938, 13.359799665674842, 46.581603515611846, -30.64407502860828, -2.484700794749893, -41.58402965757914, -30.311842969336453, 9.842259137299536, 20.86390839952794, -28.760524017130148, 34.466768907262484, -20.321942305262898, -4.122527281495307, 20.746306318356503, 4.37975316332387, -0.9836170242023612, 1.8666591602775755, 14.48975144765846, 13.093020801885745, -20.107880544737903, -22.08115163300264, -23.57824312811961, -23.073421030509664, -22.593359459515813, -6.763093872156174, 12.704962724231311, -19.50592872337433, 2.82516697657864, 8.165646536457617, -5.93834403530061, -11.076663649416515, 15.574775521300843, 9.56590568441901, -9.735354085285174, -5.536205289316367, 12.98184922592245, 3.356941197686249, -10.94734640892052, 2.559583378992496, 15.165538760326433]

CAR_QUERY = [1, 1, 3, 3, 1, 1]

model_query_mappings = {
    '1' : IRIS_QUERY ,
    '2' : BREAST_CANCER_QUERY ,
    '3' : ARRHYTHMIA_QUERY ,
    '4' : CAR_QUERY
}
model_name_mappings = {
    '1' : 'iris' ,
    '2' : 'breast_cancer' ,
    '3' : 'arrhythmia' ,
    '4' : 'car'
}
public_key =''
with open('../secrets512.pkl' ,mode='rb') as f  :
    public_key = pickle.load(f)

model_choice = input("Please enter model choice\n1)iris\n2)breast_cancer\n3)arrhythmia\n")
# model_choice = '2'
num_rec = "all"
query = [public_key.encrypt(val) for val in model_query_mappings[model_choice]]
data = {}
data['values'] = [ (str(x.ciphertext()), x.exponent) for x in query ]
# print(f"Running for {num_rec} records")
url = f'http://localhost:8000/execute-KNN?model_name={model_name_mappings[model_choice]}&num_rec={num_rec}'
response = requests.post(url , json = data)
print(response.status_code)
# prompt: generate a graph by varying number of records vs KNN time required

# import time

# num_records = [10, 20, 30, 40, 50, 100, 150 ,200 ,250,300 ,455]
# times = []

# def create_graph() : 
#     for num_rec in num_records:
#         start_time = time.time()
#         model_choice = '2'
#         query = [public_key.encrypt(val) for val in model_query_mappings[model_choice]]
#         data = {}
#         data['values'] = [ (str(x.ciphertext()), x.exponent) for x in query ]
#         print(f"Running for {num_rec} records")
#         url = f'http://localhost:8000/execute-KNN?model_name={model_name_mappings[model_choice]}&num_rec={num_rec}'
#         response = requests.post(url , json = data)
#         # print(response.status_code ,response.text)
#         end_time = time.time()
#         times.append(end_time - start_time)


# create_graph()
# print(times)