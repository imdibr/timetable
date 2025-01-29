import pandas as pd

# Initialize timetable structure
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
periods = [f"Period {i+1}" for i in range(6)]
sections = 9  # Number of sections
timetable = {section: {day: {period: "" for period in periods} for day in days_of_week} for section in range(1, sections + 1)}

# Assign fixed classes
fixed_classes = ["Honours/Minors/Certification Course","Meeting Hour"]
for section in timetable:
    timetable[section]["Tuesday"]["Period 5"] = fixed_classes[0]
    timetable[section]["Tuesday"]["Period 6"] = fixed_classes[0]
    timetable[section]["Friday"]["Period 5"] = fixed_classes[0]
    timetable[section]["Friday"]["Period 6"] = fixed_classes[0]
    timetable[section]["Monday"]["Period 4"] = fixed_classes[1]

# Function to input elective timings
def input_elective_timings(even_sem):
    electives_schedule = {}
    print("\nPlease enter the timings for each elective type:")

    electives = ["Program Elective"]
    if even_sem:
        electives.append("Global Elective")
    else:
        electives.append("Open Elective")

    for elective in electives:
        print(f"\nConfiguring {elective}:")
        if elective == "Global Elective" or elective == "Open Elective":
            day = input("Enter the day (e.g., Monday): ").capitalize()
            period = int(input("Enter the starting period number (e.g., 1): "))
            # Ensure no two-hour session at Monday, Period 3
            if day == "Monday" and period == 3:
                print("Error: Cannot assign a two-hour session starting at Monday, Period 3.")
                return None
            electives_schedule[elective] = [(day, period, period + 1)]  # Two-hour session
        elif elective == "Program Elective":
            schedule = []
            for i in range(2):  # Two theory sessions
                day = input(f"Enter the day for Theory Session {i+1} (e.g., Monday): ").capitalize()
                period = int(input(f"Enter the starting period number for Theory Session {i+1} (e.g., 1): "))
                schedule.append((day, period, period))
            # Practical session
            day = input("Enter the day for Practical Session (e.g., Monday): ").capitalize()
            period = int(input("Enter the starting period number for Practical Session (e.g., 1): "))
            if day == "Monday" and period == 3:
                    print("Error: Cannot assign a two-hour session starting at Monday, Period 3.")
                    return None
            schedule.append((day, period, period + 1))
            electives_schedule[elective] = schedule

    return electives_schedule

# Assign electives to the timetable
def assign_electives(elective_schedule):
    for section in timetable:
        for elective, sessions in elective_schedule.items():
            for session in sessions:
                day, start_period, end_period = session
                for period in range(start_period, end_period + 1):
                    timetable[section][day][f"Period {period}"] = elective

# Main function
def main():
    print("Welcome to Timetable Generator")
    print("\nSelect the year for timetable generation:")
    print("1. 2nd Year")
    print("2. 3rd Year")
    year_choice = int(input("Enter your choice (1 or 2): "))

    if year_choice == 2:
        semester_type = input("Enter semester type (even/odd): ").strip().lower()
        if semester_type not in ["even", "odd"]:
            print("Invalid semester type! Please restart.")
            return

        print(f"\nYou selected 3rd Year ({semester_type} semester).")
        even_sem = semester_type == "even"
        elective_schedule = input_elective_timings(even_sem)  # Get elective timings from user
        if elective_schedule is None:
            print("Timetable generation aborted due to invalid input.")
            return
        assign_electives(elective_schedule)  # Assign electives to the timetable

        # Convert timetable to a pandas DataFrame for export to Excel
        final_timetable = []
        for section in timetable:
            for day in days_of_week:
                row = {"Section": section, "Day": day}
                row.update(timetable[section][day])
                final_timetable.append(row)

        df = pd.DataFrame(final_timetable)
        file_name = "timetable.xlsx"
        df.to_excel(file_name, index=False)
        print(f"\nTimetable has been saved to {file_name}")
    else:
        print("\nTimetable generation for 2nd Year is not yet supported.")

if __name__ == "__main__":
    main()
