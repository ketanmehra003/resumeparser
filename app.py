from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
from parsers import extract_skills

app = Flask(__name__)

# Define the upload directory
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def print_resume_content(pdf_path):
    # Call readfile.py passing the resume path as argument
    process = subprocess.Popen(['python', 'readfile.py', pdf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8')

@app.route('/')
def index():
    return render_template('resumeparser.html')

@app.route('/parse', methods=['POST'])
def parse_resume():
    # Check if the POST request has the file part
    if 'resume' not in request.files:
        return redirect(request.url)

    resume_file = request.files['resume']
    print(resume_file)
    # resume_text=print_resume_content(resume_file)
    # Skills=extract_skills(resume_text)
    # print(Skills)

    # If the user does not select a file, the browser submits an empty file without a filename
    if resume_file.filename == '':
        return redirect(request.url)

    if resume_file:
        # Save the uploaded resume file
        resume_filename = resume_file.filename
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        resume_file.save(resume_path)

        # Call readfile.py passing the resume path as argument
        subprocess.Popen(['python', 'readfile.py', resume_path])
        

        return "Resume uploaded successfully and sent for parsing."

if __name__ == '__main__':
    app.run(debug=True)
