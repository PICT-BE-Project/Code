from phe import paillier
import pickle
from server2.schemas import QueryRequest

""" GET PUBLIC PRIVATE KEYS """
def get_public_private_key_pair() :
    PUBLIC_KEY : paillier.PaillierPublicKey =''
    PRIVATE_KEY : paillier.PaillierPrivateKey =''
    with open('./secrets512.pkl' ,mode='rb') as f : 
        PUBLIC_KEY = pickle.load(f)
        PRIVATE_KEY = pickle.load(f)
    return PUBLIC_KEY,PRIVATE_KEY

public_key , private_key = get_public_private_key_pair()


""" DESERIALIZE INPUT RECEIVED FROM CLOUD1  """
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


""" SECURE MULTIPLICATION """
def perform_secure_multiplication(ad , bd) : 
    ha = private_key.decrypt(ad)
    hb = private_key.decrypt(bd)

    h = (ha * hb) % public_key.n
    hd = public_key.encrypt(h)
    return hd

def SMIN_C2(a, b):
    distance_1 = private_key.decrypt(a[1])
    distance_2 = private_key.decrypt(b[1])
    
    if distance_1 <= distance_2 : 
        return a 
    else : 
        return b

""" SECURE ELIMINATION """
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


""" SECURE MINIMUM """
def SMIN_C2(a, b):
    distance_1 = private_key.decrypt(a[1])
    distance_2 = private_key.decrypt(b[1])
    
    if distance_1 <= distance_2 : 
        return a 
    else : 
        return b
    
""" SECURE MAXIMUM """
def SMAX_C2(a, b):
    da = private_key.decrypt(a[1])
    db = private_key.decrypt(b[1])

    if da < db:
        return b
    else:
        return a
    
""" SECURE FREQUENCY """
def SF_C2(S):
    k = len(S)
    w = len(S[0])

    U = [[0 for _ in range(w)] for _ in range(k)]
    for i in range(k):
        for j in range(w):
            if private_key.decrypt(S[i][j]) == 0:
                U[i][j] = public_key.encrypt(1)
            else:
                U[i][j] = public_key.encrypt(0)

    return U

