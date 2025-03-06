import os
import random
import pandas as pd
from flask import Flask, request, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define file paths
UPLOAD_FOLDER = "timetable/uploads"
DOWNLOAD_FOLDER = os.path.expanduser("~/Downloads")

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Configure Flask
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

# Allowed file types
ALLOWED_EXTENSIONS = {"xlsx"}

# Define column names
COLUMN_SUBJECT = "Subject Name"
COLUMN_TEACHER = "Teacher Name"
COLUMN_YEAR = "Year Name"
COLUMN_ELECTIVE = "Elective Class Status"
COLUMN_CLASS = "Class Name"

# Define days and periods
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
periods = ["Period 1", "Period 2", "Period 3", "Period 4", "Period 5", "Period 6"]

# Define sections
sections = [
    "2IT", "2DS", "2IOT", "2CS A", "2CS B", "2CS C", "2CSAIML A", "2CSAIML B", "2CSAIML C",
    "3IT", "3DS", "3IOT", "3CS A", "3CS B", "3CS C", "3CSAIML A", "3CSAIML B", "3CSAIML C"
]

# Define locked periods
locked_classes = {
    "Monday": ["Period 4"],
    "Tuesday": ["Period 5", "Period 6"],
    "Friday": ["Period 5", "Period 6"],
    "Saturday": ["Period 5", "Period 6"],
}

def create_empty_timetable():
    """Creates an empty timetable structure for all sections."""
    return {
        section: {day: {period: "" for period in periods} for day in days_of_week}
        for section in sections
    }

def assign_fixed_classes(timetable):
    """Assigns fixed classes to the timetable."""
    fixed_classes = ["Honours/Minors/Certification Course", "Meeting Hour"]
    for section in timetable:
        timetable[section]["Tuesday"]["Period 5"] = fixed_classes[0]
        timetable[section]["Tuesday"]["Period 6"] = fixed_classes[0]
        timetable[section]["Friday"]["Period 5"] = fixed_classes[0]
        timetable[section]["Friday"]["Period 6"] = fixed_classes[0]
        timetable[section]["Monday"]["Period 4"] = fixed_classes[1]

def assign_electives(timetable, elective_schedule):
    """Assigns elective classes to the timetable."""
    for section in timetable:
        for elective, sessions in elective_schedule.items():
            for session in sessions:
                day, start_period, end_period = session
                for period in range(start_period, end_period + 1):
                    timetable[section][day][f"Period {period}"] = elective

def assign_lab_sessions(timetable, lab_classes):
    """Assigns lab sessions to available slots."""
    random.shuffle(lab_classes)  # Randomize lab allocation order
    assigned_teachers = {day: set() for day in days_of_week}  # Track assigned teachers per day

    for row in lab_classes:
        class_name = row[COLUMN_CLASS]
        subject = row[COLUMN_SUBJECT]
        teacher_name = row[COLUMN_TEACHER]
        elective_status = row.get(COLUMN_ELECTIVE, "No").strip().lower()  # Handle missing electives safely

        # Skip if class_name is not in the timetable
        if class_name not in timetable:
            print(f"Warning: Class '{class_name}' not found in timetable. Skipping.")
            continue

        # Skip elective labs for second-year students
        if class_name.startswith("2") and elective_status == "yes":
            continue

        # Find available lab slots (two consecutive periods)
        available_slots = [
            (day, periods[i], periods[i + 1])
            for day in days_of_week
            for i in range(len(periods) - 1)
            if timetable[class_name][day][periods[i]] == ""
            and timetable[class_name][day][periods[i + 1]] == ""
            and periods[i] not in locked_classes.get(day, [])
            and teacher_name not in assigned_teachers[day]  # Prevent teacher overlap
        ]
        
        random.shuffle(available_slots)  # Randomize slot selection

        # Assign the lab session if an available slot is found
        for day, period1, period2 in available_slots:
            timetable[class_name][day][period1] = f"{subject} (Lab) - {teacher_name}"
            timetable[class_name][day][period2] = f"{subject} (Lab) - {teacher_name}"
            assigned_teachers[day].add(teacher_name)
            break  # Move to the next lab

def generate_timetable(lab_classes, elective_schedule=None):
    """Generates the complete timetable with lab assignments."""
    timetable = create_empty_timetable()
    assign_fixed_classes(timetable)
    if elective_schedule:
        assign_electives(timetable, elective_schedule)
    assign_lab_sessions(timetable, lab_classes)
    return timetable

def process_file(file_path, semester_type):
    """Processes the uploaded Excel file and generates timetables."""
    df = pd.read_excel(file_path)

    # Ensure required columns are present
    required_columns = {COLUMN_SUBJECT, COLUMN_TEACHER, COLUMN_YEAR, COLUMN_CLASS, COLUMN_ELECTIVE}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        return f"Error: Missing columns: {missing}", 400

    # Fill missing elective values with "No"
    df[COLUMN_ELECTIVE] = df.get(COLUMN_ELECTIVE, "No").fillna("No")

    # Generate elective schedule based on semester type
    elective_schedule = None
    if semester_type == "even":
        elective_schedule = {
            "Global Elective": [("Wednesday", 1, 2)]  # Example: Wednesday, Periods 1-2
        }
    elif semester_type == "odd":
        elective_schedule = {
            "Open Elective": [("Thursday", 3, 4)]  # Example: Thursday, Periods 3-4
        }

    # Generate timetable
    timetable = generate_timetable(df.to_dict(orient="records"), elective_schedule)

    # Save to Excel
    second_year_output = os.path.join(DOWNLOAD_FOLDER, "2nd_year_timetable.xlsx")
    third_year_output = os.path.join(DOWNLOAD_FOLDER, "3rd_year_timetable.xlsx")

    with pd.ExcelWriter(second_year_output, engine="xlsxwriter") as writer:
        for section in sections:
            if section.startswith("2"):
                df_section = pd.DataFrame([{**{"Day": day}, **timetable[section][day]} for day in days_of_week])
                df_section.to_excel(writer, sheet_name=section, index=False)

    with pd.ExcelWriter(third_year_output, engine="xlsxwriter") as writer:
        for section in sections:
            if section.startswith("3"):
                df_section = pd.DataFrame([{**{"Day": day}, **timetable[section][day]} for day in days_of_week])
                df_section.to_excel(writer, sheet_name=section, index=False)

    return f"""
        ✅ Timetable generated! <br>
        📥 <a href='/download/2nd_year_timetable.xlsx' download>Download 2nd Year Timetable</a><br>
        📥 <a href='/download/3rd_year_timetable.xlsx' download>Download 3rd Year Timetable</a>
    """

def allowed_file(filename):
    """Checks if uploaded file has allowed extensions."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    """Serves the homepage."""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles file upload."""
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Get semester type from form data
        semester_type = request.form.get("semester", "even").strip().lower()
        if semester_type not in ["even", "odd"]:
            return "Invalid semester type", 400

        result = process_file(file_path, semester_type)
        os.remove(file_path)  # Remove uploaded file after processing
        return result

    return "Invalid file type", 400

@app.route("/download/<filename>")
def download_file(filename):
    """Handles file download."""
    file_path = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return f"File not found: {file_path}", 404

    return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)