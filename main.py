from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from typing import Annotated


from app.logic import convert_pdf_to_images, extract_text_from_img


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/pdf")
async def extract_content_from_file(file: Annotated[bytes, File()]):
    return FileResponse(file, media_type="application/pdf")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    path = f'{file.filename}'
    # at least i have the file here
    pdf_image_list = convert_pdf_to_images(path)
    pdf_text_list = extract_text_from_img(pdf_image_list)

    print(path)
   


