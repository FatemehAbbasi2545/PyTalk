from tkinter import Tk, Label, Entry, Button, messagebox, constants
from Business.user_business_service import UserBusinessService
from Common.Entities.user import User
from Ui.Frames.base_frame import BaseFrame
from Ui.ui_service import UiService

class RegisterFrame(BaseFrame):
    def __init__(self, container: Tk, ui_service: UiService, user_business_service: UserBusinessService, show_login_frame_fn):      
        super().__init__(container, ui_service)         
        self.user_business_service = user_business_service
        self.show_login_frame_fn = show_login_frame_fn

    def create_labels(self):
        self.name_label = Label(self, text="Name:", font=('Segoe UI', 11), bg='#F0F0F0')
        self.name_label.grid(row=0, column=0, padx=10, pady=10)

        self.user_name_label = Label(self, text="User name:", font=('Segoe UI', 11), bg='#F0F0F0')
        self.user_name_label.grid(row=1, column=0, padx=10, pady=10)

        self.mobile_phone_label = Label(self, text="Mobile phone:", font=('Segoe UI', 11), bg='#F0F0F0')
        self.mobile_phone_label.grid(row=2, column=0, padx=10, pady=10)

        self.password_label = Label(self, text="Password:", font=('Segoe UI', 11), bg='#F0F0F0')
        self.password_label.grid(row=3, column=0, padx=10, pady=10)

        self.confirm_password_label = Label(self, text="Confirm password:", font=('Segoe UI', 11), bg='#F0F0F0')
        self.confirm_password_label.grid(row=4, column=0, padx=10, pady=10)

        self.show_login_label = Label(self, text="Go to login page", font=("Segoe UI", 11), bg="#F0F0F0", fg="blue", cursor="hand2")
        self.show_login_label.grid(row=6, column=1, pady=10)
        self.show_login_label.bind("<Button-1>", lambda e: self.show_login_page())

    def create_entries(self):
        self.name_entry = Entry(self, font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.user_name_entry = Entry(self, font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.user_name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.mobile_phone_entry = Entry(self, font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.mobile_phone_entry.grid(row=2, column=1, padx=10, pady=10)

        self.password_entry = Entry(self, show="*", font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.password_entry.grid(row=3, column=1, padx=10, pady=10)

        self.confirm_password_entry = Entry(self, show="*", font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.confirm_password_entry.grid(row=4, column=1, padx=10, pady=10)

    def create_buttons(self):
        self.create_account_button = Button(self, text="Create Account", font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0, command=self.create_account)
        self.create_account_button.grid(row=5, column=1, pady=10)

    def create_account(self):
        name = self.name_entry.get()
        user_name = self.user_name_entry.get()
        mobile_phone = self.mobile_phone_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not name or not user_name or not mobile_phone or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return False
        if password != confirm_password:
            messagebox.showerror("Error", "Password and confirm password must be the same.")
            return 
        
        user = User(None, name, user_name, password, mobile_phone)
        response = self.user_business_service.register_user(user)

        if not response.success:
            messagebox.showerror(title="Create Account Failed!", message=response.message)
        else:
            messagebox.showinfo('Success', response.message)
            self.show_login_page()      

    def show_login_page(self):
        self.name_entry.delete(0, constants.END)
        self.user_name_entry.delete(0, constants.END)
        self.mobile_phone_entry.delete(0, constants.END)
        self.password_entry.delete(0, constants.END)
        self.confirm_password_entry.delete(0, constants.END)
        self.pack_forget()
        self.show_login_frame_fn()
        

        
 

    

       
