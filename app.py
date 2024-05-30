from flask import Flask, render_template, request
import pdfplumber
import re

app = Flask(__name__)

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_director_detail(text):
    director_details = []
    director_pattern = r"\. (.+?) \(DIN: (\w+)\) as\s+(.*?)\s+(?:Director|Directors)"
    director_info = re.findall(director_pattern, text)
    for match in director_info:
        director_details.append({'director': match[0], 'din': match[1], 'role': match[2]+" Director"})
        
    director_pattern = r"\. (.+?) \(DIN: (\w+)\),\s+(.*?)\s+(?:Director|Directors)"
    director_info = re.findall(director_pattern, text)
    for match in director_info:
        director_details.append({'director': match[0], 'din': match[1], 'role': match[2]+" Director"})
    director_pattern = r"\. (.+?) \(DIN: (\w+)\] as\s+(.*?)\s+(?:Director|Directors)"
    director_info = re.findall(director_pattern, text)
    for match in director_info:
        director_details.append({'director': match[0], 'din': match[1], 'role': match[2]+" Director"})
    director_pattern = r"\. (.+?) \(DIN: (\w+)\) as\s+an\s+(.*?)\s+(?:Director|Directors)"
    director_info = re.findall(director_pattern, text)
    for match in director_info:
        director_details.append({'director': match[0], 'din': match[1], 'role': match[2]+" Director"})
    
    return director_details

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('results.html', error='No file part')
    file = request.files['file']
    if file.filename == '':
        return render_template('results.html', error='No selected file')
    if file:
        text = extract_text_from_pdf(file)
        director_details = extract_director_detail(text)
        print(director_details)
        return render_template('results.html', director_details=director_details)

if __name__ == '__main__':
    app.run(debug=True)