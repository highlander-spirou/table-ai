from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import Annotated
from random import randint, seed
from os import mkdir, path
import pandas as pd
from io import BytesIO
from pathlib import Path
from jinja2 import Environment
from template import template
import cohere
import duckdb


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = 'vSULf5lQOyNZ9mUaOFjIuMlwmYkbafZikmXtH8c1'
co = cohere.Client(API_KEY)
env = Environment()


@app.get("/")
async def root():
    return {"response": "Hello World"}


def create_hash_str(s):
    seed(1)
    hashed = str(randint(1_000_000, 9_999_999_999))
    return s + '_' + hashed


def save_upload_file(file:UploadFile, upload_dir: str):
    hashed_dir = f'uploads/{create_hash_str(upload_dir)}'
    if not path.exists(hashed_dir):
        mkdir(hashed_dir)
    
    contents = file.file.read()
    file_data = BytesIO(contents)
    if file.content_type == 'text/csv':
        df = pd.read_csv(file_data)
    else:
        df = pd.read_excel(file_data)

    df.to_parquet(hashed_dir + f'/{Path(file.filename).stem}.parquet.gzip', compression='gzip')
    


@app.post("/uploadfiles")
async def create_upload_files(room: Annotated[str, Form()], files: list[UploadFile]):
    for f in files:
        if f.content_type not in ('text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
            raise HTTPException(
                422, f'`{f.filename}` is not a csv or xlsx file')
        else:
            save_upload_file(f, room)
    return {"filenames": [file.filename for file in files]}


def get_table_meta(file_path):
    df = duckdb.read_parquet(file_path)
    return [(i[0], i[1]) for i in df.description]


@app.post('/ask-question')
async def ask_question(question: Annotated[str, Form()]):
    
    tmpl = env.from_string(template)
    schema = get_table_meta('uploads/asd_9168024629/pokemon.parquet.gzip')
    prompt = tmpl.render(table_alias='tbl_1', schema=schema, question=question)
    response = co.generate(prompt, model='command-nightly',max_tokens=544, temperature=0)
    print(response.generations[0].text)
    # aaa = """SELECT Name FROM tbl_1 WHERE "HP" = (SELECT MAX("#") FROM tbl_1) AND "Type 1" = 'Legendary'"""
    # b = aaa.replace('tbl_1', "read_parquet('uploads/asd_9168024629/pokemon.parquet.gzip')")
    # print(b)
    # alias = ('tbl_1', 'uploads/asd_9168024629/pokemon.parquet.gzip')
    # df = duckdb.sql(b)
    # print(df)
    return ""

if __name__ == '__main__':
    uvicorn.run("__main__:app", reload=True)
