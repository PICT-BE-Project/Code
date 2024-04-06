from pydantic import BaseModel
from phe import paillier


""" Request Model for Secure Multiplication at Cloud 2 """

class QueryRequest(BaseModel) : 
    values : list

