# Timetable Generator for Christ University - Dept. of CSE

## Overview
This project is a **Timetable Generator** designed specifically for the **Department of Computer Science & Engineering (CSE)** at Christ University. The system automates the generation of timetables by considering multiple academic inputs, ensuring no conflicts while optimizing class schedules.

## Features
- Handles **Even and Odd Semesters** separately.
- Supports **Certification Classes**, **Global Elective Programs**, and **Open Electives**.
- Ensures no scheduling conflicts for faculty and students.
- Generates multiple valid timetable variations for better selection.
- Uses **SQLite database** to store course and faculty data.

## Requirements
- **Python 3.x**
- **SQLite** for database storage
- **Flask / Django** (for web interface, if applicable)
- **Excel/CSV Parser** (for importing data, if required)

## Usage
1. Input course details, faculty assignments, and semester type.
2. Select the categories (Certifications, Global Electives, Open Electives, etc.).
3. The system will generate a timetable ensuring no conflicts.
4. Export the generated timetable as **Excel/PDF** if needed.

## Example Input
- **Semester:** Odd / Even
- **Courses:** DBMS, AI, Cloud Computing
- **Certifications:** AWS, Data Science
- **Global Electives:** Finance, Psychology
- **Open Electives:** Cybersecurity, Blockchain


