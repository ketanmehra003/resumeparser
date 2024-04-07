import PyPDF2
import sys

def parse_resume(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty string to store the text
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

if __name__ == '__main__':
    # Get the path of the uploaded PDF file from command line arguments
    pdf_path = sys.argv[1]
    resume_text = parse_resume(pdf_path)
    print(resume_text)
