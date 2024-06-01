from flask import Flask, request
import os
import json
import time
from utility import download_pdf, convertPdf2Docx, upload2CMS, extract_text_from_pdf, save_document, convert_json_to_docx

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/convert', methods=['POST'])
def convert():
    asset = request.json

    pdf_url = asset['url']

    print(pdf_url)
    if asset['filename'].split('.')[1]!= 'pdf':
        return {"message": "File is not of type PDF"}, 400
    
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

        # if raw_text.find('```json'):
        first_json_index = raw_text.find('```json') + 7
        last_json_index = raw_text.rfind('```')
        raw_text = raw_text[first_json_index:last_json_index].strip()

        # Parse the cleaned JSON text
        json_data = json.loads(raw_text)

        # Convert the JSON data to a DOCX file
        output_docx = '/tmp/output.docx'
        try :
            doc = convert_json_to_docx(json_data)
            save_document(doc, output_docx)

            try:
                # generate two variables where title and fiename is timestampped
                title = str(int(round(time.time() * 1000)))
                filename = title + '.docx'

                uploadRes = upload2CMS(output_docx, {'title': title, 'filename': filename})
                # print(f'uploaded {uploadRes.json()} {uploadRes.status_code}')
                
                # Return the JSON data back as the response
                if uploadRes:
                    # print(f'Process completed successfully:\n {uploadRes.json()}')
                    return uploadRes.json(), uploadRes.status_code
                else:
                    return {"Error": "Error while uploading document"}, 422
            
            except Exception as error:
                print(f"Error while uploading document: {error}")
                return {"Error": "Error while uploading document"}, 422
            
        except Exception as error:
            print(f"Error while converting to docx: {error}")
            return {"Error": "Bad Request"}, 400

    
    except Exception as error:
        print(f"Error =========: {error}")
        return {"Error": "Bad Request..."}, 400


if __name__ == '__main__':
    app.run(debug=True)
