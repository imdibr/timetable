# Timetable Generator

This project is a **Timetable Generator System** designed to automate the creation of timetables for university batches with specific constraints. The system ensures optimal allocation of classes, teachers, and time slots while adhering to predefined rules.

## Features
- Generates timetables for multiple batches (2nd, 3rd, 4th years).
- Supports both **theory** and **lab classes**.
- Avoids back-to-back classes for teachers.
- Handles electives and batch-specific constraints for 3rd years.
- Outputs timetables in both database and `.xlsx` formats.

## Tech Stack
- **Backend**: Python with SQLite
- **Frontend**: ReactJS
- **Database**: SQLite for storing course, faculty, and class assignments
- **Libraries**: pandas, openpyxl

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/imdibr/timetable.git

