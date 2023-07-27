import requests
import json
from werkzeug.datastructures import FileStorage

UPLOAD_ENDPOINT = "http://127.0.0.1:5000"


#test calling the endoint
def test_can_call_endpoint():
    response = requests.get(UPLOAD_ENDPOINT)
    assert response.status_code == 200
    

#test a successful file upload
def test_successful_file_upload():
    # Create a sample file to upload
    file_data = b'Test file content'
    file = FileStorage(stream=file_data, filename='test_file.csv')
    
    # Send a POST request to the file upload endpoint
    response = requests.post(url = UPLOAD_ENDPOINT+'/products/upload', data={'file': file})
    
    # Assert the response status code
    assert response.status_code == 200
   

#test the file upload process accepts only csv files
def test_incorrect_file_format_upload():
      # Create a sample file to upload
    file_data = b'Test file content'
    file = {'file': ('test_file.txt', file_data)}

    # Send a POST request to the file upload endpoint
    response = requests.post(url=UPLOAD_ENDPOINT+'/products/process_file', files=file)
    print("response content", response)
    upload_error = b'Wrong file format. Please upload a csv file'
    assert upload_error in response.content

#test for a missing file upload
def test_missing_file():
    url = UPLOAD_ENDPOINT+'/products/process'
    response = requests.post(url = url, files="")
    upload_error = b'No file received, please upload a csv file'

    print("response", response.content)
    assert response.status_code == 200
    #check if it receives the response error on encountering a missing file
   


