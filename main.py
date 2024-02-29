from tempfile import NamedTemporaryFile
from fastapi import FastAPI, UploadFile, File
import json

from app.logic import convert_pdf_to_images, extract_text_from_img, extract_structured_data


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    default_data_points = """{
        "invoice_item": "what is the item that charged",
        "Amount": "how much does the invoice item cost in total",
        "Company_name": "company that issued the invoice",
        "invoice_date": "when was the invoice issued",
    }"""

    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    path = f'{file.filename}'

    results = []
    with NamedTemporaryFile(dir='.', suffix='.csv') as f:

        pdf_image_list = convert_pdf_to_images(path)
        pdf_text_list = extract_text_from_img(pdf_image_list)
        
        data = extract_structured_data(pdf_text_list, default_data_points)
        json_data = json.loads(data)
        if isinstance(json_data, list):
            results.extend(json_data)  # Use extend() for lists
        else:
            results.append(json_data)
        
    
    return results


   


