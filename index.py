from flask import Flask, request
import os
# import json
from utility import download_pdf, convertPdf2Docx

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/convert', methods=['POST'])
def convert():
    asset = request.json
    print(request)

    pdf_url = asset['url']
    print(pdf_url)
    
    local_pdf_path = '/tmp/temp.pdf'
    local_docx_path = '/tmp/temp.docx'

    try:
        # Step 1: Download PDF from Cloudinary
        download_pdf(pdf_url, local_pdf_path)

        # Step 2: Convert PDF to DOCX
        convertPdf2Docx(local_pdf_path, local_docx_path)

        # Step 3: Upload DOCX to Cloudinary
        # response = upload2CMS(local_docx_path)
        
        # if response.status_code == 201:
        #     print(f'Process completed successfully:\n {response.json()}')

    finally:
        # Clean up local files
        if os.path.exists(local_pdf_path):
            os.remove(local_pdf_path)
        if os.path.exists(local_docx_path):
            os.remove(local_docx_path)

    return {"messge": "done"}, 200

if __name__ == '__main__':
    app.run(debug=True)
