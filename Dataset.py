import pandas as pd
from faker import Faker
import random

fake = Faker()

# Define job roles and their skills
job_roles = {
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Pandas"],
    "Frontend Developer": ["JavaScript", "React", "HTML/CSS"],
    "DevOps Engineer": ["AWS", "Docker", "Kubernetes"],
    # Add 20+ more roles here...
}

# Generate 10,000 entries
data = []
for _ in range(10000):
    job = random.choice(list(job_roles.keys()))
    skills = job_roles[job] + [fake.word() for _ in range(2)]  # Add 2 random skills
    experience = f"{random.randint(0, 5)}-{random.randint(2, 10)} years"
    data.append([job, ", ".join(skills), experience])

# Save to CSV
df = pd.DataFrame(data, columns=["job_title", "required_skills", "experience"])
df.to_csv("10,000_Job_Listings.csv", index=False)
print("Dataset generated!")



