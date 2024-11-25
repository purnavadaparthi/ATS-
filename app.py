from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a folder for uploads if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Skills and requirements for different roles
role_requirements = {
    "MERN Stack Developer": ['MongoDB', 'Express.js', 'React', 'Node.js'],
    "MEAN Stack Developer": ['MongoDB', 'Express.js', 'Angular', 'Node.js'],
    "WEB FullStack Developer": ['HTML', 'CSS', 'JavaScript', 'Node.js', 'React', 'SQL'],
    "Java FullStack Developer": ['Java', 'Spring Boot', 'Angular', 'SQL', 'JavaScript'],
    "ReactNative Developer": ['React Native', 'JavaScript', 'Redux', 'Firebase'],
    "Android Developer": ['Java', 'Kotlin', 'Android Studio', 'XML'],
    "PHP Developer": ['PHP', 'Laravel', 'MySQL', 'JavaScript'],
    "UI UX Developer": ['Adobe XD', 'Figma', 'Sketch', 'HTML', 'CSS', 'JavaScript'],
    "ServiceNow Developer": ['ServiceNow', 'JavaScript', 'REST APIs', 'ITSM'],
    "DotNet Developer": ['C#', '.NET Framework', 'ASP.NET', 'SQL Server'],
    "DataBase Developer": ['SQL', 'Database Design', 'PL/SQL', 'NoSQL'],
    "QA Automation Tester": ['Selenium', 'Java', 'TestNG', 'Jenkins', 'Python'],
    "HR Recruiter": ['Talent Acquisition', 'Interviewing', 'HR Management', 'Communication'],
    "Accountant": ['Financial Reporting', 'Excel', 'Bookkeeping', 'Taxation'],
    "Node.js Developer": ['Node.js', 'Express.js', 'MongoDB', 'JavaScript'],
    "Data Analyst": ['Data Analysis', 'Python', 'SQL', 'Tableau'],
    "Data Engineer": ['Python', 'SQL', 'Hadoop', 'Spark'],
    "AI Engineer": ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow'],
    "Java Developer": ['Java', 'Spring Boot', 'Hibernate', 'SQL'],
    "Data Scientist": ['Python', 'Machine Learning', 'Data Analysis', 'Pandas', 'Numpy']
}

# Function to simulate matching a resume to the role requirements
def match_resume(file_path, selected_roles, experience_level):
    extracted_skills = ['Python', 'Machine Learning', 'Data Analysis', 'JavaScript', 'React']  # Example extracted skills
    extracted_experience = 3  # Example years of experience

    results = {}

    for role in selected_roles:
        if role not in role_requirements:
            continue

        skills = role_requirements[role]
        missing_skills = [skill for skill in skills if skill not in extracted_skills]

        try:
            if 'above' in experience_level:
                min_experience_required = 10
            else:
                min_experience_required = int(experience_level.split('-')[0].replace(' yr', '').split()[0])

            if extracted_experience >= min_experience_required:
                experience_score = 1
                experience_status = "Experience matched"
            else:
                experience_score = 0
                experience_status = f"Experience does not meet the requirement. ({min_experience_required} years required, found {extracted_experience} years)"

        except ValueError:
            experience_status = "Invalid experience level specified"
            experience_score = 0

        matching_skills = [skill for skill in skills if skill in extracted_skills]
        skill_score = len(matching_skills) / len(skills)

        total_score = (skill_score * 0.7) + (experience_score * 0.3)
        total_score_percentage = total_score * 100

        if total_score_percentage >= 70:
            results[role] = f"{role}: Resume matched with {round(total_score_percentage, 2)}% accuracy. {experience_status}"
        else:
            results[role] = f"{role}: Resume not matched. Score: {round(total_score_percentage, 2)}%. {experience_status}"

    return results

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['resume']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file: 
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            file.save(file_path)

            experience = request.form.get('experience')
            selected_roles = request.form.getlist('roles')

            if not selected_roles:
                flash('No roles selected.')
                return redirect(request.url)

            result = match_resume(filename, selected_roles, experience)
            for role_result in result.values():
                flash(role_result)

            return redirect(url_for('upload_file'))

    return render_template('upload.html', roles=role_requirements.keys())

if __name__ == '__main__':
    app.run(debug=True)
