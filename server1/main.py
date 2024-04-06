from fastapi import FastAPI
from server1.schemas import QueryRequest 
from server1.utils import (
    deserialize_input ,get_model_data ,SSED ,
    prepare_distance_label ,
    private_key ,
    KMIN_C1 ,
    SDMCL
 )
import time
import concurrent


app = FastAPI()

@app.post('/execute-KNN')
async def start(request_data : QueryRequest ,model_name : str ,num_rec : str | None ) : 

    print("Received model = " , model_name )
    model_query = deserialize_input(request_data)
    model = get_model_data(model_name)
    if num_rec == "all" : num_rec = len(model.data)
    else :  num_rec = int(num_rec)

    records = model.data[:num_rec]
    queries = [model_query for _ in range(len(records))]
    # print(len(records))
    # added for test purposes to ensure same amount of model data
    start = time.time() 
    print("Starting SSED ")
    # with concurrent.futures.ProcessPoolExecutor() as executor  :
    #     result =  executor.map(SSED ,records ,queries)
    result = SSED(records , model_query)  
    end = time.time()
    print(f'Finised SSED in {end-start} second(s)')
    # dist = []
    # for r in result : 
    #     dist.append(r[0])
    # distance_label = prepare_distance_label(dist ,model.data)
    distance_label = prepare_distance_label(result ,model.data)
    k = 11
    print("Starting KMIN")
    start = time.time()
    knearest_labels = KMIN_C1(distance_label, k)
    end = time.time()
    print(f"Finished KMIN in {end-start} second(s)")
    print("KMIN :")
    for labels in knearest_labels : 
        print([private_key.decrypt(ele) for ele in labels])
    start = time.time()
    ans_label = SDMCL(knearest_labels ,model.all_labels)
    print("Final label = " , private_key.decrypt(ans_label))
    end = time.time()   
    print(f"Finished SDMCL in {end-start} second(s)")
    # print(f"Finished in {end-start} seconds")
    return ans_label
    return 1


