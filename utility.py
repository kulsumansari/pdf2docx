# import requests
# from pdf2docx import Converter
# from dotenv import dotenv_values

# config = dotenv_values(".env")


# def download_pdf(pdf_url, local_pdf_path):
    
#     response = requests.get(pdf_url)
#     with open(local_pdf_path, 'wb') as file:
#         file.write(response.content)
#     print(f"Downloaded PDF from {pdf_url} to {local_pdf_path}")
    

# # convert to local docx
# def convertPdf2Docx(local_pdf_path, local_docx_path):

#     cv = Converter(local_pdf_path)
#     cv.convert(local_docx_path)
#     cv.close()
#     print(f"Converted PDF from {local_pdf_path} to DOCX at {local_docx_path}")
    
    
# # upload to CMS
# def upload2CMS(local_docx_path):
#     import os

#     try:
#         url = "https://api.contentstack.io/v3/assets"

#         payload = {'asset[title]': 'doc2222'}
#         files=[
#             ('asset[upload]',('sample1.docx',open(local_docx_path,'rb'),'application/octet-stream'))
#         ]
#         headers = {
#             'api_key': config['API_KEY'],
#             'authorization': config['AUTHORIZATION']
#         }

#         response = requests.request('POST', url, headers=headers, data=payload, files=files)
#         print("🚀 ~ response:", response.text)

#         # print(response)
#         # if response.status != 201:
#         #     raise Exception(response.text)
        
#         return response

#     except Exception as error:
#         print(f"Error while uploading document: {error}")
#         return error
