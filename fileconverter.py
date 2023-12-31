import streamlit as st
from PIL import Image
import base64
import os
from pdf2image import convert_from_path
from tempfile import NamedTemporaryFile
from docx import Document
import asyncio
from pyppeteer import launch

async def html_to_pdf(input_filename, output_filename):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('file://' + input_filename)
    await page.pdf({'path': output_filename, 'format': 'A4'})
    await browser.close()

def convert_word_to_html(file):
    temp_html_file = NamedTemporaryFile(suffix=".html", delete=False).name
    document = Document(file)

    # Save the Word document's text to a temporary HTML file
    with open(temp_html_file, 'w') as f:
        for paragraph in document.paragraphs:
            f.write('<p>' + paragraph.text + '</p>\n')

    return temp_html_file

def convert_word_to_pdf(file):
    temp_html_file = convert_word_to_html(file)
    output_file = NamedTemporaryFile(suffix=".pdf", delete=False).name

    # Convert the HTML to PDF
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(html_to_pdf(temp_html_file, output_file))
    finally:
        loop.close()

    return output_file

def convert_image(file, format):
    image = Image.open(file)
    if image.mode in ("RGBA", "P"): 
        image = image.convert("RGB")
    new_filename = file.name.split(".")[0] + "." + format
    image.save(new_filename, format)
    return new_filename

def convert_pdf_to_images(file, format):
    with open(file.name, "wb") as f:
        f.write(file.read())

    images = convert_from_path(file.name)
    output_files = []
    for i, image in enumerate(images):
        if image.mode in ("RGBA", "P"): 
            image = image.convert("RGB")
        output_file = f"{file.name.split('.')[0]}_{i+1}.{format}"
        image.save(output_file, format)
        output_files.append(output_file)
    
    os.remove(file.name)  # Remove the temporary file
    
    return output_files

def create_download_link(file):
    with open(file, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/{file.split(".")[-1]};base64,{b64}" download="{os.path.basename(file)}">Download file</a>'
        return href

def main():
    st.title('Image to Image / PDF to Image / Word to PDF Converter')

    file = st.file_uploader("Upload a file", type=['jpg', 'png', 'pdf', 'docx'])

    if file is not None:
        file_type = st.selectbox("Select output format", ['jpg', 'png', 'pdf'])

        if st.button('Convert'):
            if file_type in ['jpg', 'png']:
                if file.type in ['image/jpeg', 'image/png']:
                    output_file = convert_image(file, file_type)
                    st.success('File converted successfully.')
                    st.markdown(create_download_link(output_file), unsafe_allow_html=True)
                elif file.type == 'application/pdf':
                    output_files = convert_pdf_to_images(file, file_type)
                    for output_file in output_files:
                        st.success('File converted successfully.')
                        st.markdown(create_download_link(output_file), unsafe_allow_html=True)
                else:
                    st.error('Please upload a jpg, png, or pdf file to convert to another image format.')
            elif file_type == 'pdf':
                if file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    output_file = convert_word_to_pdf(file)
                    st.success('File converted successfully.')
                    st.markdown(create_download_link(output_file), unsafe_allow_html=True)
                else:
                    st.error('Please upload a docx file to convert to pdf.')

if __name__ == "__main__":
    main()
