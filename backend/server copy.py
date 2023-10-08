from fastapi import FastAPI, UploadFile, HTTPException, Request, Depends, Cookie
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
import uvicorn
from typing import Annotated, Any
from random import randint, seed
from os import mkdir, path, listdir, remove
import pandas as pd
from io import BytesIO
from pathlib import Path
from jinja2 import Environment
from template import template
from cohere import AsyncClient
import duckdb
import re
from uuid import uuid4
from pathlib import Path
from typing import Optional, Annotated
from db import ClientUtils, Client, engine
from errors import *
from sqlalchemy.orm import Session
from pydantic import BaseModel, ValidationError
from time import sleep

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = 'vSULf5lQOyNZ9mUaOFjIuMlwmYkbafZikmXtH8c1'
env = Environment()
prompt_tmpl = env.from_string(template)
templates = Jinja2Templates('./static/dist')

# def GetSession():
#     session = Session(engine)
#     try:
#         yield session
#     finally:
#         session.close()


def split_parquet(s):
    return s.split('.parquet.gzip')[0]


# def UploadCheckingFlow(files: list[UploadFile], client: Client) -> list[UploadFile]:
#     """
#     Validate upload files, return the files or raise Exceptions

#     @ Exceptions subclass:
#     - DuplicateUploadFile
#     - ClientMaxUssage
#     - FileExceedUssage
#     - FileExtensionInvalid

#     """
#     # check duplicated files (on upload)
#     file_set = {Path(i.filename).stem for i in files}
#     if len(file_set) != len(files):
#         raise DuplicateUploadFile

#     # check existed files (no-overwrite)
#     files_in_dir = listdir(f'./uploads/{client.server_cookie}')

#     if len(file_set.intersection({split_parquet(f) for f in files_in_dir})) > 0:
#         raise UploadedFileExisted

#     # check total file size
#     total_size = sum([i.size for i in files])
#     if total_size - client.total_consume < 0:
#         raise ClientMaxUssage

#     # check single file size
#     valid_size = all([i.size <= 1 * (10**8) for i in files])
#     if valid_size is False:
#         raise FileExceedUssage

#     # Check file extension
#     accepted_content_type = (
#         'text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     valid_ext = all([i.content_type in accepted_content_type for i in files])
#     if valid_ext is False:
#         raise FileExtensionInvalid

#     return files


def create_hash_str(s):
    seed(1)
    hashed = str(randint(1_000_000, 9_999_999_999))
    return s + '_' + hashed


def ensure_upload_path(path_name):
    destination = f'uploads/{path_name}'
    if not path.exists(destination):
        mkdir(destination)


def save_upload_file(file: UploadFile, hashed_dir: str):
    destination = f'uploads/{hashed_dir}'
    try:
        contents = file.file.read()
        file_data = BytesIO(contents)
        if file.content_type == 'text/csv':
            df = pd.read_csv(file_data)
        else:
            df = pd.read_excel(file_data)
        df.to_parquet(
            destination + f'/{Path(file.filename).stem}.parquet.gzip', compression='gzip')
    except Exception as e:
        if path.exists(destination + f'/{Path(file.filename).stem}.parquet.gzip'):
            remove(destination + f'/{Path(file.filename).stem}.parquet.gzip')
        raise ParquetConversionError


def analyze_df(df):
    col_type = df.dtypes.to_dict()
    null_counts = df.isnull().sum().to_dict()

    a = {}
    for index in col_type.keys():
        a[index] = (str(col_type[index]), null_counts[index])
    return a


# def GetClientCookie(client_id: Annotated[str | None, Cookie(alias='client-id')] = None):
#     return client_id


# def auth_flow(client_id: str, client_utils: ClientUtils):
#     """
#     Return `Client` or exceptions

#     - `HeaderMissing`
#     - `ClientNotFound`
#     - `ClientTimeOut`
#     """
#     client_in_db = client_utils.find_client(client_id)
#     client_utils.verify_client(client_in_db)
#     return client_in_db


# def LoginOptional(client_id: Annotated[str | None, Depends(GetClientCookie)],
#                   session: Annotated[Session, Depends(GetSession)]):
#     client_utils = ClientUtils(session)
#     try:
#         if client_id is None:
#             raise HeaderMissing
#         client = auth_flow(client_id, client_utils)
#         return client
#     except ClientTimeOut as e:
#         client_in_db = e.client_in_db
#         new_client_id = str(uuid4())
#         client_utils.update_refresh_token(client_in_db, new_client_id)
#         return client_in_db

#     except (ClientNotFound, HeaderMissing) as e:
#         new_client_id = str(uuid4())
#         new_client = client_utils.create_client(new_client_id)
#         return new_client


# def LoginRequired(client_id: Annotated[str | None, Depends(GetClientCookie)],
#                   session: Annotated[Session, Depends(GetSession)]):
#     client_utils = ClientUtils(session)
#     try:
#         client = auth_flow(client_id, client_utils)
#         return client

#     except ClientTimeOut as e:
#         client_in_db = e.client_in_db
#         new_client_id = str(uuid4())
#         client_utils.update_refresh_token(client_in_db, new_client_id)
#         return client_in_db

#     except (HeaderMissing, ClientNotFound) as e:
#         raise HTTPException(400, 'Client ID invalid')


# async def Pagination(page: int = 0, limit: int = 5):
#     return {"page": page, "limit": limit}



def get_table_list(client: Client):
    return [split_parquet(i) for i in listdir(f'uploads/{client.server_cookie}')]


# def get_table_rows(file_path):


@app.post("/api")
async def root(client: Annotated[Client, Depends(LoginOptional)]):
    try:
        tables = get_table_list(client)
    except:
        tables = []
    response = JSONResponse(content={"response": tables})
    response.set_cookie('client-id', client.client_cookie, httponly=True,
                        samesite='strict', secure=True, max_age=10*24*60*60)
    return response


@app.get('/api/table/{tbl_name}')
def get_table(tbl_name: str, client: Annotated[Client, Depends(LoginRequired)], pagination: Annotated[dict, Depends(Pagination)]):
    file_path = f'uploads/{client.server_cookie}/{tbl_name}.parquet.gzip'
    print(file_path)
    return ""
    # try:
    #     file_path = f'uploads/{client.server_cookie}/{tbl_name}.parquet.gzip'
    #     with duckdb.connect(':default:') as con:
    #         tbl = duckdb.read_parquet(file_path)
    #     tbl_rows = tbl.query(virtual_table_name='tbl', sql_query='SELECT * FROM tbl LIMIT ')
    # except Exception:
    #     pass


@app.post('/test_pandas_reading')
async def test_pandas_reading(files: list[UploadFile]):
    dfs = []
    try:
        for file in files:
            contents = file.file.read()
            file_data = BytesIO(contents)
            if file.content_type == 'text/csv':
                df = pd.read_csv(file_data)
            else:
                df = pd.read_excel(file_data)

            dfs.append({'name': file.filename, 'info': analyze_df(df)})
        return dfs
    except Exception as e:
        raise HTTPException(400, {'origin': file.filename, 'error': str(e)})


@app.post("/uploadfiles")
async def create_upload_files(files: list[UploadFile], client: Annotated[Client, Depends(LoginOptional)]):
    ensure_upload_path(client.server_cookie)
    try:
        valid_files = UploadCheckingFlow(files, client)
        for f in valid_files:
            save_upload_file(f, client.server_cookie)
        response = JSONResponse(content='File upload successfully')
        response.set_cookie(
            key="client-id", value=client.client_cookie, max_age=20*24*60*60)
        return response

    except (DuplicateUploadFile, UploadedFileExisted):
        raise HTTPException(400, 'Duplicate uploaded file name')
    except ClientMaxUssage:
        raise HTTPException(400, 'Exceed 500MB of total upload files')
    except FileExceedUssage:
        raise HTTPException(400, 'Uploaded file exceed 100MB')
    except FileExtensionInvalid:
        raise HTTPException(400, 'File extension not .csv or .xlsx')
    except ParquetConversionError:
        raise HTTPException(400, 'Cannot convert file to parquet')


def get_table_meta(df):
    # df = duckdb.read_parquet(file_path)
    return [(i[0], i[1]) for i in df.description]


class AskQuestionRequestInterface(BaseModel):
    question: str
    table_name: str


class LongTask:
    def __init__(self, file_path, question) -> None:
        self.file_path = file_path
        self.question = question
        self.alias = 'tbl_1'

        # Placeholder attributes
        self.df = None
        self.schema = None
        self.prompt = None
        self.sql_query = None
        self.full_explain = None
        self.result = None

    def get_df(self):
        try:
            print(self.file_path)
            self.df = duckdb.read_parquet(self.file_path)
        except Exception:
            raise FileNotExisted

    def get_schema(self):
        self.schema = get_table_meta(self.df)

    def create_prompt(self):
        self.prompt = prompt_tmpl.render(
            table_alias=self.alias, schema=self.schema, question=self.question)

    async def get_query_suggestion(self):
        try:
            async with AsyncClient(API_KEY) as co:
                response = await co.generate(self.prompt, model='command-nightly',
                                             max_tokens=544, temperature=0)

            sql_query = re.findall(
                r'```([^```]*)```', response.generations[0].text)[0]

            if 'sql' in sql_query:
                sql_query = sql_query.split('\n')[1]

            self.sql_query = sql_query
            self.full_explain = response.generations[0].text
        except Exception:
            raise CohereNotResponse

    def run_query(self):
        try:
            result = self.df.query(self.alias, self.sql_query)
            self.result = result.fetchall()
        except Exception:
            print('raising')
            raise RunQueryFail(query=self.sql_query)

    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.get_df()
        self.get_schema()
        self.create_prompt()
        await self.get_query_suggestion()
        self.run_query()
        return self.result


@app.post('/ask-question')
async def ask_question(client: Annotated[Client, Depends(LoginRequired)],
                       args: AskQuestionRequestInterface, ai_explain: Optional[bool] = False):
    try:
        file_name = f'uploads/{client.server_cookie}/{args.table_name}.parquet.gzip'
        task = LongTask(file_name, args.question)
        await task()
        content = {'result': task.result}
        if ai_explain:
            content['ai_explain'] = task.full_explain
        return JSONResponse(content)

    except FileNotExisted:
        raise HTTPException(
            400, 'Error when finding file')
    except CohereNotResponse:
        raise HTTPException(
            400, 'Cohere server not response, please try again')
    except RunQueryFail as e:
        print('catching')
        raise HTTPException(
            400, {'msg': 'Error when executing query', 'query': e.query})
    except Exception:
        raise HTTPException(404, 'Invalid response')


app.mount("/haha", StaticFiles(directory="static/dist", html=True), name="index")

@app.route("/{full_path}")
async def catch_all(request: Request, full_path: str):
    print("full_path: "+full_path)
    return ""


if __name__ == '__main__':
    uvicorn.run("__main__:app", reload=True)
