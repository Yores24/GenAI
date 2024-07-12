from dotenv import load_dotenv

load_dotenv() # load all environment variables from .env file

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("Google_API_key"))

# Function to load Gemini Pro-Vision

model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
      respone=model.generate_content([input,image[0],prompt])
      return respone.text

def input_img(uploaded_file):
    if uploaded_file is not None:
            bytes_d=uploaded_file.getvalue()
            
            image_parts=[
                  {
                        "mime_type":uploaded_file.type,# get the mime type of the uploaded file
                        "data":bytes_d
                  }
            ]
            return image_parts
    else:
          raise FileNotFoundError("No file found") 


# Initialize the streamlit app

st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("Gemini Application")

input=st.text_input("Input Prompt: ",key="input")
uploaded_file= st.file_uploader("Choose an image of invoice ...", type=['jpg','jpeg','png'])
image=""

if uploaded_file is not None:
      image=Image.open(uploaded_file)
      st.image(image,caption="Uploaded Image, ",use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload an image as invoice and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
      image_data=input_img(uploaded_file)
      response=get_gemini_response(input_prompt,image_data,input)
      st.subheader("The response is ")
      st.write(response)