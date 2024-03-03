import os
import google.generativeai as genai
from pathlib import Path
import pypdfium2 as pdfium
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


genai.configure(api_key = os.getenv('Gemini_Key'))
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def convert_pdf_to_images(file_path: str, scale: float = 300/72):

    pdf_file = pdfium.PdfDocument(file_path)

    page_indices = [i for i in range(len(pdf_file))]

    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices=page_indices,
        scale=scale,
    )

    # final_images = []

    for i, image in zip(page_indices, renderer):
        # final_images.append(image)
        image.save(f"invoice_{i}.jpeg", format='jpeg', optimize=True)
    # return final_images


def extract_structured_data(data_points):
    
    # content = input_image_setup(image_list)
    content = [
       {
          "mime_type": "image/jpeg",
          "data" : Path(f"invoice_0.jpeg").read_bytes()
       },
    ]

    prompt = [
       "You are an expert admin people who will extract core information from documents",
       {
          "mime_type": "image/jpeg",
          "data" : Path(f"invoice_0.jpeg").read_bytes()
       },
       "Above is the content; Image please try to extract all data points from the content above and export in a JSON array format: ",
        data_points,
        "Now please extract details from the content  and export in a JSON array format, return ONLY the JSON array:"
    ]
    
    # template = f"""
    # You are an expert admin people who will extract core information from documents

    # {content}

    # Above is the content; Binary Image please try to extract all data points from the content above
    # and export in a JSON array format:
    # {data_points}

    # Now please extract details from the content  and export in a JSON array format,
    # return ONLY the JSON array:
    # """

    # prompt = PromptTemplate(
    #     input_variables=["content", "data_points"],
    #     template=template,
    # )

    # chain = LLMChain(llm=llm, prompt=prompt)
    

    results = model.generate_content(prompt)
    return (results.text)
    # return results


# def input_image_setup(image_list):
#   image_parts = []
#   for image_data in image_list:
#     # print(type(image_data))
#     data = {
#         "mine_type": "image.jpeg",
#         "data" : image_data.tobytes()
#     }
#     image_parts.append(data)
#   return image_parts

# res = convert_pdf_to_images(file_path="invoice.pdf")

data_points = """{
            "invoice_item": "what is the item that charged",
            "Amount": "how much does the invoice item cost in total",
            "Company_name": "company that issued the invoice",
            "invoice_date": "when was the invoice issued",
        }"""


# game = extract_structured_data(data_points)
# print(game)

#print(image_parts) 