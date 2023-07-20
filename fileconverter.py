import streamlit as st
from PIL import Image
from pdf2docx import Converter
import base64
import os
from pptx import Presentation

def convert_image(file, format):
    image = Image.open(file)
    if image.mode in ("RGBA", "P"): 
        image = image.convert("RGB")
    new_filename = file.name.split(".")[0] + "." + format
    image.save(new_filename, format)
    return new_filename

def convert_pdf_to_word(file):
    pdf_file = file.name
    word_file = pdf_file.split(".")[0] + ".docx"
    cv = Converter(pdf_file)
    cv.convert(word_file, start=0, end=None)
    cv.close()
    return word_file

def convert_jpg_to_pptx(file):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.add_picture(file, 0, 0)
    new_filename = file.name.split(".")[0] + ".pptx"
    prs.save(new_filename)
    return new_filename

def create_download_link(file):
    with open(file, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/{file.split(".")[-1]};base64,{b64}" download="{os.path.basename(file)}">Download file</a>'
        return href

st.title('JPG/PNG/PDF/JPEG/DOCX/PPTX Converter(파일 확장자 변환기)')

file = st.file_uploader("Upload a file", type=['jpg', 'png', 'pdf'])

if file is not None:
    file_type = st.selectbox("Select output format", ['jpg', 'png', 'pdf', 'docx', 'pptx'])

    if st.button('Convert'):
        if file_type in ['jpg', 'png']:
            if file.type in ['image/jpeg', 'image/png']:
                output_file = convert_image(file, file_type)
                st.success(f'File converted successfully.')
                st.markdown(create_download_link(output_file), unsafe_allow_html=True)
            else:
                st.error('Please upload a jpg or png file to convert to another image format.')
        elif file_type == 'pdf':
            if file.type in ['image/jpeg', 'image/png']:
                output_file = convert_image(file, file_type)
                st.success(f'File converted successfully.')
                st.markdown(create_download_link(output_file), unsafe_allow_html=True)
            else:
                st.error('Please upload a jpg or png file to convert to pdf.')
        elif file_type == 'docx':
            if file.type == 'application/pdf':
                output_file = convert_pdf_to_word(file)
                st.success(f'File converted successfully.')
                st.markdown(create_download_link(output_file), unsafe_allow_html=True)
            else:
                st.error('Please upload a pdf file to convert to docx.')
        elif file_type == 'pptx':
            if file.type in ['image/jpeg', 'image/png']:
                output_file = convert_jpg_to_pptx(file)
                st.success(f'File converted successfully.')
                st.markdown(create_download_link(output_file), unsafe_allow_html=True)
            else:
                st.error('Please upload a jpg or png file to convert to pptx.')
