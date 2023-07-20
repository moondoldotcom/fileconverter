import streamlit as st
from PIL import Image
import base64
import os
from pdf2image import convert_from_path
from docx2pdf import convert

def convert_image(file, format):
    image = Image.open(file)
    if image.mode in ("RGBA", "P"): 
        image = image.convert("RGB")
    new_filename = file.name.split(".")[0] + "." + format
    image.save(new_filename, format)
    return new_filename

def convert_pdf_to_images(file, format):
    images = convert_from_path(file.name)
    output_files = []
    for i, image in enumerate(images):
        if image.mode in ("RGBA", "P"): 
            image = image.convert("RGB")
        output_file = f"{file.name.split('.')[0]}_{i+1}.{format}"
        image.save(output_file, format)
        output_files.append(output_file)
    return output_files

def convert_word_to_pdf(file):
    output_file = file.name.split(".")[0] + ".pdf"
    convert(file.name, output_file)
    return output_file

def create_download_link(file):
    with open(file, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/{file.split(".")[-1]};base64,{b64}" download="{os.path.basename(file)}">Download file</a>'
        return href

st.title('Image to Image / PDF to Image / Word to PDF Converter(파일 변환기)')

file = st.file_uploader("Upload a file", type=['jpg', 'png', 'pdf', 'docx'])

if file is not None:
    file_type = st.selectbox("Select output format", ['jpg', 'png', 'pdf'])

    if st.button('Convert'):
        if file_type in ['jpg', 'png']:
            if file.type in ['image/jpeg', 'image/png']:
                output_file = convert_image(file, file_type)
                st.success(f'File converted successfully.')
                st.markdown(create_download_link(output_file), unsafe_allow_html=True)
            elif file.type == 'application/pdf':
                output_files = convert_pdf_to_images(file, file_type)
                for output_file in output_files:
                    st.success(f'File converted successfully.')
                    st.markdown(create_download_link(output_file), unsafe_allow_html=True)
            else:
                st.error('Please upload a jpg, png, or pdf file to convert to another image format.')
        elif file_type == 'pdf':
            if file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                output_file = convert_word_to_pdf(file)
                st.success(f'File converted successfully.')
                st.markdown(create_download_link(output_file), unsafe_allow_html=True)
            else:
                st.error('Please upload a docx file to convert to pdf.')
