def match_jobs_from_dataset(df, user_skills, top_k=5):
    matched = []
    for _, row in df.iterrows():
        job_skills = str(row['skills']).lower().split()
        score = len(set(user_skills).intersection(set(job_skills)))
        if score > 0:
            matched.append((score, row.to_dict()))
    matched.sort(reverse=True, key=lambda x: x[0])
    return [job for _, job in matched[:top_k]]
