from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
import chromadb
import numpy as np
import pandas as pd
import sqlalchemy
import json
from sklearn.metrics.pairwise import cosine_similarity

app=FastAPI()
# vector db
client=chromadb.PersistentClient("blog_vector_db")
collection=client.get_or_create_collection("blogs", metadata={"hnsw:space": "cosine"})

# Collaborative filtering SQL config
connection_url = f'postgresql+psycopg2://myuser:root@localhost:5432/store_db'
engine = sqlalchemy.create_engine(connection_url)

def padding(array:list):
    array=array+[0]*(5-len(array))
    return np.array(array)

def collaborative(target:np.array,df:pd.DataFrame):
    df['similarity']=df.activity.apply(
            lambda x: cosine_similarity(
                [target], [x])[0][0]
    )
    ids=df.sort_values("similarity",ascending=False)[['activity']][:2].values
    return [i for i in  list(np.concatenate(ids.flatten())) if i not in set(target) and i!=0][:5]



@app.post("/add_product_to_vector")
async def add_product(request:Request):
    data= await request.json()
    for item in data:
        collection.add(
                documents=[item['name']+item['description']],
                ids=[str(item['id'])]
            )
        print("Done $$$$")
    return JSONResponse(
        {
            'data':"ok"
        },status_code=200
    )


# Recommendation by activity
@app.post("/recommend_by_activity")
async def recommend_by_activity(request:Request):
    data=await request.json()
    ids=data['activity']
    embeddings=collection.get(ids=ids,include=['embeddings'])['embeddings']
    # target_embedding=list(np.array(embeddings).mean(0))
    temp=collection.query(
        query_embeddings=[list(np.array(embeddings).mean(0))],
        include=['distances'],
        n_results=20,
        )['ids'][0]
    result=[i for i in temp if i not in set(ids)]
    return JSONResponse({
        'data':result
    },status_code=200)


# Recommendation for a product
@app.post("/recommend_products")
async def recommend_products(request:Request):
    data=await request.json()
    product_id=data['product_id']
    ids=collection.query(
        query_embeddings=collection.get(ids=[product_id],include=['embeddings'])['embeddings'],n_results=6
                    )['ids'][0][1:]
    return JSONResponse(
        {'data':ids},status_code=200
    )

@app.post("/collaborative_recommending")
async def collaborative_recommending(request:Request):
    data=await request.json()
    try:
        activity=data['activity']
        user_id=data["user_id"]
        query=f'''select id , user_id , activity
                from authentication_profile
                where array_length(activity, 1) > 0 and user_id!={user_id};
                '''
        df=pd.read_sql(query,engine)
        df['activity']=df.activity.apply(padding)
        product_ids=collaborative(padding(activity),df)
        product_ids=list(map(str,product_ids))
        return JSONResponse({
            'data':product_ids,'status':True
        },status_code=200)
    except:
        return JSONResponse({
            'status':False
        },status_code=400)


@app.get("/")
async def test():
    return {
        'testing':True
    }
