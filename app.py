from flask import Flask, request, jsonify
import os
import json
import time
from utility import download_pdf, convertPdf2Docx, upload2CMS, extract_text_from_pdf, save_json_to_docx

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

# Post method to accept url of pdf and pass it to extract_text_from_pdf utility
@app.route('/extract', methods=['POST'])
def extract():
    try:
        local_pdf_path = '/tmp/extract_text.pdf'
        pdf_url = request.json['url']
        res = extract_text_from_pdf(pdf_url, local_pdf_path)
        return {"content": {
            "paras": res
        }}, 200
    except Exception as error:
        print(f"Error while extracting text: {error}")
        return {"error": str(error)}, 500
    
@app.route('/todocx', methods=['POST'])
def text_2_docx():
    try:
        raw_text = request.get_data(as_text=True)

        # Remove ```json at the beginning and ``` at the end
        if raw_text.startswith('```json'):
            raw_text = raw_text[len('```json'):].strip()
        if raw_text.endswith('```'):
            raw_text = raw_text[:-len('```')].strip()

        # Parse the cleaned JSON text
        json_data = json.loads(raw_text)

        # Log the received data (for debugging purposes)
        # print('Received JSON:', json_data)

        # Convert the JSON data to a DOCX file
        output_docx = '/tmp/output.docx'
        save_json_to_docx(json_data, output_docx)

        print(f"Converted JSON to DOCX at {output_docx}")

        # generate two variables where title and fiename is timestampped
        title = str(int(round(time.time() * 1000)))
        filename = title + '.docx'

        upload2CMS(output_docx, {'title': title, 'filename': filename})

        return {"message": "file Created!!"}, 201
        

        # Return the JSON data back as the response
        # return jsonify(json_data), 200
    
    except Exception as error:
        print(f"Error while converting to docx: {error}")
        return {"error": "Bad request"}, 400


if __name__ == '__main__':
    app.run(debug=True)

# output_docx = 'output.docx'
        # print('==============')
        # save_json_to_docx(content, output_docx)
        # return {"message": "file converted!!"}, 201