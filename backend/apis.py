from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dependencies import LoginOptional, LoginRequired, Pagination, PaginationInterface
from typing import Annotated
from db import Client
from services import upload, folder, tables, session
from errors import *
from pydantic import BaseModel
from typing import Optional

api_routes = APIRouter(prefix='/api')
db = session.DB()

@api_routes.get('/')
async def index(client: Annotated[Client, Depends(LoginOptional)]):
    try:
        total_consume = folder.get_dir_size(f'uploads/{client.server_cookie}')
        tables = folder.get_uploads(client.server_cookie, "strip")
    except:
        total_consume = 0
        tables = []
    response = JSONResponse(
        content={"response": tables, "consume": total_consume})
    response.set_cookie('client-id', client.client_cookie, httponly=True,
                        samesite='strict', secure=True, max_age=10*24*60*60)
    return response


@api_routes.post('/uploadfiles')
async def create_upload_files(files: list[UploadFile], client: Annotated[Client, Depends(LoginRequired)]):
    upload.ensure_upload_path(client.server_cookie)
    try:
        valid_files = upload.validate_upload_files(files, client)
        for f in valid_files:
            upload.save_upload_file(f, client.server_cookie)
        response = JSONResponse(content='File upload successfully')
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


@api_routes.get('/table/{tbl_name}')
def index(tbl_name: str, 
          client: Annotated[Client, Depends(LoginRequired)],
          pagination: Annotated[PaginationInterface, Depends(Pagination)]):
    
    file_path = f'uploads/{client.server_cookie}/{tbl_name}.parquet.gzip'
    table = tables.show_table(
        file_path, page=pagination['page'], limit=pagination['limit'])
    return table


class AskQuestionInterface(BaseModel):
    question: str
    table_name: str
    select: Optional[str] = None


@api_routes.post('/ask-question')
def ask_question(req: AskQuestionInterface, client: Annotated[Client, Depends(LoginRequired)]):
    try:
        file_path = f'uploads/{client.server_cookie}/pokemon.parquet.gzip'
        ai_flow = db.get_session(client.client_cookie, req.table_name)

        if ai_flow is None:
            alias = 'tbl_1'
            ai_flow = tables.AIFlow(file_path, alias)
            db.add_obj(client.client_cookie, req.table_name, ai_flow)

        answer = ai_flow.answer_question(req.question, select=req.select)
        return answer
    except FileNotExisted:
        raise HTTPException(400, 'Table collapse, please delete the table and reupload')

    except CohereNotResponse:
        raise HTTPException(400, 'Cohere AI not responding')

    except RunQueryFail as e:
        raise HTTPException(400, {'msg': 'Error executing query', 'query': e.query})