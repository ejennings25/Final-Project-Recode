import tkinter as tk
from tkinter import messagebox
from database_handler import DatabaseHandler  # Import from current directory
import volunteer 
from volunteer import Volunteer
import volunteer_hours
from volunteer_hours import VolunteerHours

class VolunteerApp:
    def __init__(self, root):
        self.db_handler = DatabaseHandler()
        self.root = root
        self.root.title("Volunteer Tracking System")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        self.main_frame = tk.Frame(self.root, bg="lightblue", padx=60, pady=10)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        button_style = {"bg": "white", "fg": "black", "font": ("Arial", 12), "padx": 10, "pady": 5, "relief": tk.RAISED}

        tk.Button(self.main_frame, text="Add Volunteer", command=self.add_volunteer_menu, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Update Volunteer", command=self.update_volunteer_menu, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Remove Volunteer", command=self.remove_volunteer_menu, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Log Hours", command=self.log_hours_menu, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Generate Reports", command=self.generate_reports_menu, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Exit", command=self.exit_app, **button_style).pack(fill=tk.X, pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def add_volunteer_menu(self):
        self.clear_frame()

        tk.Label(self.root, text="Add New Volunteer", font=('Helvetica', 16, 'bold')).pack(pady=20)

        id_entry = self._extracted_from_add_volunteer_menu_6("ID:")
        name_entry = self._extracted_from_add_volunteer_menu_6("Name:")
        email_entry = self._extracted_from_add_volunteer_menu_6("Email:")
        contact_entry = self._extracted_from_add_volunteer_menu_6("Contact Info:")
        skills_entry = self._extracted_from_add_volunteer_menu_6(
            "Skills (comma-separated):"
        )
        # Save button
        save_button = tk.Button(self.root, text="Save", command=lambda: self.save_new_volunteer(id_entry.get(), name_entry.get(), email_entry.get(), contact_entry.get(), skills_entry.get()), width=10)
        save_button.pack(side='left', padx=5, pady=10)

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu, width=10)
        back_button.pack(side='left', padx=5, pady=10)

    # TODO Rename this here and in `add_volunteer_menu`
    def _extracted_from_add_volunteer_menu_6(self, text):
        # sourcery skip: class-extract-method
        tk.Label(self.root, text=text).pack()
        result = tk.Entry(self.root)
        result.pack()

        return result

    def save_new_volunteer(self, id, name, email, contact_info, skills):
        if not self.validate_not_empty(id, name, email, contact_info, skills):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        volunteer = Volunteer(id, name, email, contact_info, skills.split(','))
        self.db_handler.add_volunteer(volunteer)
        messagebox.showinfo("Success", "Volunteer added successfully!")
        self.create_main_menu()

    def update_volunteer_menu(self):
        self.clear_frame()

        tk.Label(self.root, text="Update Volunteer", font=('Helvetica', 16, 'bold')).pack(pady=20)

        tk.Label(self.root, text="Enter ID of Volunteer to Update:").pack()
        id_entry = tk.Entry(self.root)
        id_entry.pack()

        search_button = tk.Button(self.root, text="Search", command=lambda: self.search_volunteer(id_entry.get()))
        search_button.pack()

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu, width=10)
        back_button.pack(side='left', padx=5, pady=10)

    def search_volunteer(self, id):
        if volunteer := self.db_handler.get_all_volunteers():
            self.clear_frame()

            tk.Label(self.root, text="Update Volunteer", font=('Helvetica', 16, 'bold')).pack(pady=20)

            tk.Label(self.root, text="ID:").pack()
            tk.Entry(self.root, textvariable=tk.StringVar(value=volunteer.id), state='disabled').pack()

            tk.Label(self.root, text="Name:").pack()
            name_entry = tk.Entry(self.root, textvariable=tk.StringVar(value=volunteer.name))
            name_entry.pack()

            tk.Label(self.root, text="Email:").pack()
            email_entry = tk.Entry(self.root, textvariable=tk.StringVar(value=volunteer.email))
            email_entry.pack()

            tk.Label(self.root, text="Contact Info:").pack()
            contact_entry = tk.Entry(self.root, textvariable=tk.StringVar(value=volunteer.contact_info))
            contact_entry.pack()

            tk.Label(self.root, text="Skills (comma-separated):").pack()
            skills_entry = tk.Entry(self.root, textvariable=tk.StringVar(value=','.join(volunteer.skills)))
            skills_entry.pack()

            # Save button
            save_button = tk.Button(self.root, text="Save", command=lambda: self.save_updated_volunteer(volunteer.id, name_entry.get(), email_entry.get(), contact_entry.get(), skills_entry.get()), width=10)
            save_button.pack(side='left', padx=5, pady=10)

            # Back button
            back_button = tk.Button(self.root, text="Back", command=self.create_main_menu, width=10)
            back_button.pack(side='left', padx=5, pady=10)
        else:
            messagebox.showerror("Error", "Volunteer not found!")

    def save_updated_volunteer(self, id, name, email, contact_info, skills):
        if not self.validate_not_empty(id, name, email, contact_info, skills):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        volunteer = Volunteer(id, name, email, contact_info, skills.split(','))
        self.db_handler.update_volunteer(volunteer)
        messagebox.showinfo("Success", "Volunteer updated successfully!")
        self.create_main_menu()

    def remove_volunteer_menu(self):
        self.clear_frame()

        tk.Label(self.root, text="Remove Volunteer", font=('Helvetica', 16, 'bold')).pack(pady=20)

        tk.Label(self.root, text="Enter ID of Volunteer to Remove:").pack()
        id_entry = tk.Entry(self.root)
        id_entry.pack()

        remove_button = tk.Button(self.root, text="Remove", command=lambda: self.remove_volunteer(id_entry.get()), width=10)
        remove_button.pack()

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu, width=10)
        back_button.pack()

    def remove_volunteer(self, volunteer_id):
        self.db_handler.remove_volunteer(volunteer_id)
        messagebox.showinfo("Success", f"Volunteer with ID {volunteer_id} removed successfully!")
        self.create_main_menu()

    def log_hours_menu(self):
        self.clear_frame()

        tk.Label(self.root, text="Log Volunteer Hours", font=('Helvetica', 16, 'bold')).pack(pady=20)

        id_entry = self._extracted_from_log_hours_menu_6("Volunteer ID:")
        date_entry = self._extracted_from_log_hours_menu_6("Date (YYYY-MM-DD):")
        hours_entry = self._extracted_from_log_hours_menu_6("Hours Worked:")
        description_entry = self._extracted_from_log_hours_menu_6("Description:")
        log_button = tk.Button(self.root, text="Log Hours", command=lambda: self.save_volunteer_hours(id_entry.get(), date_entry.get(), hours_entry.get(), description_entry.get()), width=10)
        log_button.pack()

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu, width=10)
        back_button.pack()

    # TODO Rename this here and in `log_hours_menu`
    def _extracted_from_log_hours_menu_6(self, text):
        tk.Label(self.root, text=text).pack()
        result = tk.Entry(self.root)
        result.pack()

        return result

    def save_volunteer_hours(self, volunteer_id, date, hours_worked, description):
        if not self.validate_not_empty(volunteer_id, date, hours_worked, description):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            hours_worked = float(hours_worked)
        except ValueError:
            messagebox.showerror("Error", "Hours worked must be a number!")
            return

        volunteer_hours = VolunteerHours(date, hours_worked, description)
        self.db_handler.add_volunteer_hours(volunteer_id, volunteer_hours)
        messagebox.showinfo("Success", "Volunteer hours logged successfully!")
        self.create_main_menu()

    def generate_reports_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Reports", font=('Helvetica', 16, 'bold')).pack(pady=20)

        hours_report_button = tk.Button(self.root, text="Generate Hours Report", command=self.display_hours_report, width=20)
        hours_report_button.pack(pady=10)

        summary_report_button = tk.Button(self.root, text="Generate Volunteer Summary", command=self.display_volunteer_summary, width=20)
        summary_report_button.pack(pady=10)

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.create_main_menu, width=20)
        back_button.pack(pady=10)

    def display_hours_report(self):
        report = self.db_handler.generate_hours_report()
        self.clear_frame()
        tk.Label(self.root, text=report).pack(pady=20)

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.generate_reports_menu, width=10)
        back_button.pack(pady=10)

    def display_volunteer_summary(self):
        report = self.db_handler.generate_volunteer_summary()
        self.clear_frame()
        tk.Label(self.root, text=report).pack(pady=20)

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.generate_reports_menu, width=10)
        back_button.pack(pady=10)

    def exit_app(self):
        self.root.destroy()

    def validate_not_empty(self, *args):
        return all(arg.strip() for arg in args)

    def validate_email(self, email):
        return '@' in email and '.' in email

def main():
    root = tk.Tk()
    app = VolunteerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


