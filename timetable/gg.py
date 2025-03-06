import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime

# Import the processor module
import timetable_processor as tp

class TimetableGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Christ University Timetable Generator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F0F0F0")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#F0F0F0')
        self.style.configure('TLabel', background='#F0F0F0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 10))
        
        # Add version info and user info
        self.version_label = tk.Label(root, text=f"Last modified: 2025-03-06 19:02:05 | User: imdibr", 
                                     bg="#F0F0F0", fg="#888888", font=("Arial", 8))
        self.version_label.pack(side="bottom", anchor="se", padx=10, pady=5)
        
        self.input_file_path = None
        self.create_main_ui()
    
    def create_main_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="CHRIST UNIVERSITY TIMETABLE GENERATOR", 
                              font=("Arial", 18, "bold"))
        title_label.pack(anchor='center')
        
        # File selection area
        file_frame = ttk.LabelFrame(main_frame, text="Input File", padding="10 10 10 10")
        file_frame.pack(fill=tk.X, pady=10)
        
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        file_path_entry = ttk.Entry(file_select_frame, textvariable=self.file_path_var, 
                                   width=80, state='readonly')
        file_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(file_select_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Second year tab
        self.second_year_frame = ttk.Frame(notebook, padding="10 10 10 10")
        notebook.add(self.second_year_frame, text="Second Year Timetable")
        
        # Third year tab
        self.third_year_frame = ttk.Frame(notebook, padding="10 10 10 10")
        notebook.add(self.third_year_frame, text="Third Year Timetable")
        
        # Setup the content for each tab
        self.setup_second_year_frame()
        self.setup_third_year_frame()
        
        # Buttons for generating timetables
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        generate_button = ttk.Button(button_frame, text="Generate Timetable", 
                                   command=self.generate_timetable)
        generate_button.pack(side=tk.RIGHT, padx=5)
        
        # Status area
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value="Ready to generate timetable")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(pady=5)
    
    def setup_second_year_frame(self):
        # HED Class Input
        hed_frame = ttk.LabelFrame(self.second_year_frame, text="HED Class", padding="10 10 10 10")
        hed_frame.pack(fill=tk.X, pady=10)
        
        # HED Day
        hed_day_frame = ttk.Frame(hed_frame)
        hed_day_frame.pack(fill=tk.X, pady=5)
        
        hed_day_label = ttk.Label(hed_day_frame, text="HED Day:")
        hed_day_label.pack(side=tk.LEFT, padx=5)
        
        self.hed_day_var = tk.StringVar()
        hed_day_dropdown = ttk.Combobox(hed_day_frame, textvariable=self.hed_day_var, 
                                      values=tp.days_of_week, width=15, state="readonly")
        hed_day_dropdown.pack(side=tk.LEFT, padx=5)
        
        # HED Period
        hed_period_frame = ttk.Frame(hed_frame)
        hed_period_frame.pack(fill=tk.X, pady=5)
        
        hed_period_label = ttk.Label(hed_period_frame, text="HED Period:")
        hed_period_label.pack(side=tk.LEFT, padx=5)
        
        self.hed_period_var = tk.StringVar()
        hed_period_dropdown = ttk.Combobox(hed_period_frame, textvariable=self.hed_period_var, 
                                         values=["1", "2", "3", "4", "5", "6"], width=15, state="readonly")
        hed_period_dropdown.pack(side=tk.LEFT, padx=5)
    
    def setup_third_year_frame(self):
        # Program Elective Classes
        prog_elective_frame = ttk.LabelFrame(self.third_year_frame, text="Program Elective Classes", 
                                           padding="10 10 10 10")
        prog_elective_frame.pack(fill=tk.X, pady=10)
        
        # Program Elective 1
        elec1_frame = ttk.Frame(prog_elective_frame)
        elec1_frame.pack(fill=tk.X, pady=5)
        
        elec1_name_label = ttk.Label(elec1_frame, text="Program Elective 1 Name:")
        elec1_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.progelec1_name_var = tk.StringVar()
        elec1_name_entry = ttk.Entry(elec1_frame, textvariable=self.progelec1_name_var, width=30)
        elec1_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        elec1_day_label = ttk.Label(elec1_frame, text="Day:")
        elec1_day_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        self.progelec1_day_var = tk.StringVar()
        elec1_day_dropdown = ttk.Combobox(elec1_frame, textvariable=self.progelec1_day_var, 
                                       values=tp.days_of_week, width=15, state="readonly")
        elec1_day_dropdown.grid(row=0, column=3, padx=5, pady=5)
        
        elec1_period_label = ttk.Label(elec1_frame, text="Period:")
        elec1_period_label.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        
        self.progelec1_period_var = tk.StringVar()
        elec1_period_dropdown = ttk.Combobox(elec1_frame, textvariable=self.progelec1_period_var, 
                                          values=["1", "2", "3", "4", "5", "6"], width=15, state="readonly")
        elec1_period_dropdown.grid(row=0, column=5, padx=5, pady=5)
        
        # Program Elective 2
        elec2_frame = ttk.Frame(prog_elective_frame)
        elec2_frame.pack(fill=tk.X, pady=5)
        
        elec2_name_label = ttk.Label(elec2_frame, text="Program Elective 2 Name:")
        elec2_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.progelec2_name_var = tk.StringVar()
        elec2_name_entry = ttk.Entry(elec2_frame, textvariable=self.progelec2_name_var, width=30)
        elec2_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        elec2_day_label = ttk.Label(elec2_frame, text="Day:")
        elec2_day_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        self.progelec2_day_var = tk.StringVar()
        elec2_day_dropdown = ttk.Combobox(elec2_frame, textvariable=self.progelec2_day_var, 
                                       values=tp.days_of_week, width=15, state="readonly")
        elec2_day_dropdown.grid(row=0, column=3, padx=5, pady=5)
        
        elec2_period_label = ttk.Label(elec2_frame, text="Period:")
        elec2_period_label.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        
        self.progelec2_period_var = tk.StringVar()
        elec2_period_dropdown = ttk.Combobox(elec2_frame, textvariable=self.progelec2_period_var, 
                                          values=["1", "2", "3", "4", "5", "6"], width=15, state="readonly")
        elec2_period_dropdown.grid(row=0, column=5, padx=5, pady=5)
        
        # Lab Period
        lab_frame = ttk.Frame(prog_elective_frame)
        lab_frame.pack(fill=tk.X, pady=5)
        
        lab_label = ttk.Label(lab_frame, text="Lab Period (2 consecutive periods):")
        lab_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.lab_day_var = tk.StringVar()
        lab_day_dropdown = ttk.Combobox(lab_frame, textvariable=self.lab_day_var, 
                                      values=tp.days_of_week, width=15, state="readonly")
        lab_day_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        lab_period_label = ttk.Label(lab_frame, text="Starting Period:")
        lab_period_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        self.lab_period_var = tk.StringVar()
        lab_period_dropdown = ttk.Combobox(lab_frame, textvariable=self.lab_period_var, 
                                         values=["1", "2", "3", "4", "5"], width=15, state="readonly")
        lab_period_dropdown.grid(row=0, column=3, padx=5, pady=5)
        
        # Semester Selection
        semester_frame = ttk.LabelFrame(self.third_year_frame, text="Semester Selection", 
                                      padding="10 10 10 10")
        semester_frame.pack(fill=tk.X, pady=10)
        
        semester_type_frame = ttk.Frame(semester_frame)
        semester_type_frame.pack(fill=tk.X, pady=5)
        
        semester_label = ttk.Label(semester_type_frame, text="Semester Type:")
        semester_label.pack(side=tk.LEFT, padx=5)
        
        self.semester_type_var = tk.StringVar(value="odd")  # Default to odd
        odd_radio = ttk.Radiobutton(semester_type_frame, text="Odd", variable=self.semester_type_var, 
                                  value="odd", command=self.update_semester_options)
        odd_radio.pack(side=tk.LEFT, padx=5)
        
        even_radio = ttk.Radiobutton(semester_type_frame, text="Even", variable=self.semester_type_var, 
                                   value="even", command=self.update_semester_options)
        even_radio.pack(side=tk.LEFT, padx=5)
        
        # Container for dynamic semester-specific options
        self.semester_options_frame = ttk.Frame(semester_frame)
        self.semester_options_frame.pack(fill=tk.X, pady=10)
        
        # Initialize semester options based on default (odd)
        self.update_semester_options()
    
    def update_semester_options(self):
        # Clear current frame contents
        for widget in self.semester_options_frame.winfo_children():
            widget.destroy()
        
        semester_type = self.semester_type_var.get()
        
        if semester_type == "even":
            # Global Elective (2 consecutive periods)
            global_elec_frame = ttk.LabelFrame(self.semester_options_frame, 
                                             text="Global Elective (2 consecutive periods)", 
                                             padding="10 10 10 10")
            global_elec_frame.pack(fill=tk.X, pady=5)
            
            ge_day_label = ttk.Label(global_elec_frame, text="Day:")
            ge_day_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            
            self.global_elec_day_var = tk.StringVar()
            ge_day_dropdown = ttk.Combobox(global_elec_frame, textvariable=self.global_elec_day_var, 
                                         values=tp.days_of_week, width=15, state="readonly")
            ge_day_dropdown.grid(row=0, column=1, padx=5, pady=5)
            
            ge_period_label = ttk.Label(global_elec_frame, text="Starting Period:")
            ge_period_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
            
            self.global_elec_period_var = tk.StringVar()
            ge_period_dropdown = ttk.Combobox(global_elec_frame, textvariable=self.global_elec_period_var, 
                                            values=["1", "2", "3", "4", "5"], width=15, state="readonly")
            ge_period_dropdown.grid(row=0, column=3, padx=5, pady=5)
        
        else:  # odd semester
            # Open Electives (3 individual periods)
            open_elec_frame = ttk.LabelFrame(self.semester_options_frame, text="Open Electives", 
                                           padding="10 10 10 10")
            open_elec_frame.pack(fill=tk.X, pady=5)
            
            # Variables for open electives
            self.open_elec_vars = []
            
            # Create 3 open elective entries
            for i in range(1, 4):
                elec_row = ttk.Frame(open_elec_frame)
                elec_row.pack(fill=tk.X, pady=5)
                
                elec_label = ttk.Label(elec_row, text=f"Open Elective {i}:")
                elec_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
                
                # Day selection
                day_var = tk.StringVar()
                day_dropdown = ttk.Combobox(elec_row, textvariable=day_var, 
                                         values=tp.days_of_week, width=15, state="readonly")
                day_dropdown.grid(row=0, column=1, padx=5, pady=5)
                
                period_label = ttk.Label(elec_row, text="Period:")
                period_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
                
                # Period selection
                period_var = tk.StringVar()
                period_dropdown = ttk.Combobox(elec_row, textvariable=period_var,
                                            values=["1", "2", "3", "4", "5", "6"], width=15,
                                            state="readonly")
                period_dropdown.grid(row=0, column=3, padx=5, pady=5)
                
                # Store variables for later access
                self.open_elec_vars.append((day_var, period_var))
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input Excel File",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        
        if file_path:
            self.input_file_path = file_path
            self.file_path_var.set(file_path)
            self.status_var.set(f"File selected: {os.path.basename(file_path)}")
    
    def get_config(self):
        """Collect all configuration values from the UI"""
        config = {
            # Second year config
            'hed_day': self.hed_day_var.get(),
            'hed_period': self.hed_period_var.get(),
            
            # Third year config
            'progelec1_name': self.progelec1_name_var.get(),
            'progelec1_day': self.progelec1_day_var.get(),
            'progelec1_period': self.progelec1_period_var.get(),
            'progelec2_name': self.progelec2_name_var.get(),
            'progelec2_day': self.progelec2_day_var.get(),
            'progelec2_period': self.progelec2_period_var.get(),
            'lab_day': self.lab_day_var.get(),
            'lab_period': self.lab_period_var.get(),
            'semester_type': self.semester_type_var.get()
        }
        
        # Add semester-specific config
        if self.semester_type_var.get() == 'even':
            config.update({
                'global_elec_day': getattr(self, 'global_elec_day_var', tk.StringVar()).get(),
                'global_elec_period': getattr(self, 'global_elec_period_var', tk.StringVar()).get()
            })
        else:
            # Add open electives
            for i, (day_var, period_var) in enumerate(getattr(self, 'open_elec_vars', []), 1):
                config[f'open_elec{i}_day'] = day_var.get()
                config[f'open_elec{i}_period'] = period_var.get()
        
        return config
    
    def generate_timetable(self):
        """Generate timetable and save to Excel files"""
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select an input Excel file")
            return
        
        try:
            # Update status
            self.status_var.set("Generating timetable...")
            self.root.update_idletasks()
            
            # Get configuration from UI
            config = self.get_config()
            
            # Validate essential inputs
            if not config.get('hed_day') or not config.get('hed_period'):
                messagebox.showwarning("Warning", "Please select day and period for HED Class")
                return
            
            # Check if third year elective configurations are set
            if not (config.get('progelec1_day') and config.get('progelec1_period') and 
                    config.get('progelec2_day') and config.get('progelec2_period')):
                messagebox.showwarning("Warning", "Please select days and periods for Program Electives")
                return
            
            # Load lab classes from Excel file
            lab_classes = tp.load_lab_classes(self.input_file_path)
            
            # Generate timetable
            timetable = tp.generate_timetable(lab_classes, config)
            
            # Select directory to save output files
            output_dir = filedialog.askdirectory(title="Select Directory to Save Timetables")
            if not output_dir:
                return
            
            # Save timetable to Excel files
            second_year_file, third_year_file = tp.save_timetable_to_excel(timetable, output_dir)
            
            # Show success message
            messagebox.showinfo("Success", 
                f"Timetables generated successfully!\n\n"
                f"Second Year Timetable: {os.path.basename(second_year_file)}\n"
                f"Third Year Timetable: {os.path.basename(third_year_file)}")
            
            self.status_var.set("Timetable generation complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableGeneratorApp(root)
    root.mainloop()