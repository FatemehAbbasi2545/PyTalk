from tkinter import Tk, Label, Entry, Button, messagebox
from Ui.Frames.base_frame import BaseFrame
from Ui.ui_service import UiService
from Business.user_business_service import UserBusinessService

class ChangePasswordFrame(BaseFrame):
    def __init__(self, container: Tk, ui_service: UiService, user_business_service: UserBusinessService, logout_fn):      
        super().__init__(container, ui_service) 
        
        self.user_business_service = user_business_service    
        self.logout_fn = logout_fn         

    def create_labels(self):
        self.password_label = Label(self, text="Password:", font=('Segoe UI', 11), bg='#F0F0F0')
        self.password_label.grid(row=0, column=0, padx=10, pady=10)

        self.confirm_password_label = Label(self, text="Confirm password:", font=('Segoe UI', 11), bg='#F0F0F0')
        self.confirm_password_label.grid(row=1, column=0, padx=10, pady=10)

    def create_entries(self):
        self.password_entry = Entry(self, show="*", font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.password_entry.grid(row=0, column=1, padx=10, pady=10)

        self.confirm_password_entry = Entry(self, show="*", font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.confirm_password_entry.grid(row=1, column=1, padx=10, pady=10)

    def create_buttons(self):
        self.submit_button = Button(self, text="Submit", command=self.submit, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.submit_button.grid(row=2, column=1, padx=10, pady=10)

    def submit(self):
        if not self.user_business_service.current_user:
            return
        
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return False
        if password != confirm_password:
            messagebox.showerror("Error", "Password and confirm password must be the same.")
            return 
        
        response = self.user_business_service.change_password(password)

        if not response.success:
            messagebox.showerror(title="Change Password Failed!", message=response.message)
        else:
            messagebox.showinfo('Success', response.message)            
            self.ui_service.change_password_window_destroy()
            self.logout_fn()