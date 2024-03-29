from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.ocr import convert_pdf_to_images, extract_text_from_img, extract_structured_data
from app.schema import Item
import app.multimodel as mm
from app.helper import standardize_json



app = FastAPI()
app.mount("/static", StaticFiles(directory="template"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",  response_class=FileResponse)
async def read_root():
    return FileResponse('template/index.html')


@app.post("/autmoate/multimodel")
async def multimodel_upload_file(item: str = Body(None) , file: UploadFile = File(...), ):
    if(item == None):
        item = """{
            "invoice_item": "what is the item that charged",
            "Amount": "how much does the invoice item cost in total",
            "Company_name": "company that issued the invoice",
            "invoice_date": "when was the invoice issued",
        }"""

    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    path = f'{file.filename}'

    results = []

    mm.convert_pdf_to_images(file_path=path)
    extract_data = mm.extract_structured_data(item)
    
    print(extract_data)
    try:
        json_data = standardize_json(extract_data)
    except Exception as e:
        return {"error": str(e)}
    
    if isinstance(json_data, list):
        results.extend(json_data) 
    else:
        results.append(json_data)

    return results

@app.post("/autmoate/ocr/")
async def ocr_upload_file(data: Item, file: UploadFile = File(...), ):
    
    if (data == None):
        data = """{
            "invoice_item": "what is the item that charged",
            "Amount": "how much does the invoice item cost in total",
            "Company_name": "company that issued the invoice",
            "invoice_date": "when was the invoice issued",
        }"""
    
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    path = f'{file.filename}'

    results = []

    pdf_image_list = convert_pdf_to_images(path)
    pdf_text_list = extract_text_from_img(pdf_image_list)
    
    extract_data = extract_structured_data(pdf_text_list, data)
    json_data = standardize_json(extract_data)
    if isinstance(json_data, list):
        results.extend(json_data) 
    else:
        results.append(json_data)
        
    
    return results

    
