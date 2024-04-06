from fastapi import FastAPI
from server2.utils import public_key,private_key
from server2.schemas import QueryRequest
from server2.utils import (
    deserialize_input,
    perform_secure_multiplication,
    SELIM_C2 ,
    SMIN_C2 ,
    SMAX_C2 ,
    SF_C2
)
import timeit

app = FastAPI()


""" FUNCTION TO HANDLE SM """
@app.post('/get-sm-result')
async def SM_P2(request_data : QueryRequest) : 
    data =  deserialize_input(request_data)
    result = perform_secure_multiplication(data[0] , data[1])
    return result.ciphertext() , result.exponent


""" FUNCTION TO HANDLE SMIN """
@app.post('/get-smin-result')
async def SMIN_P2(request_data : QueryRequest) : 
    data =  deserialize_input(request_data)
    result = SMIN_C2(data[0] , data[1])
    return [(x.ciphertext() , x.exponent) for x in result]

""" FUNCTION TO HANDLE SELIM """
@app.post('/get-selim-result')
async def SELIM_P2(request_data : QueryRequest) :
    data =  deserialize_input(request_data)
    E_zero = data.pop(-1)
    E_maxVal = data.pop(-1)
    result = SELIM_C2(data,E_maxVal ,E_zero)
    return [(x.ciphertext() , x.exponent) for x in result]


""" FUNCTION TO HANDLE SMAX """
@app.post('/get-smax-result')
async def SMAX_P2(request_data : QueryRequest) :
    data =  deserialize_input(request_data)
    result = SMAX_C2(data[0] , data[1])
    return [(x.ciphertext() , x.exponent) for x in result]


""" FUNCTION TO HANDLE SF """
@app.post('/get-sf-result')
async def SF_P2(request_data : QueryRequest) :
    data =  deserialize_input(request_data)
    result = SF_C2(data)
    return [[(x.ciphertext() , x.exponent) for x in row ]for row in result]
