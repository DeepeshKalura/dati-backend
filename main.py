from tempfile import NamedTemporaryFile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, Dict
import json

from app.logic import convert_pdf_to_images, extract_text_from_img, extract_structured_data


app = FastAPI()
app.mount("/static", StaticFiles(directory="template"), name="static")

@app.get("/",  response_class=FileResponse)
async def read_root():
    return FileResponse('template/index.html')


@app.post("/autmoate/")
async def create_upload_file(file: UploadFile = File(...), data: Optional[str] = None):
    if (data == None):
        data_points = """{
            "invoice_item": "what is the item that charged",
            "Amount": "how much does the invoice item cost in total",
            "Company_name": "company that issued the invoice",
            "invoice_date": "when was the invoice issued",
        }"""

    else :
        data_points = json.dumps(data)
        print(data_points)
    
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    path = f'{file.filename}'

    results = []

    pdf_image_list = convert_pdf_to_images(path)
    pdf_text_list = extract_text_from_img(pdf_image_list)
    
    data = extract_structured_data(pdf_text_list, data_points)
    json_data = json.loads(data)
    if isinstance(json_data, list):
        results.extend(json_data) 
    else:
        results.append(json_data)
        
    
    return results

@app.route("/just_for_fun")
async def just_for_fun(file: UploadFile = File(...)):
    return {"message": "Hello World"}