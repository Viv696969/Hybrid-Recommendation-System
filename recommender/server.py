from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
import chromadb
import numpy as np

app=FastAPI()
# vector db
client=chromadb.PersistentClient("blog_vector_db")
collection=client.get_or_create_collection("blogs", metadata={"hnsw:space": "cosine"})


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


@app.get("/")
async def test():
    return {
        'testing':True
    }
