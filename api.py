import json
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pyarrow.parquet as pq

from scratch_pad import build_my_stuff

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# to start: uvicorn api:app --reload

@app.post("/api/build")
async def build(info: Request):
    if await info.body():
        req_info = await info.json()
        logging.info(req_info)
        ret_val = build_my_stuff(req_info['mod_ids'])
        response = {
            "status": "SUCCESS",
            "data": ret_val
        }
    else:
        response = {"status": "SUCCESS"}
    logging.info(response)
    return response


@app.get("/api/mods")
def mods(info: Request):
    mod_list_df = pq.read_table('mappings/mod_list.parquet.gzip').to_pandas()
    response = {
        "status": "SUCCESS",
        "data": json.loads(mod_list_df.to_json(orient="records"))
    }
    logging.info(response)
    return response


@app.get("/api/mods/attributes")
async def mods_attributes(info: Request):
    mod_attribute_list = pq.read_table('mappings/mod_attribute_list.parquet.gzip').to_pandas()
    response = {
        "status": "SUCCESS",
        "data": json.loads(mod_attribute_list.to_json(orient="records"))
    }
    logging.info(response)
    return response
