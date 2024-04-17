from typing import Union
from fastapi import FastAPI, Query
import boto3
from boto3.dynamodb.conditions import Key, Attr
from KeywordLearning import keyword_learning
from PreferenceInference import preference_inference
from fastapi_utils.tasks import repeat_every
from time import time
import httpx
import asyncio

app = FastAPI()
URL = "https://0iluhpf98l.execute-api.ap-northeast-2.amazonaws.com/Prod/"
# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# 테이블 접속
table = dynamodb.Table('keyword_blog_contents') # 스크랩한 블로그 글

@app.get("/")
def home():
    return {"result": "items"}

@app.get("/similarities")
def read_root():
  # keyword가 같은 쿼리와 같은 요소를 전부 가져온다.
  response = table.query(
      KeyConditionExpression=Key('keyword').eq('광주 여행')
  )
  items = response['Items']
  print(items)
  print(len(items))
  return {"result": items}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/keyword/query")
def get_query():
    return {}

@app.get("/model/keywords")
def recommend_region(keywords: list[str] = Query()):
    model = preference_inference.load_model()
    recommended_region = preference_inference.get_recommended_region(model, keywords)
    return {"region" : recommended_region}

@app.post("/model/params")
def train_model():
    model = keyword_learning.train_model()
    keyword_learning.save_model_params(model)
    return {"result" : "complete"}

@app.on_event("startup")
@repeat_every(seconds=60)  # 60 hour
async def print_task() -> None:
    print("수행 시작!")
    async with httpx.AsyncClient() as client:
        params = {'keyword': '포항 여행','count':"5"}
        response = await client.post(URL, params)
        print(response)
    if(response.status_code == 200):
        return {"result" : "수행 완료"}
    else:
        return {"result" : "수행 실패"}

