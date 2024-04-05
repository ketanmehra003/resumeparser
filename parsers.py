import re


def extract_skills(resume_text):
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
    # Example usage
    example_resume_text = """
    This is a sample resume text. It mentions skills like Python, Java, Data Analysis,
    Machine Learning, and Project Management.
    """
    skills = extract_skills(example_resume_text)
    print("Extracted Skills:", skills)
