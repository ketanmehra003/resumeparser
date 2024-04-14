from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_ats_score(job_description, resume_skills):
    resume_skills = ' '.join(resume_skills)
    
    # Combine job description and resume skills
    documents = [job_description, resume_skills]

    # Create a CountVectorizer object
    count_vectorizer = CountVectorizer().fit_transform(documents)

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(count_vectorizer)

    # ATS score is the cosine similarity value between the two documents
    ats_score = cosine_sim[0][1]
    return ats_score

'''
I need to bulk send emails, the clients should then click on a link in hte email and fill out a form on the website, once submitted then a copy of that form should be sent to us, the system should know who sent the form by the link. We send this info fro a csv file. The form should only be submitted if a goal is not reached, in this case getting to a free consultation I have copies of the the html code and python code, it should only take a couple of hours if that as most of the coding is done but I am having problems in one area
'''
