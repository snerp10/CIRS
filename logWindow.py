from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from dashWindow import *
from adminDashWindow import *
import mysql.connector
from mysql.connector import Error

    
class log:
    # main window
    def __init__(self):
        self.window = Tk()
        self.window.title("Log In Account")
        self.x = (self.window.winfo_screenwidth() // 2) - (720 // 2)
        self.y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry('{}x{}+{}+{}'.format(720, 500, self.x, self.y))
        self.username = None
        
    # window title
        self.title = Label(self.window,
                           text = "Crime Incident Reporting System",
                           font = ('Comic Sans MS', 20, 'bold'),
                           padx = 0,
                           pady = 20)
        self.title.pack()

    # window logFrame
        self.frame = Frame(self.window)
        self.frame.config(border = 10, highlightbackground= "black", highlightcolor= "black", highlightthickness= 2)
        self.frame.pack()

    # frame userLabel
        self.userName = Label(self.frame,
                              text = 'Username',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 50,
                              pady = 30)
        self.userName.grid(row = 1, column = 0)

    # frame userEntry
        self.userEntry = Entry(self.frame,
                               font = ('Arial',14))
        self.userEntry.grid(row = 1, column = 1)

    # frame passLabel
        self.password = Label(self.frame,
                              text = 'Password',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 50,
                              pady = 30)
        self.password.grid(row = 2, column = 0)

    # frame passEntry
        self.passEntry = Entry(self.frame,
                               font = ('Arial',14 ),
                               show = '*')
        self.passEntry.grid(row = 2, column = 1)

    # frame submitButton

        self.subButton = Button(self.frame,
                                text = 'Login',
                                command = self.login,
                                width = 20,
                                font = ('Comic Sans MS',12),
                                foreground = 'white',
                                background = '#333333')
        self.subButton.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.subButton.grid(row = 3, column = 1)

    # frame cancelButton

        self.cancelButton = Button(self.frame,
                                text = 'Cancel',
                                command = self.cancel,
                                width = 10,
                                font = ('Comic Sans MS',12),
                                foreground = 'white',
                                background = '#333333')
        self.cancelButton.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.cancelButton.grid(row = 3, column = 0)

    # frame 2
    
        self.frame2 = Frame(self.frame)
        self.frame2.config(border = 10, highlightbackground= "black", highlightcolor= "black", highlightthickness= 2)
        self.frame2.grid(row = 4, columnspan=2, column = 0)
        
        self.dontHave = Label(self.frame2,
                              text = 'Dont have an account?',
                              font = ('Comic Sans MS',15 ,'bold'),
                              padx = 25,
                              pady = 0)
        self.dontHave.grid(row = 0, column = 0)
        
        self.signIn = Button(self.frame2,
                                text = 'Sign in',
                                command = self.signIn,
                                width = 10,
                                font = ('Comic Sans MS',12),
                                foreground = 'white',
                                background = '#333333')
        self.signIn.config(border=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.signIn.grid(row = 0, column = 1)

        self.window.mainloop()

    # button functions

    def login(self):

        user_entry = str(self.userEntry.get())
        pass_entry = str(self.passEntry.get())

    # Connect to the database
        try:
            connection = mysql.connector.connect(
                host='localhost',      
                user='root',   
                password='',  
                database='crime_incidents_db'  
            )
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (user_entry, pass_entry))
            user = cursor.fetchone()
            
            
            if user:
                self.username = user['username']
                print(f"Logged in user: {self.username}")
                messagebox.showinfo("Login Success", f"Welcome, {user['name']}!")
                self.window.destroy() 
                
                if user['username'] == 'admin':  
                    admin_dash(self.username)
                    return self.username
                else:
                    dash(self.username) 
                    return self.username
                

            # Check if the user is admin
                
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
                self.userEntry.delete(0, END)
                self.passEntry.delete(0, END)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return
        finally:
            if connection:
                cursor.close()
                connection.close()
             
# sign in function

    def signIn(self):
        self.window.destroy()
        from signWindow import sign
        sign()

    def cancel(self):
        
        self.userEntry.delete(0, END)
        self.passEntry.delete(0, END)

if __name__ == "__main__":
    log()
     