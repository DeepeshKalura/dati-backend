import os
from pathlib import Path
import google.generativeai as genai


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
  }
]

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

model = genai.GenerativeModel(model_name = "gemini-pro-vision", generation_config = generation_config, safety_settings = safety_settings)

def input_image_setup(file_loc):
    if not (img := Path(file_loc)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": Path(file_loc).read_bytes()
            }
        ]
    return image_parts

def extract_text_from_img_gemini(list_dict_final_images:list, data_poinsts: str):
    image_list = [list(data.values())[0] for data in list_dict_final_images]
    response = []
    for index, image_bytes in enumerate(image_list):
        image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_bytes
            }
        ]

        res = generate_gemini_response(input_prompt, image_parts, data_poinsts)

        response.append(res)
        print(response)
        return response
        
def generate_gemini_response(input_prompt, image_parts, data_points):
    response = model.predict(input_prompt, image_parts, data_points)
    return response.txt