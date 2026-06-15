from tkinter import Tk, Label, Entry, Button, messagebox
from Ui.Frames.base_frame import BaseFrame
from Ui.ui_service import UiService
from Business.user_business_service import UserBusinessService
from Business.contact_business_service import ContactBusinessService

class AddContactFrame(BaseFrame):
    def __init__(self, container: Tk, ui_service: UiService, user_business_service: UserBusinessService, 
                contact_business_service: ContactBusinessService, update_contacts_fn):      
        super().__init__(container, ui_service) 
        
        self.user_business_service = user_business_service        
        self.contact_business_service = contact_business_service 

        self.update_contacts_fn = update_contacts_fn     

    def create_labels(self):
        self.contact_number_label = Label(self, text="Audience phone number:", font=("Segoe UI", 11), bg="#F0F0F0")
        self.contact_number_label.grid(row=0, column=0, padx=10, pady=10)

    def create_entries(self):
        self.contact_number_entry = Entry(self, font=('Segoe UI', 11), bg='#FFFFFF', relief='solid', borderwidth=1)
        self.contact_number_entry.grid(row=0, column=1, padx=10, pady=10)

    def create_buttons(self):
        self.add_contact_button = Button(self, text="Add Contact", command=self.add_contact, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.add_contact_button.grid(row=1, column=1, padx=10, pady=10)

    def add_contact(self):
        contact_number = self.contact_number_entry.get()        

        if not contact_number:
            messagebox.showerror("Error", "Please enter the contact's phone number.")
            return
        
        if not self.user_business_service.current_user:
            return
        
        response = self.contact_business_service.add_contact(self.user_business_service.current_user.user_id, contact_number)

        if not response.success:
            messagebox.showerror(title="Add Contact Failed!", message=response.message)              
        else:
            messagebox.showinfo('Success', 'Operation successful')
            self.update_contacts_fn(response.data)
            self.ui_service.add_contact_container_destroy()