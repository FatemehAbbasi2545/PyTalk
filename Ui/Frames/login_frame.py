import random
import string
from tkinter import Tk, Frame, Label, Entry, Button, messagebox, constants
from Ui.Frames.base_frame import BaseFrame
from Business.user_business_service import UserBusinessService
from Ui.ui_service import UiService

class LoginFrame(BaseFrame):
    def __init__(self, container: Tk, ui_service: UiService, user_business_service: UserBusinessService, 
                show_register_frame_fn, show_navbar_fn, show_contact_panel_fn):      
        super().__init__(container, ui_service) 
        self.user_business_service = user_business_service

        self.show_register_frame_fn = show_register_frame_fn
        self.show_navbar_fn = show_navbar_fn
        self.show_contact_panel_fn = show_contact_panel_fn
        
        self.create_user_info_section()
        self.generate_captcha_text(5)
        self.create_captcha_section()
        self.create_last_section()

    def create_user_info_section(self):
        self.user_info_frame = Frame(self)
        self.user_info_frame.pack(fill="x", padx=10, pady=5)

        self.user_name_label = Label(self.user_info_frame, text="User Name:", font=("Segoe UI", 11), bg="#F0F0F0")
        self.user_name_label.grid(row=0, column=0, padx=10, pady=10)

        self.user_name_entry = Entry(self.user_info_frame, font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.user_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = Label(self.user_info_frame, text="Password:", font=("Segoe UI", 11), bg="#F0F0F0")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = Entry(self.user_info_frame, show="*", font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)     

    def create_captcha_section(self):
        self.captcha_frame = Frame(self)
        self.captcha_frame.pack(fill="x", padx=10, pady=5)

        self.refresh_captcha_btn = Button(self.captcha_frame, text="Refresh", command=self.refresh_captcha, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.refresh_captcha_btn.grid(row=0, column=0, padx=5)

        self.captcha_label = Label(self.captcha_frame, text=self.captcha_text, font=("Segoe UI", 11, "bold"), bg="#F0F0F0", fg="blue", relief="solid")
        self.captcha_label.grid(row=0, column=1, padx=5)

        self.captcha_entry = Entry(self.captcha_frame, font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.captcha_entry.grid(row=0, column=2, padx=5)

    def create_last_section(self):
        self.last_frame = Frame(self)
        self.last_frame.pack(fill="x", padx=10, pady=10)

        self.login_button = Button(self.last_frame, text="Login", command=self.login, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.login_button.pack(padx=10, pady=5)

        self.sign_up_label = Label(self.last_frame, text="I want to sign up", font=("Segoe UI", 11), bg="#F0F0F0", fg="blue", cursor="hand2")
        self.sign_up_label.pack(pady=5)
        self.sign_up_label.bind("<Button-1>", lambda e: self.sign_up())          

    def generate_captcha_text(self, length=5):        
        """تولید متن تصادفی برای کپچا"""
        chars = string.ascii_uppercase + string.digits # or chars = string.digits
        # حذف کاراکترهای گیج‌کننده مثل 0, O, I, L
        chars = chars.replace('O', '').replace('0', '').replace('I', '').replace('L', '')
        self.captcha_text = ''.join(random.choices(chars, k=length))

    def refresh_captcha(self):
        self.generate_captcha_text()
        self.captcha_label.config(text=self.captcha_text)

    def login(self):
        user_name = self.user_name_entry.get()        
        password = self.password_entry.get()
        user_captcha = self.captcha_entry.get()

        if not user_name or not password or not user_captcha:
            messagebox.showerror("Error", "All fields are required.")
            return False
        
        user_captcha = user_captcha.strip()
        if user_captcha.upper() != self.captcha_text.upper():
            messagebox.showerror("Error", "Incorrect security code.")
            return False
        
        response = self.user_business_service.login(user_name, password)

        if not response.success:
            messagebox.showerror(title="Login Failed!", message=response.message)              
        else:
            self.clear_user_inputs()  
            self.pack_forget()   
            self.show_navbar_fn()
            self.show_contact_panel_fn()

    def sign_up(self):
        self.clear_user_inputs()  
        self.pack_forget()
        self.show_register_frame_fn()

    def clear_user_inputs(self):
        self.user_name_entry.delete(0, constants.END)
        self.password_entry.delete(0, constants.END)
        self.captcha_entry.delete(0, constants.END)
         

        
 

    

       