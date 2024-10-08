from tkinter import *
from tkinter import messagebox, font
from tkinter import ttk
import tkinter as tk
from crime_incident import CrimeIncident, CrimeIncidentManager
import mysql.connector
from mysql.connector import Error

class admin_dash:
    def __init__(self, username):
     # Initialize database
   
        db_config = {
            'host': 'localhost',
            'user': 'root',  # Update with your DB username
            'password': '',  # Update with your DB password
            'database': 'crime_incidents_db'  # Update with your DB name
        }
        self.manager = CrimeIncidentManager(db_config=db_config)

        self.current_user = username

    # Main window for the dashboard
        self.dashWindow = Tk()
        self.dashWindow.title("Crime Incident Reporting System")
        self.x = (self.dashWindow.winfo_screenwidth() // 2) - (720 // 2)
        self.y = (self.dashWindow.winfo_screenheight() // 2) - (500 // 2)
        self.dashWindow.geometry('{}x{}+{}+{}'.format(750, 500, self.x, self.y))

        
        self.curr_user()
        
        self.userLabel = Label(self.dashWindow,
                               text=f"Welcome Bossing Admin",
                               font=("Comic Sans MS", 12))
        self.userLabel.pack(pady=0)
    # Log out Button

        self.logOut = Button(self.dashWindow, text="Log out",
                                   command=self.logOut,
                                   width=10,
                                   background = "#333333",
                                   foreground= "#FFA07A")
        self.logOut.config(font=("Comic Sans MS", 12))
        self.logOut.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.logOut.pack(anchor='e')
        
    # Title
        self.title = Label(self.dashWindow,
                           text="Crime Incident Reporting System",
                           font=("Comic Sans MS", 18, "bold"),
                           pady=20)
        self.title.pack()
        

    # Frame for the form and buttons
        self.formFrame = Frame(self.dashWindow)
        self.formFrame.config(border=10, highlightbackground="black", highlightcolor="black", highlightthickness=3)
        self.formFrame.pack()


    # descriptionLabel

        self.descLabel = Label(self.formFrame,
                            text="Description")
        self.descLabel.config(font=("Comic Sans MS", 12))
        self.descLabel.grid(row=1, column=0, padx=10, pady=5)

    # descriptionEntry

        self.description = Entry(self.formFrame)
        self.description.config(font=("Arial", 12),
                                width=30)
        self.description.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

    # locationLabel

        self.locLabel = Label(self.formFrame,
                            text="Location")
        self.locLabel.config(font=("Comic Sans MS", 12))
        self.locLabel.grid(row=2, column=0, padx=10, pady=5)

    # locationEntry

        self.location = Entry(self.formFrame)
        self.location.config(font=("Arial", 12),
                             width=30)
        self.location.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

    # dateLabel

        self.dateLabel = Label(self.formFrame,
                             text="Date")
        self.dateLabel.config(font=("Comic Sans MS", 12))
        self.dateLabel.grid(row=3, column=0, padx=10, pady=5)

    # dateEntry

        self.date = Entry(self.formFrame)
        self.date.config(font=("Arial", 12),
                         width=30)
        self.date.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

    # Buttons for CRUD operations

        self.addButton = Button(self.formFrame, text="Add",
                                command=self.create,
                                width=10,
                                background = "#333333",
                                foreground= "#FFFFFF")
        self.addButton.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.addButton.config(font=("Comic Sans MS", 12))
        self.addButton.grid(row=4, column=0, pady=10, padx = 30)

        self.updateButton = Button(self.formFrame, text="Update",
                                   command=self.update,
                                   width=10,
                                   background = "#333333",
                                   foreground= "#FFFFFF")
        self.updateButton.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.updateButton.config(font=("Comic Sans MS", 12))
        self.updateButton.grid(row=4, column=1, pady=10, padx = 30)

        self.deleteButton = Button(self.formFrame, text="Delete",
                                   command=self.delete,
                                   width=10,
                                   background = "#333333",
                                   foreground= "#FFA07A")
        self.deleteButton.config(font=("Comic Sans MS", 12))
        self.deleteButton.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.deleteButton.grid(row=4, column=2, pady=10, padx = 30)

        self.deleteAllButton = Button(self.formFrame, text="Delete All",
                                      command=self.deleteAll,
                                      width=10,
                                      background = "#333333",
                                      foreground = "#FFA07A")
        self.deleteAllButton.config(font=("Comic Sans MS", 12))
        self.deleteAllButton.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.deleteAllButton.grid(row=4, column=3, pady=10, padx = 30)

    # Treeview 
        self.tree = ttk.Treeview(self.dashWindow,
                                 columns=("ID", "Description", "Location", "Date"),
                                 show='headings')
        self.tree.config(height = 50)
        self.tree.column("ID", width = 50, anchor = 'center')
        self.tree.column("Description", width=200, anchor='center')
        self.tree.column("Location", width=200, anchor='center')
        self.tree.column("Date", width=100, anchor='center')

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Comic Sans MS', 12), foreground='black')
        style.configure("Treeview", font=('Arial', 10))

        style.map("Treeview",
              background=[("selected", "#FFA07A")],  # Orange Red highlight when clicked
              foreground=[("selected", "black")])  # White text when clicked

        self.tree.tag_configure('evenrow', background="lightgreen")
        self.tree.heading("ID", text="Incident ID")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Date", text="Date")
        self.tree.pack(pady = 20, expand = False, fill = 'both')

    #load functions
    
        self.load_data()
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)  # Bind selection event
        self.dashWindow.mainloop()

    # Functions
    
    def curr_user(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',      
                user='root',   
                password='',  
                database='crime_incidents_db'  
            )
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM users WHERE username = %s "
            cursor.execute(query, (self.current_user,))
            user = cursor.fetchone()
            self.current_user = user['name']
            
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()   
        
    def logOut(self):
        
        self.dashWindow.destroy()
        print(f"Balik balik boss {self.current_user}")
        from logWindow import log 
        log() 
    # Create a new crime report
    
    def create(self):
        
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to add incident?")
            
        if confirm:
            description = self.description.get()
            location = self.location.get()
            date = self.date.get()
            reporter = "Admin"

            if description and location and date:
                self.manager.add_incident(description, location, date, reporter)
                self.clear_tree()
                self.load_data()
                self.clear_form()
                
                messagebox.showinfo("Added","Incident has been added.")
            else:
                messagebox.showwarning("Input Error", "Please fill out all fields!")
        else:
            messagebox.showinfo("Cancelled", "Addition cancelled.")

    # Update an existing crime report
    
    def update(self):
        
        selected_item = self.tree.selection()
        if selected_item:
            selected_id = self.tree.item(selected_item, 'values')[0]

            confirm = messagebox.askyesno("Confirm", "Are you sure you want to update incident?")
            
            if confirm:
                updated_description = self.description.get()
                updated_location = self.location.get()
                updated_date = self.date.get()

            if updated_description and updated_location and updated_date:
                updated_incident = CrimeIncident(
                    selected_id,
                    updated_description,
                    updated_location,
                    updated_date,
                    self.current_user   
                )

                if self.manager.update_incident(selected_id, updated_incident):
                    self.clear_tree()
                    self.load_data()
                    self.clear_form()
                else:
                    messagebox.showwarning("Error", "Incident not found!")
                

                messagebox.showinfo("Updated","Incident has been updated.")
                
            else:
                messagebox.showinfo("Cancelled", "Deletion cancelled.")
        else:
            messagebox.showwarning("Selection Error", "Please select an incident to update!")

    # Delete a crime report
    
    def delete(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_id = self.tree.item(selected_item, 'values')[0]
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete incident?")
            
            if confirm:

                self.manager.delete_incident_from_db(selected_id)
                self.clear_tree()
                self.load_data()
                self.clear_form()

                messagebox.showinfo("Deleted","Incident has been deleted.")
                
            else:
                messagebox.showinfo("Cancelled", "Deletion cancelled.")
        else:
            messagebox.showwarning("Selection Error", "Please select an incident to delete!")
            
    # Delete all a crime incident
    
    def deleteAll(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all incidents?")
        if confirm:

            self.manager.delete_all_incidents_from_db()
            self.clear_tree()
            self.load_data()
            self.clear_form()

            messagebox.showinfo("Deleted", "All incidents have been deleted.")
        else:
            messagebox.showinfo("Cancelled", "Deletion cancelled.")

    # Clear the tree view
    
    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    # Load existing crime data in tree view
    
    def load_data(self):
        self.clear_tree()
        incidents = self.manager.get_all_incidents()

        for incident in incidents:
            self.tree.insert("", tk.END,    
                             values=(incident.incident_id, incident.description, incident.location, incident.date))

    # Clear the form after creating or updating
    # Function
    
    def clear_form(self):
        self.description.delete(0, END)
        self.location.delete(0, END)
        self.date.delete(0, END)
        
    # If selected = show to entry
    
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            selected_id = self.tree.item(selected_item, 'values')[0]
            incident = self.manager.get_incident_by_id(selected_id)
            if incident:
                self.description.delete(0, END)
                self.description.insert(0, incident.description)
                self.location.delete(0, END)
                self.location.insert(0, incident.location)
                self.date.delete(0, END)
                self.date.insert(0, incident.date)

if __name__ == "__main__":
    admin_dash()
