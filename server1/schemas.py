from pydantic import BaseModel

class QueryRequest(BaseModel) : 
    values : list

