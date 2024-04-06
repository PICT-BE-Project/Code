from phe import paillier
from pydantic import BaseModel
import random



public_key , private_key = paillier.generate_paillier_keypair(n_length=1024)


def deserialize_input(received_dict ) : 
    enc_nums_rec = []

    for x in received_dict['values']:
        if isinstance(x[0] ,list) :
            tmp = []
            for ele in x : 
                tmp.append(paillier.EncryptedNumber(public_key, int(ele[0]), int(ele[1]))) 
            enc_nums_rec.append(tmp)   
        else : 
           enc_nums_rec.append(paillier.EncryptedNumber(public_key, int(x[0]), int(x[1])))
    return enc_nums_rec


def perform_secure_multiplication(ad , bd) : 
    ha = private_key.decrypt(ad)
    hb = private_key.decrypt(bd)

    h = (ha * hb) % public_key.n
    hd = public_key.encrypt(h)
    return hd

def randomize(a ,ra) :
  if isinstance(a ,list) :
    ans = []
    for i in range(len(a)) :
      ans.append(a[i]+ra)
    return ans
  else :
    ans = a + ra
    return ans

def SM_P2(request_data) : 
    data =  deserialize_input(request_data)
    result = perform_secure_multiplication(data[0] , data[1])
    return result.ciphertext() , result.exponent


if __name__ == '__main__':
    ra = random.getrandbits(25)
    rb = random.getrandbits(25)
    a = public_key.encrypt(10)
    b = public_key.encrypt(20)
    enc_a = randomize(a, ra)
    enc_b = randomize(b,rb)

    data = {}
    data['values'] = [ (str(x.ciphertext()), x.exponent) for x in [enc_a,enc_b] ]
    SM_P2(data)