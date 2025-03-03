from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handling file upload
        file = request.files['timetable_file']
        if file and file.filename.endswith('.xlsx'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            
            # Get user inputs
            second_year_values = request.form.getlist('second_year_timetable')
            third_year_values = request.form.getlist('third_year_timetable')
            semester = request.form.get('semester')
            elective_classes = request.form.getlist('elective_classes')
            
            # Process the timetable (dummy processing for now)
            first_year_timetable = generate_dummy_timetable(filepath, 'First Year')
            second_year_timetable = generate_dummy_timetable(filepath, 'Second Year')
            
            first_year_file = os.path.join(UPLOAD_FOLDER, "first_year_timetable.xlsx")
            second_year_file = os.path.join(UPLOAD_FOLDER, "second_year_timetable.xlsx")
            
            first_year_timetable.to_excel(first_year_file, index=False)
            second_year_timetable.to_excel(second_year_file, index=False)
            
            return render_template('index2.html', 
                                   success=True, 
                                   first_year_file='first_year_timetable.xlsx', 
                                   second_year_file='second_year_timetable.xlsx')
    
    return render_template('index2.html', success=False)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

def generate_dummy_timetable(filepath, year):
    # Dummy processing of the uploaded Excel file
    df = pd.read_excel(filepath)
    df['Processed'] = f'Timetable for {year}'
    return df

if __name__ == '__main__':
    app.run(debug=True)
