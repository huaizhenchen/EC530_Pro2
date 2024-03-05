import requests

url = 'http://localhost:5000/process'
headers = {'Content-Type': 'application/json'}
data = {
    'pdf_paths': ['pdftest1.pdf', 'pdftest2.pdf','pdftest3.pdf']
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("API call successful!")
    print("Returned summaries:", response.json())
else:
    print("API call failed, status code:", response.status_code)
