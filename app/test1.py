from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def identify_low_ats_parameters(job_description, resume_skills, threshold=0.75):
    resume_skills_text = ' '.join(resume_skills)
    
    # Combine job description and resume skills
    documents = [job_description, resume_skills_text]

    # Create a CountVectorizer object
    count_vectorizer = CountVectorizer().fit_transform(documents)

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(count_vectorizer)

    # ATS score is the cosine similarity value between the two documents
    ats_score = cosine_sim[0][1]

    # Check if ATS score is below threshold
    if ats_score < threshold:
        # Get the terms that contributed to the low score
        job_description_tokens = CountVectorizer().fit([job_description]).get_feature_names_out()
        resume_skills_tokens = CountVectorizer().fit([resume_skills_text]).get_feature_names_out()
        
        # Get the indices of resume skills terms that contributed to low score
        low_score_indices = cosine_sim[1].argsort()[:10]  # Get the indices of the 10 lowest scoring terms
        
        # Get the terms from resume skills corresponding to low score indices
        low_score_terms = [resume_skills_tokens[idx] for idx in low_score_indices]
        
        return {
            "ATS Score": ats_score,
            "Low Score Parameters": low_score_terms
        }
    else:
        return {"ATS Score": ats_score, "Low Score Parameters": None}

# Example usage
job_description = "Strong programming skills in Python and Java required. Experience with data analysis and machine learning preferred."
resume_skills = ["Python", "Java", "Data Analysis", "C++"]

result = identify_low_ats_parameters(job_description, resume_skills)
print(result)
