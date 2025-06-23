from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import pandas as pd
from io import BytesIO
import logging

from typing import Optional
from execute import run
from utills import get_sample_file_path, get_output_file_path
from constant import EXCEL_FILE_PATH, SAMPLE_INPUT_FILENAME, OUTPUT_FILENAME

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


router = APIRouter()

@router.get("/health")
async def health():
    return "OK"

@router.get('/data/download')
async def data_output_file():
    file = get_output_file_path()
    if not os.path.exists(file):
        LOGGER.error("File not found")
        return HTTPException(status_code=500, detail="File Not Found") 
    return FileResponse(file, filename=OUTPUT_FILENAME, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@router.get('/data/sample-file')
async def data_sample_file():
    file = get_sample_file_path()
    if not os.path.exists(file):
        LOGGER.error("File not found")
        return HTTPException(status_code=500, detail="File Not Found") 
    return FileResponse(file, filename=SAMPLE_INPUT_FILENAME, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')



@router.post("/upload/weather-update")
async def upload(file: Optional[UploadFile] = File(None)):
    try:
        if file:
            if not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
                LOGGER.error("Uploaded file is not an Excel file")
                raise HTTPException(status_code=400, detail="Uploaded file is not an Excel file")
            file_content = await file.read()
            df_dict = pd.read_excel(BytesIO(file_content), sheet_name=None)

            LOGGER.info("Excel file uploaded and read successfully")
        else:
            if not os.path.isfile(EXCEL_FILE_PATH):
                LOGGER.error(f"Excel file not found: {EXCEL_FILE_PATH}")
                raise HTTPException(status_code=404, detail="Excel file not found")
            df_dict = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None)
            LOGGER.info(f"Excel file read from path: {EXCEL_FILE_PATH}")

        return run(df_dict)

    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

