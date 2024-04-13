import PyPDF2
import sys
import re

def parse_resume(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty string to store the
        resume_text = ''
        
        # Loop through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Extract text from the page
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            # Append the text from this page to the resume_text string
            resume_text += page_text
            
        # Return the extracted text
        return resume_text

def extract_skills(pdf_path):

    resume_text = parse_resume(pdf_path)
    # List of predefined skills (you can adjust or expand this list)
    skills_list = [
        'Python', 'Java', 'JavaScript', 'HTML', 'CSS', 'SQL',
        'Machine Learning', 'Data Analysis', 'Data Science', 'AI',
        'Project Management', 'Communication', 'Teamwork', 'Problem Solving'
    ]

    # Initialize an empty list to store the extracted skills
    extracted_skills = []

    # Convert resume text to lowercase for case-insensitive matching
    resume_text_lower = resume_text.lower()

    # Iterate through each skill in the skills list and check if it appears in the resume text
    for skill in skills_list:
        # Use regular expression to find the skill in the resume text
        # We use word boundaries (\b) to match whole words only
        if re.search(r'\b{}\b'.format(skill.lower()), resume_text_lower):
            extracted_skills.append(skill)

    return extracted_skills

if __name__ == '__main__':
    # Get the path of the uploaded PDF file from command line arguments
    pdf_path = sys.argv[1]
    resume_text = extract_skills(pdf_path)
    print(resume_text)
