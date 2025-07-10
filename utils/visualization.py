import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import os

def generate_plots(supervised_metrics=None, nn_metrics=None):
    plots = []

    # Load job postings dataset
    job_path = "data/job_postings.csv"
    if not os.path.exists(job_path):
        print("Job data not found at", job_path)
        return []

    df = pd.read_csv(job_path)

    # Clean and extract skills
    df['skills'] = df['skills'].fillna('')
    all_skills = df['skills'].str.split(', ').explode()
    top_skills = all_skills.value_counts().head(10)
    skill_bar = go.Figure([go.Bar(x=top_skills.index, y=top_skills.values)])
    skill_bar.update_layout(title='Top 10 In-Demand Skills', xaxis_title='Skill', yaxis_title='Count')
    plots.append(skill_bar)

    # Most common job titles
    if 'job_title' in df:
        job_title_counts = df['job_title'].value_counts().head(5)
        job_pie = px.pie(values=job_title_counts.values, names=job_title_counts.index,
                         title='Most Common Job Titles')
        plots.append(job_pie)

    # Experience distribution
    if 'experience_required' in df and df['experience_required'].notnull().sum():
        df['experience_required'] = df['experience_required'].fillna('0')
        df['experience_years'] = df['experience_required'].str.extract(r'(\d+)')[0].astype(float)
        exp_hist = px.histogram(df, x='experience_years', nbins=10, title='Experience Required Distribution')
        plots.append(exp_hist)

    # Optional: supervised model accuracy if available
    if supervised_metrics and isinstance(supervised_metrics, dict):
        bar = go.Figure([go.Bar(x=list(supervised_metrics.keys()), y=list(supervised_metrics.values()))])
        bar.update_layout(title='Supervised Model Metrics')
        plots.append(bar)

    # Optional: neural net accuracy if available
    if nn_metrics and isinstance(nn_metrics, dict):
        bar = go.Figure([go.Bar(x=list(nn_metrics.keys()), y=list(nn_metrics.values()))])
        bar.update_layout(title='Neural Net Model Metrics')
        plots.append(bar)

    return plots