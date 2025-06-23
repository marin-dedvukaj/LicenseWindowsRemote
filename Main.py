from BackendDataMenagement import LicenseStorage
import tkinter as tk
from tkinter import messagebox, simpledialog

class LicenseManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("License Manager")
        self.storage = LicenseStorage("licenses")
        self.projects = self.storage.listProjects()
        print("Available Projects:", self.projects)
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=50, pady=50)

        tk.Button(self.main_frame, text="Get license", width=20, command=self.open_get_license).pack(pady=5)
        tk.Button(self.main_frame, text="Add License", width=20, command=self.open_add_license).pack(pady=5)
        tk.Button(self.main_frame, text="Create new project", width=20, command=self.open_create_project).pack(pady=5)

    def refresh_projects(self):
        self.projects = self.storage.listProjects()
    

    def open_get_license(self):
        self.refresh_projects()
        win = tk.Toplevel(self.master)
    
        win.title("Get License")
        tk.Label(win, text="Select Project:").pack(pady=5)
        project_var = tk.StringVar(win)
        if self.projects:
            project_var.set(self.projects[0])
        # Ensure at least one value is passed to OptionMenu
        dropdown_values = self.projects if self.projects else ["No Projects Available"]
        dropdown = tk.OptionMenu(win, project_var, *dropdown_values)
        dropdown.pack(pady=5)

        def fetch_license():
            project = project_var.get()
            license_key = self.storage.getLicense(project)
            license_entry = tk.Entry(win, width=40)
            # Ensure license_key is a string and handle None
            if license_key is None:
                license_entry.insert(0, "No license found")
            else:
                license_entry.insert(0, str(license_key))
            license_entry.config(state='readonly')
            license_entry.pack(pady=5)
            license_entry.focus_set()
            license_entry.selection_range(0, tk.END)
        
            def done_action():
                ask_status()
                win.destroy()
        
            tk.Button(win, text="Done", command=done_action).pack(pady=5)
            # Make the messagebox non-blocking by using after() to check status later
            def ask_status():
                result = messagebox.askyesno("License Status", "Did the license work?", parent=win)
                status = "Used" if result else "Expired"
                if license_key is not None:
                    self.storage.changeStatus(project, license_key, status)
                # Optionally, you can close the window or disable further prompts here

        tk.Button(win, text="Fetch License", command=fetch_license).pack(pady=10)

    def open_add_license(self):
        self.refresh_projects()
        win = tk.Toplevel(self.master)
        win.title("Add License")
        tk.Label(win, text="Select Project:").pack(pady=5)
        project_var = tk.StringVar(win)
        if self.projects:
            project_var.set(self.projects[0])
        dropdown = tk.OptionMenu(win, project_var, *self.projects)
        dropdown.pack(pady=5)
        tk.Label(win, text="License:").pack(pady=5)
        license_entry = tk.Entry(win, width=30)
        license_entry.pack(pady=5)

        def submit_license():
            project = project_var.get()
            license_key = license_entry.get()
            self.storage.AddLicenses(project, license_key)
            license_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "License added.")

        tk.Button(win, text="Submit", command=submit_license).pack(pady=10)

    def open_create_project(self):
        win = tk.Toplevel(self.master)
        win.title("Create New Project")
        tk.Label(win, text="Project Name:").pack(pady=5)
        project_entry = tk.Entry(win, width=30)
        project_entry.pack(pady=5)

        def submit_project():
            project_name = project_entry.get()
            if project_name:
                self.storage.newProject(project_name)
                self.refresh_projects()
                messagebox.showinfo("Success", "Project created.")
                win.destroy()

        tk.Button(win, text="Submit", command=submit_project).pack(pady=10)
        win.transient(self.master)
        win.grab_set()
        project_entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = LicenseManagerApp(root)
    root.mainloop()