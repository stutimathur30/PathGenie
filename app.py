from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import pandas as pd
from werkzeug.utils import secure_filename
from utils.resume_parser import extract_text_from_pdf
from utils.matcher import match_jobs_from_dataset

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    try:
        job_df = pd.read_csv('data/job_postings.csv')
        total_jobs = len(job_df)
        top_skills = job_df['skills'].str.split(',').explode().str.strip().value_counts().head(5)
        jobs_by_role = job_df['job_title'].value_counts().head(5)
        
        return render_template('dashboard.html',
                           total_jobs=total_jobs,
                           top_skills=top_skills,
                           jobs_by_role=jobs_by_role)
    except Exception as e:
        return f"Dashboard Error: {str(e)}"

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        skills_input = request.form.get('skills')
        skills = [s.strip().lower() for s in skills_input.split(',') if s.strip()]
        job_df = pd.read_csv('data/job_postings.csv')
        matched_jobs = match_jobs_from_dataset(job_df, skills)
        
        return jsonify({
            "success": True,
            "html": render_template('job_results.html', jobs=matched_jobs)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"success": False, "error": "No file selected"})
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"success": False, "error": "Empty filename"})
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        resume_text = extract_text_from_pdf(filepath)
        skills = resume_text.lower().split()
        job_df = pd.read_csv('data/job_postings.csv')
        matched_jobs = match_jobs_from_dataset(job_df, skills)
        
        return jsonify({
            "success": True,
            "html": render_template('job_results.html', jobs=matched_jobs)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)