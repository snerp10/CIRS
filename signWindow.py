import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import messagebox
from tkinter import ttk




class sign:
    def __init__(self):
        
        self.window = Tk()
        self.window.title("Register Account")
        self.x = (self.window.winfo_screenwidth() // 2) - (720 // 2)
        self.y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry('{}x{}+{}+{}'.format(720, 700, self.x, self.y))
        
    #window title
      
        self.title = Label(self.window,
                           text = "Crime Incident Reporting System",
                           font = ('Comic Sans MS', 20, 'bold'),
                           padx = 0,
                           pady = 25)
        self.title.pack()
        
    #window frame
        
        self.frame = Frame(self.window)
        self.frame.config(border = 10, highlightbackground= "black", highlightcolor= "black", highlightthickness= 2)
        self.frame.pack()
        
        self.name = Label(self.frame,
                              text = 'Full Name',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 0,
                              pady = 10)
        self.name.grid(row = 1, column = 0)
        
        self.nameEntry = Entry(self.frame,
                               font = ('Arial',14))
        self.nameEntry.grid(row = 1, column = 1)
        
        self.age = Label(self.frame,
                              text = 'Age',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 0,
                              pady = 10)
        self.age.grid(row = 2, column = 0)
        
        self.ageEntry = Entry(self.frame,
                               font = ('Arial',14))
        self.ageEntry.grid(row = 2, column = 1)
        
        self.address = Label(self.frame,
                              text = 'Address',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 0,
                              pady = 10)
        self.address.grid(row = 3, column = 0)
        
        self.addressEntry = Entry(self.frame,
                               font = ('Arial',14))
        self.addressEntry.grid(row = 3, column = 1)
        
        self.email = Label(self.frame,
                              text = 'Email',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 0,
                              pady = 10)
        self.email.grid(row = 4, column = 0)
        
        self.emailEntry = Entry(self.frame,
                               font = ('Arial',14))
        self.emailEntry.grid(row = 4, column = 1)
        
        self.username = Label(self.frame,
                              text = 'Username',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 0,
                              pady = 10)
        self.username.grid(row = 5, column = 0)
        
        self.usernameEntry = Entry(self.frame,
                               font = ('Arial',14))
        self.usernameEntry.grid(row = 5, column = 1)
        
        self.password = Label(self.frame,
                              text = 'Password',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 0,
                              pady = 10)
        self.password.grid(row = 6, column = 0)
        
        self.passEntry = Entry(self.frame,
                               font = ('Arial',14 ),
                               show = '*',)
        self.passEntry.grid(row = 6, column = 1)
        
        self.confirmPassword = Label(self.frame,
                              text = 'Confirm Password',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 0,
                              pady = 10)
        self.confirmPassword.grid(row = 7, column = 0)
        
        self.conPassEntry = Entry(self.frame,
                               font = ('Arial',14 ),
                               show = '*')
        self.conPassEntry.grid(row = 7, column = 1)
        
        self.cancel = Button(self.frame,
                                text = 'Cancel',
                                command = self.logIn,
                                width = 10,
                                font = ('Comic Sans MS',12),
                                foreground = 'white',
                                background = '#333333')
        self.cancel.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.cancel.grid(row = 8, column = 0)
        
        self.sign_in = Button(self.frame,
                                text = 'Sign in',
                                command = self.signIn,
                                width = 20,
                                font = ('Comic Sans MS',12),
                                foreground = 'white',
                                background = '#333333')
        self.sign_in.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.sign_in.grid(row = 8, column = 1)
        
        self.frame2 = Frame(self.frame)
        self.frame2.config(border = 10, highlightbackground= "black", highlightcolor= "black", highlightthickness= 2)
        
        self.frame2.grid(row = 9, columnspan=2, column = 0)
        
        self.haveAcc = Label(self.frame2,
                              text = 'Already have an account?',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 0,
                              pady = 0)
        self.haveAcc.grid(row = 0, column = 0)
        
        self.logIn = Button(self.frame2,
                                text = 'Log in',
                                command = self.logIn,
                                width = 10,
                                font = ('Comic Sans MS',12),
                                foreground = 'white',
                                background = '#333333')
        self.logIn.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.logIn.grid(row = 0, column = 1)
        
        self.window.mainloop()
        
# Funtions

    def signIn(self):
        full_name = self.nameEntry.get()
        age = self.ageEntry.get()
        address = self.addressEntry.get()
        email = self.emailEntry.get()
        username = self.usernameEntry.get()
        password = self.passEntry.get()
        conPassword = self.conPassEntry.get()
        
        
        if not (full_name and age and address and email and username and password and conPassword):
            messagebox.showerror("Invalid Input", "Please fill out all fields!")
            return

    
        if not age.isdigit():  # Check if age is numeric
            messagebox.showerror("Invalid Age", "Age must be a number.")
            self.ageEntry.delete(0, END)
            return

        age = int(age)  # Now safe to convert
        if age < 18:
            messagebox.showerror("Invalid Age", "You must be 18+ years old.")
            self.ageEntry.delete(0, END)
            return

    
        if '@' not in email or '.' not in email:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            self.emailEntry.delete(0, END)
            return

    
        if password != conPassword:
            messagebox.showerror("Password Mismatch", "Passwords do not match.")
            self.passEntry.delete(0, END)
            self.conPassEntry.delete(0, END)
            return
        
        num_user = self.next_user_id()
        
        if num_user is None: 
            messagebox.showerror("Error", "Could not retrieve the next user ID.")
            return
        
        self.add_user_to_db(full_name, age, address, email, username, password, num_user)

    def logIn(self):
        
        self.window.destroy()
        from logWindow import log 
        log() 
        
    def cancel(self):
        print()
        
    def add_user_to_db(self, name, age, address, email, username, password, num_user):
        
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',  
                password='',  
                database='crime_incidents_db'
            )
            cursor = conn.cursor()

            # Check 
            
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                messagebox.showerror("Username Taken", "This username is already taken. Please choose another one.")
                self.usernameEntry.delete(0, END)
                return

            # Insert the new user 
    
            query = "INSERT INTO users (name, age, address, email, username, password, num_user) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, age, address, email, username, password, num_user))
            conn.commit()

            messagebox.showinfo("Success", "Account registered successfully!")
            self.window.destroy()
            self.log_in() 

        except Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                
    def next_user_id(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',  
                password='',  
                database='crime_incidents_db'
            )
            cursor = conn.cursor()
            query = "SELECT MAX(CAST(num_user AS UNSIGNED)) FROM users"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

            if result[0] is None:
                return "1" 

            next_id = int(result[0]) + 1
            return next_id
    
        except Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

        finally:
            if conn.is_connected():
                conn.close()

    
    def log_in(self):
        from logWindow import log 
        log()



if __name__ == "__main__":
    sign()