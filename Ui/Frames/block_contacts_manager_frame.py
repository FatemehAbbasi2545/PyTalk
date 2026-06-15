from tkinter import Tk, Label, Button, messagebox, Checkbutton
from Ui.Frames.base_frame import BaseFrame
from Ui.ui_service import UiService
from Business.contact_business_service import ContactBusinessService
from Common.Entities.contact import ContactInfo
from Common.Enums.contact_status import ContactStatus

class BlockContactsManagerFrame(BaseFrame):
    def __init__(self, container: Tk, ui_service: UiService, contact_business_service: ContactBusinessService,
                load_contacts_fn):      
        super().__init__(container, ui_service)       
        self.contact_business_service = contact_business_service
        self.load_contacts_fn = load_contacts_fn

        self.contacts: list[ContactInfo] = contact_business_service.current_user_contacts
        self.build_contact_list() 

        self.blocked_contacts = []
        self.unblocked_contacts = []

        self.create_submit_button()

    def build_contact_list(self):
        Label(  
            self, text="Contacts", font=("Segoe UI", 11, "bold"),  
            bg="#f0f0f0", fg="#333"  
        ).grid(row=0, column=0, pady=10)

        contacts_count = len(self.contacts)
        for i in range(contacts_count):
            c = self.contacts[i]
            check_button = Checkbutton(self, text=f'{c.audience_name}',
                                    command=lambda x=c: self.on_checkbox_change(x))
            check_button.grid(row=i+1, column=0, pady=5)
            if c.status == ContactStatus.blocked.value:
                check_button.select()

    def on_checkbox_change(self, contact: ContactInfo):
        if contact.status == 1:
            if contact.contact_id in self.unblocked_contacts:
                self.unblocked_contacts.remove(contact.contact_id)
            self.blocked_contacts.append(contact.contact_id)
            return
        
        if contact.status == 2:
            if contact.contact_id in self.blocked_contacts:
                self.blocked_contacts.remove(contact.contact_id)
            self.unblocked_contacts.append(contact.contact_id)

    def create_submit_button(self):
        self.submit_button = Button(self, text="Submit", command=self.submit, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.submit_button.grid(row=len(self.contacts)+1, column=0, pady=10)

    def submit(self):
        response = self.contact_business_service.change_status(self.blocked_contacts, self.unblocked_contacts)

        if not response.success:
            messagebox.showerror(title="Internal server Error!", message=response.message)              
        else:
            messagebox.showinfo('Success', 'Operation successful')
            self.load_contacts_fn()
            self.ui_service.block_contacts_manager_container_destroy()

            








       