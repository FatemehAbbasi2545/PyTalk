from tkinter import Tk, Label, Listbox, Scrollbar, constants
from Ui.Frames.base_frame import BaseFrame
from Business.user_business_service import UserBusinessService
from Business.contact_business_service import ContactBusinessService
from Business.message_business_service import MessageBusinessService
from Ui.Frames.chat_area_frame import ChatAreaFrame
from Common.Entities.contact import ContactInfo
from Ui.ui_service import UiService

class ContactPanel(BaseFrame):
    def __init__(self, container: Tk, ui_service: UiService, user_business_service: UserBusinessService, 
                contact_business_service: ContactBusinessService, message_business_service: MessageBusinessService,
                create_chat_area_frame_fn):
        super().__init__(container, ui_service)
        
        self.user_business_service = user_business_service        
        self.contact_business_service = contact_business_service  
        self.message_business_service = message_business_service  

        self.create_chat_area_frame_fn = create_chat_area_frame_fn

        self.create_list_box()
        self.create_scrollbar()

        self.chat_area_frame = None     

    def create_labels(self):       
        self.user_name_label = Label(self, text='Contacts', font=("Segoe UI", 11), bg="#F0F0F0")
        self.user_name_label.pack(pady=(10, 5))        

    def create_list_box(self):
        self.contact_list = Listbox(
            self, 
            font=("Segoe UI", 12, "bold"),
            bg="white", 
            fg="black",
            selectmode='single', # هر بار فقط یکی انتخاب شود
            exportselection=False,
            selectbackground="#0078d4",
            relief=constants.FLAT,
            activestyle='dotbox', # ظاهر بهتر هنگام انتخاب
            height=15, # تعداد اولیه سطرهای قابل مشاهده
            width=20
        )
        self.contact_list.pack(fill='both', expand=True, padx=1, pady=1)
        self.contact_list.bind('<<ListboxSelect>>', self.on_contact_select)

    def create_scrollbar(self):
        self.scrollbar = Scrollbar(self, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')

        # اتصال اسکرول بار به لیست
        self.contact_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.contact_list.yview)

    def update_user_name_label(self):
        text = "Contacts" if not self.user_business_service.current_user else f'Contacts of {self.user_business_service.current_user.user_name}:'  
        self.user_name_label.config(text=text)      

    def load_contacts(self):
        if not self.user_business_service.current_user:
            return
        response = self.contact_business_service.get_user_contacts(self.user_business_service.current_user.user_id)
        self.contacts: list[ContactInfo] = response.data
        active_contacts = list(filter(lambda x: x.status == 1, self.contacts))
        self.contact_list.delete(0, constants.END)
        for contact in active_contacts:
            self.contact_list.insert('end', contact.audience_name)

    def update_contacts(self, contact: ContactInfo):
        self.contacts.append(contact)
        self.contact_list.insert('end', contact.audience_name)

    def on_contact_select(self, event):
        # این تابع وقتی اجرا می‌شود که کاربر روی یک آیتم کلیک می‌کند
        selection = self.contact_list.curselection()
        if selection:            
            index = selection[0] # اندیس ایتم انتخاب شده
            selected_value = self.contact_list.get(index)
            result = list(filter(lambda x: x.audience_name == selected_value, self.contacts))
            if len(result) > 0:
                self.selected_contact: ContactInfo = result[0]    
                self.create_chat_area_frame()        
                self.chat_area_frame.on_contact_select(self.selected_contact)          

    def create_chat_area_frame(self):
        if self.chat_area_frame:
            if self.chat_area_frame.winfo_manager() == '':           
                self.chat_area_frame.pack(fill=constants.BOTH, side=constants.LEFT, expand=True)   
            return
        
        self.chat_area_frame = ChatAreaFrame(self.master, self.ui_service,
                                            self.contact_business_service, self.message_business_service)
        self.chat_area_frame.pack(fill=constants.BOTH, side=constants.LEFT, expand=True)   
        self.create_chat_area_frame_fn(self.chat_area_frame)     