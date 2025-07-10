import pandas as pd

candidate_df = pd.read_csv('candidate_profiles.csv')

import re

def extract_experience(exp_str):
    match = re.findall(r"(\d+)", str(exp_str))
    if len(match) == 2:
        return int(match[0]), int(match[1])
    elif len(match) == 1:
        return int(match[0]), int(match[0])
    else:
        return None, None

candidate_df[['min_experience', 'max_experience']] = candidate_df['experience'].apply(
    lambda x: pd.Series(extract_experience(x))
)

candidate_df['skills_list'] = candidate_df['required_skills'].apply(
    lambda x: [s.strip().lower() for s in str(x).split(',')]
)

candidate_df['skills_list'] = candidate_df['required_skills'].apply(
    lambda x: [s.strip().lower() for s in str(x).split(',')]
)

candidate_df.to_csv("cleaned_candidate_profiles.csv", index=False)

job_df = pd.read_csv('job_postings.csv')

from bs4 import BeautifulSoup

job_df['clean_description'] = job_df['description'].apply(
    lambda x: BeautifulSoup(str(x), "html.parser").get_text()
)

job_df['skills_list'] = job_df['skills'].apply(
    lambda x: [s.strip().lower() for s in str(x).split(',')]
)

job_df.to_csv("cleaned_job_postings.csv", index=False)


matches = []
for job_index, job_row in job_df.iterrows():
    for candidate_index, candidate_row in candidate_df.iterrows():
        score = len(set(candidate_row['skills_list']) & set(job_row['skills_list']))
        if score > 0:  # Changed from 3 to 0
            matches.append({
                'job_title': job_row['job_title'],
                'company': job_row['company'],
                'candidate_job_title': candidate_row['job_title'],
                'candidate_min_exp': candidate_row['min_experience'],
                'candidate_max_exp': candidate_row['max_experience'],
                'match_score': score
            })

matches_df = pd.DataFrame(matches)
matches_df.to_csv("job_candidate_matches.csv", index=False)


