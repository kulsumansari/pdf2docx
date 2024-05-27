from flask import Flask, request
import os
import json
from utility import download_pdf, convertPdf2Docx, upload2CMS

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/convert', methods=['POST'])
def convert():
    asset = request.json

    pdf_url = asset['url']

    print(pdf_url)
    
    local_pdf_path = '/tmp/temp.pdf'
    local_docx_path = '/tmp/temp.docx'

    try:
        # Step 1: Download PDF from Cloudinary
        download_pdf(pdf_url, local_pdf_path)

        # Step 2: Convert PDF to DOCX
        convertPdf2Docx(local_pdf_path, local_docx_path)

        # Step 3: Upload DOCX to CMS
        response = upload2CMS(local_docx_path, asset)
        
        # if response.status_code == 201:
        #     print(f'Process completed successfully:\n {response.json()}')

    except Exception as error:
        print(f"Error while uploading document: {error}")
        return {"message": "Some error occured... Check logs"}, 500


    finally:
        # Clean up local files
        if os.path.exists(local_pdf_path):
            os.remove(local_pdf_path)
        if os.path.exists(local_docx_path):
            os.remove(local_docx_path)

    return {"message": "file converted!!"}, response.status_code

if __name__ == '__main__':
    app.run(debug=True)
