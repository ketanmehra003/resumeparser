from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Define the upload directory
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_resume():
    # Check if the POST request has the file part
    if 'resume' not in request.files:
        return redirect(request.url)

    resume_file = request.files['resume']

    # If the user does not select a file, the browser submits an empty file without a filename
    if resume_file.filename == '':
        return redirect(request.url)

    if resume_file:
        # Save the uploaded resume file
        resume_filename = resume_file.filename
        resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))

        # Now you can pass the resume file to your Python code for parsing
        # For example:
        # parse_resume_pdf(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))

        return "Resume uploaded successfully and sent for parsing."

if __name__ == '__main__':
    app.run(debug=True)
