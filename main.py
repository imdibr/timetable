from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import xlsxwriter
import os

app = Flask(__name__)

# Section names
sections = ["IT", "DS", "IOT", "CS A", "CS B", "CS C", "CSAIML A", "CSAIML B", "CSAIML C"]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
periods = [f"Period {i+1}" for i in range(6)]

timetable = {section: {day: {period: "" for period in periods} for day in days_of_week} for section in sections}

# Assign fixed classes
fixed_classes = ["Honours/Minors/Certification Course", "Meeting Hour"]
for section in timetable:
    timetable[section]["Tuesday"]["Period 5"] = fixed_classes[0]
    timetable[section]["Tuesday"]["Period 6"] = fixed_classes[0]
    timetable[section]["Friday"]["Period 5"] = fixed_classes[0]
    timetable[section]["Friday"]["Period 6"] = fixed_classes[0]
    timetable[section]["Monday"]["Period 4"] = fixed_classes[1]

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/generate_timetable', methods=['POST'])
def generate_timetable():
    # Get form data
    day = request.form.get('day')
    period = request.form.get('period')
    semester = request.form.get('semester')
    global_day = request.form.get('globalDay')
    global_period = request.form.get('globalPeriod')
    open_day1 = request.form.get('openDay1')
    open_period1 = request.form.get('openPeriod1')
    open_day2 = request.form.get('openDay2')
    open_period2 = request.form.get('openPeriod2')
    open_day3 = request.form.get('openDay3')
    open_period3 = request.form.get('openPeriod3')
    program_day1 = request.form.get('programDay1')
    program_period1 = request.form.get('programPeriod1')
    program_day2 = request.form.get('programDay2')
    program_period2 = request.form.get('programPeriod2')
    program_day3 = request.form.get('programDay3')
    program_period3 = request.form.get('programPeriod3')

    # Process the data and generate the timetable
    # This is a simplified example; you would need to implement the logic to update the timetable dictionary
    # based on the form inputs.

    # Save the timetable to an Excel file
    file_name = "timetable.xlsx"
    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        for section in sections:
            df = pd.DataFrame([{"Day": day, **timetable[section][day]} for day in days_of_week])
            df.to_excel(writer, sheet_name=section, index=False)

    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)