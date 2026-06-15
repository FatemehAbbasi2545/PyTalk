from tkinter import Tk, Button, Toplevel
from Ui.Frames.base_frame import BaseFrame
from Ui.Frames.add_contact_frame import AddContactFrame
from Ui.Frames.block_contacts_manager_frame import BlockContactsManagerFrame
from Ui.Frames.change_password import ChangePasswordFrame
from Business.user_business_service import UserBusinessService
from Business.contact_business_service import ContactBusinessService
from Ui.ui_service import UiService

class Navbar(BaseFrame):
    def __init__(self, container: Tk, ui_service: UiService, user_business_service: UserBusinessService, 
                 contact_business_service: ContactBusinessService, update_contacts_fn, load_contacts_fn, logout_fn):
        super().__init__(container, ui_service)
        self.user_business_service = user_business_service        
        self.contact_business_service = contact_business_service

        self.update_contacts_fn = update_contacts_fn 
        self.load_contacts_fn = load_contacts_fn
        self.logout_fn = logout_fn

        self.add_contact_window = None
        self.block_contacts_manager_window = None
        self.change_password_window = None

        self["bg"] = '#e3e3e3'

    def create_buttons(self):
        self.add_contact_button = Button(self, text="Add Contact", command=self.open_add_contact_window, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.add_contact_button.grid(row=0, column=1, padx=20, pady=20, sticky='w')

        self.block_contacts_button = Button(self, text="Manage Block Contacts", command=self.open_block_contacts_manager_window, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.block_contacts_button.grid(row=0, column=2, padx=20, pady=20, sticky='w')

        self.change_password_button = Button(self, text="Change Password", command=self.change_password, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.change_password_button.grid(row=0, column=3, padx=20, pady=20, sticky='w')

        self.logout_button = Button(self, text="Logout", command=self.logout, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.logout_button.grid(row=0, column=4, padx=20, pady=20, sticky='w')

    def open_add_contact_window(self):
        if self.add_contact_window is None or not self.add_contact_window.winfo_exists():
            self.add_contact_window = Toplevel(self.master)
            self.add_contact_window.title("Add Contact")
            self.add_contact_window.geometry("500x200")

            self.ui_service.set_add_contact_container_instance(self.add_contact_window)

            self.add_contact_frame = AddContactFrame(self.add_contact_window, 
                                                self.ui_service,
                                                self.user_business_service, 
                                                self.contact_business_service,
                                                update_contacts_fn=self.update_contacts_fn)             
            self.add_contact_frame.pack(expand=True)

    def open_block_contacts_manager_window(self):
        if self.block_contacts_manager_window is None or not self.block_contacts_manager_window.winfo_exists():
            self.block_contacts_manager_window = Toplevel(self.master)
            self.block_contacts_manager_window.title("Block Contacts Manager")
            self.block_contacts_manager_window.geometry("400x600")

            self.ui_service.set_block_contacts_manager_container_instance(self.block_contacts_manager_window)

            self.block_contacts_manager_frame = BlockContactsManagerFrame(self.block_contacts_manager_window, 
                                                    self.ui_service, 
                                                    self.contact_business_service,
                                                    load_contacts_fn=self.load_contacts_fn)             
            self.block_contacts_manager_frame.pack(expand=True)

    def change_password(self):
        if self.change_password_window is None or not self.change_password_window.winfo_exists():
            self.change_password_window = Toplevel(self.master)
            self.change_password_window.title("Change Password")
            self.change_password_window.geometry("500x200")

            self.ui_service.set_change_password_window_instance(self.change_password_window)

            self.block_contacts_manager_frame = ChangePasswordFrame(self.change_password_window,
                                                    self.ui_service, 
                                                    self.user_business_service,
                                                    logout_fn=self.logout)             
            self.block_contacts_manager_frame.pack(expand=True)


    def logout(self):        
        self.logout_fn()
