from phe import paillier
import pickle
from helper import IrisDataset,BreastCancerDataset,ArrhythmiaDataset,CarDataset
import random
from server1.schemas import QueryRequest
import requests
import copy
import concurrent


def get_public_private_key_pair() :
    PUBLIC_KEY : paillier.PaillierPublicKey =''
    PRIVATE_KEY : paillier.PaillierPrivateKey =''
    with open('./secrets512.pkl' ,mode='rb') as f : 
        PUBLIC_KEY = pickle.load(f)
        PRIVATE_KEY = pickle.load(f)
    return PUBLIC_KEY,PRIVATE_KEY

public_key , private_key = get_public_private_key_pair()

def get_model_data(model_name) : 
    IRIS_MODEL : IrisDataset =''
    BREAST_CANCER_MODEL : BreastCancerDataset =''
    ARRHYTHMIA_MODEL : ArrhythmiaDataset =''
    CAR_MODEL : CarDataset
    with open('./edb512.pkl' ,mode='rb') as f : 
        IRIS_MODEL = pickle.load(f)
        BREAST_CANCER_MODEL = pickle.load(f)
        ARRHYTHMIA_MODEL = pickle.load(f)
        CAR_MODEL = pickle.load(f)
    model_mappings = {'iris' : IRIS_MODEL , 'breast_cancer' : BREAST_CANCER_MODEL , 'arrhythmia' : ARRHYTHMIA_MODEL 
                      ,'car' : CAR_MODEL}
    return model_mappings[model_name]
    return 1

def deserialize_input(received_dict : QueryRequest) : 
    enc_nums_rec = []
    for x in received_dict.values:
        if isinstance(x[0] ,list) : 
            tmp = []
            for ele in x : 
                tmp.append(paillier.EncryptedNumber(public_key, int(ele[0]), int(ele[1]))) 
            enc_nums_rec.append(tmp)   
        else : 
            enc_nums_rec.append(paillier.EncryptedNumber(public_key, int(x[0]), int(x[1])))
    return enc_nums_rec


def randomize(a ,ra) :
  if isinstance(a ,list) :
    ans = []
    for i in range(len(a)) :
      ans.append(a[i]+ra)
    return ans
  else :
    ans = a + ra
    return ans


def derandomize(a, ra):
  if isinstance(a ,list) :
    ans = []
    for i in range(len(a)) :
      ans.append(a[i] - ra)
    return ans
  else :
    ans = a - ra
    return ans

def derandomize_mult(a,b,ra,rb,mult_res) :
  n = public_key.n
  a_rb = a * rb
  b_ra = b * ra
  ra_rb = ra*rb
  
  mult_res = mult_res - a_rb
  mult_res = mult_res - b_ra
  mult_res = mult_res - ra_rb
  return mult_res


def SM_P1(a, b):

   ra = random.getrandbits(25)
   rb = random.getrandbits(25)
   ad = randomize(a , ra)
   bd = randomize(b , rb)
   data = {}
   data['values'] = [ (str(x.ciphertext()), x.exponent) for x in [ad,bd] ]
   response = requests.post('http://localhost:3000/get-sm-result' , json = data)
   x = response.json()
   result =  paillier.EncryptedNumber(public_key, int(x[0]), int(x[1]))
   res = derandomize_mult(a,b,ra,rb,result)
   return res
  

def SSED(P, Q):
    
    squared_dist = []
    records = P if isinstance(P[0] , list) else [P]
    # cnt = 1
    for row in records :     
            
        diff , diff2 = [] , []
        for i in range(len(row) - 1) : 
            diff.append(row[i] - Q[i])
        # arr_x = [x for x in diff]
        # with concurrent.futures.ProcessPoolExecutor() as executor  :
        #     diff2 = executor.map(SM_P1 , arr_x , arr_x)
        diff2 = [SM_P1(x,x) for x in diff]
        tot_dist = public_key.encrypt(0)
        for i in diff2:
            tot_dist = tot_dist + i
        squared_dist.append(tot_dist)
        # print("Completed row " ,cnt)
        # cnt = cnt + 1
    return squared_dist

def prepare_distance_label(dist, data):
    distance_label = []
    # encrypting all tuple elements
    for i in range(len(dist)):
        r_id = public_key.encrypt(i)
        r_dist = dist[i]
        r_clabel = data[i][-1]
        distance_label.append([r_id, r_dist, r_clabel])

    return distance_label

def SELIM_C2(distance_label , E_maxVal , E_zero) :
    found = 0
    distance_to_add = []
    for d in distance_label :
        decrypt_d = private_key.decrypt(d[1])
        if decrypt_d or found :
            distance_to_add.append(E_zero)
        else  :
            found = 1
            distance_to_add.append(E_maxVal)
    return distance_to_add

def SELIM_C1(distance_label  , mn ) :
    # Substracting all distances from minimum
    res = []
    for i in range(len(distance_label)) :
        distance_label[i][1] = (distance_label[i][1] - mn[1]) 
        res.append(distance_label[i])

    return res

def SELIM(distance_label ,mn ,max_val) :
    distance_label2 = copy.deepcopy(distance_label)
    updated_distance_label1 = SELIM_C1(distance_label2 , mn)

    data = {}
    data['values'] = [[(str(x.ciphertext()), x.exponent) for x in lst] for lst in updated_distance_label1]
    data['values'].extend((str(x.ciphertext()), x.exponent) for x in [public_key.encrypt(max_val),public_key.encrypt(0)])

    response = requests.post('http://localhost:3000/get-selim-result' , json = data)
    result = response.json()
    distance_to_add = []
    for r in result : 
       distance_to_add.append(paillier.EncryptedNumber(public_key, int(r[0]), int(r[1])))
    for i in range(len(distance_label2)) :
        distance_label[i][1] = (distance_label[i][1] + distance_to_add[i])
    return distance_label2


def find_nearest_C1(distance_label):
    mn = distance_label[0]
    sz = len(distance_label)
    for i in range(1 ,sz):
        r = random.getrandbits(50)
        mn = randomize(mn ,r )
        curr = randomize(distance_label[i] , r)

        data = {}
        data['values'] = [
          [(str(x.ciphertext()), x.exponent) for x in lst] for lst in [mn,curr] 
        ]

        response = requests.post('http://localhost:3000/get-smin-result' , json = data)
        result = response.json()  
        mn =[paillier.EncryptedNumber(public_key , int(ele[0]) ,int(ele[1])) for ele in result]
        
        mn = derandomize(mn ,r )
    return mn

def compare(a,b) : 
    r = random.getrandbits(50)
    curr = randomize(a ,r )
    next = randomize(b, r)
    data = {}
    data['values'] = [
      [(str(x.ciphertext()), x.exponent) for x in lst] for lst in [curr,next] 
    ]

    response = requests.post('http://localhost:3000/get-smin-result' , json = data)
    result = response.json()  
    mn =[paillier.EncryptedNumber(public_key , int(ele[0]) ,int(ele[1])) for ele in result]
    
    mn = derandomize(mn ,r )
    return mn

def find_nearest_C1_parallel(distance_label):

    sz = len(distance_label)
    if sz == 1 : 
        return distance_label[0]
    new_list = []
    if sz & 1 : 
        last_label = distance_label.pop(-1)
        new_list.append(last_label)
        sz = sz  - 1
    
    with concurrent.futures.ProcessPoolExecutor() as executor  :
        for r in executor.map(compare ,[distance_label[i] for i in range(sz) if i % 2 == 0] ,[distance_label[i] for i in range(sz) if i & 1]) : 
            new_list.append(r)

    return find_nearest_C1_parallel(new_list)



def KMIN_C1(distance_label, k):
    knearest = []

    for i in range(k):
        nearest = find_nearest_C1(distance_label)
        # 100 is just written for sample example , please use appropriate max value for this
        knearest.append(nearest)
        SELIM(distance_label , nearest, 1000000000)

    return knearest




class Shuffle : 

    def __init__(self , data) -> None:
        n = len(data)
        self.block_size = random.randint(2,len(data))
        self.rotation_amount = []
        for i in range(((n + self.block_size - 1)//self.block_size)) :
            r = min(i * self.block_size + self.block_size ,len(data) )
            l = i * self.block_size
            currLen = r - l 
            self.rotation_amount.append(random.randint(1, currLen))
        self.rotation_full = random.randint(0 , len(data) - 1) 


    def shuffle(self , data) -> None:
        
        i = 0 
        while i < len(data) : 
            j = min(len(data) , i + self.block_size )
            ind = (j-1)//self.block_size
            k = j - self.rotation_amount[ind]
            data[i : j] = data[k : j] + data[i : k]
            i = j

        data[:] = data[-self.rotation_full:] + data[:-self.rotation_full]

    def deshuffle(self , data) -> None : 
        i = 0 
        data[:] = data[self.rotation_full:] + data[:self.rotation_full]
        while i < len(data) : 
            j = min(len(data) , i + self.block_size )
            ind = (j-1)//self.block_size
            k = self.rotation_amount[ind]
            data[i : j] = data[i + k : j] + data[i :i + k]
            i = j

""" SECURE MAXIMUM """
def SMAX_P1(freq_labels):
    k = len(freq_labels)
    
    mx = freq_labels[0]
    for i in range(1, k):
        r = random.getrandbits(50)

        mx = randomize(mx, r)
        r_cur = randomize(freq_labels[i], r)

        data = {}
        data['values'] = [
          [(str(x.ciphertext()), x.exponent) for x in lst] for lst in [mx,r_cur] 
        ]

        response = requests.post('http://localhost:3000/get-smax-result' , json = data)
        result = response.json()  
        mx =[paillier.EncryptedNumber(public_key , int(ele[0]) ,int(ele[1])) for ele in result]
        
        mx = derandomize(mx, r)
    
    return mx


def SMAX(freq_labels) : 
    return SMAX_P1(freq_labels)


""" SECURE FREQUENCY """
def SF_P1(k_nearest_labels, all_labels):
    k = len(k_nearest_labels)
    w = len(all_labels)

    S = [[all_labels[j] - k_nearest_labels[i] for j in range(w)] for i in range(k)]

    shuffle_obj_list = [Shuffle(row) for row in S]

    for row,shuffle_obj in zip(S ,shuffle_obj_list) : 
        shuffle_obj.shuffle(row)

    data = {}
    data['values'] = [
          [(str(x.ciphertext()), x.exponent) for x in lst] for lst in S
    ]
    response = requests.post('http://localhost:3000/get-sf-result' , json = data)
    result = response.json()  
    U = [[paillier.EncryptedNumber(public_key , int(ele[0]) ,int(ele[1])) for ele in row]for row in result]

    for row,shuffle_obj in zip(U ,shuffle_obj_list) : 
        shuffle_obj.deshuffle(row)

    res = []
    for j in range(w):
        freq = sum(U[i][j] for i in range(k))
        res.append([all_labels[j], freq])
    return res

def SF(knearest_labels ,all_labels) : 
    freq_list = SF_P1(knearest_labels ,all_labels)
   
    return freq_list


def SDMCL_P1(knearest_labels, all_labels):
    freq_labels = SF(knearest_labels, all_labels)
    
    max_label, _ = SMAX(freq_labels)

    return SDMCL_P2(max_label)
    # send_to_user(r)

def SDMCL_P2(r_q_label):
    return r_q_label

def prepare_knearest_labels(knearest_labels):
    return [item[2] for item in knearest_labels]

def SDMCL(knearest_labels , all_labels) : 
    knearest_labels = prepare_knearest_labels(knearest_labels)
    return SDMCL_P1(knearest_labels, all_labels)



