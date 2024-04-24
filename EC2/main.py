from typing import Union
from fastapi import FastAPI, Query
import boto3
from boto3.dynamodb.conditions import Key, Attr
from KeywordLearning import keyword_learning
from PreferenceInference import preference_inference
import random
from fastapi_utils.tasks import repeat_every
from time import time
import pprint
import requests
import random
app = FastAPI()
URL = "https://0iluhpf98l.execute-api.ap-northeast-2.amazonaws.com/Prod/"
# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# 테이블 접속
keyword_blog_contents_table = dynamodb.Table('keyword_blog_contents') # 스크랩한 블로그 글
regionAndKeywords_table = dynamodb.Table('regionAndKeywords') # 스크랩한 블로그 글

@app.get("/")
def home():
    return {"result": "items"}

@app.get("/similarities")
def read_root():
  # keyword가 같은 쿼리와 같은 요소를 전부 가져온다.
  response = keyword_blog_contents_table.query(
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
    response = regionAndKeywords_table.scan(AttributesToGet=['keyword'])
    all_records = response['Items']

    keywords_set = set()
    while len(keywords_set) < 12:
        random_record = random.choice(all_records)
        keywords_set.add(random_record['keyword'])

    return keywords_set

model = preference_inference.load_model()

@app.get("/model/keywords")
def recommend_region(keywords: list[str] = Query()):
    recommended_region = preference_inference.get_recommended_region(model, keywords)
    return {"region" : recommended_region}

@app.post("/model/params")
def train_model():
    model = keyword_learning.train_model()
    keyword_learning.save_model_params(model)
    return {"result" : "complete"}


async def perform_task(keyword: str, count: int):
    url = "https://0iluhpf98l.execute-api.ap-northeast-2.amazonaws.com/Prod/"
    query_string = f"?keyword={keyword}&count={count}"
    print(url+query_string)
    r_post = requests.post(url+query_string)
    pprint.pprint(r_post.json())


@app.on_event("startup")
@repeat_every(seconds=60*60*24)  # 1일 간격으로 작업 진행
async def lambda_task() -> None:
    regionList = ["강릉", "동해", "삼척", "속초", "원주", "춘천", "태백", "고성"]
    for s in regionList:
        print(s," 여행 블로그 탐색 요청")
        await perform_task(s+" 여행", 5)

