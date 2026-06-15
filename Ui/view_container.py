from tkinter import Tk, Frame
from Ui.ui_service import UiService
from Business.user_business_service import UserBusinessService
from Business.contact_business_service import ContactBusinessService
from Business.message_business_service import MessageBusinessService
from Ui.Frames.login_frame import LoginFrame
from Ui.Frames.register_frame import RegisterFrame
from Ui.Frames.navbar import Navbar
from Ui.Frames.contact_panel import ContactPanel

class ViewContainer(Tk):
    def __init__(self, ui_service: UiService, user_business_service: UserBusinessService, 
                contact_business_service: ContactBusinessService, message_business_service: MessageBusinessService):
        super().__init__()  
        self.ui_service = ui_service
        self.user_business_service = user_business_service
        self.contact_business_service = contact_business_service
        self.message_business_service = message_business_service

        self.title("My Messenger")
        self.geometry('1000x700')

        self.frames: dict[str, Frame] = {}        

        # Full screen window
        # width = Tk.winfo_screenwidth(self)
        # height = Tk.winfo_screenheight(self)
        # self.geometry(f'{width}x{height}')   
            
        self.add_frames()                
        self.mainloop()

    def add_frames(self):
        login_frame = LoginFrame(self, self.ui_service, self.user_business_service, 
                                show_register_frame_fn=self.show_register_frame,
                                show_navbar_fn=self.show_navbar,
                                show_contact_panel_fn=self.show_contact_panel)
        login_frame.pack(expand=True)
        self.frames['login'] = login_frame

        register_frame = RegisterFrame(self, self.ui_service, self.user_business_service, 
                                    show_login_frame_fn=self.show_login_frame) 
        self.frames['register'] = register_frame  

        navbar = Navbar(self, self.ui_service, self.user_business_service, self.contact_business_service,
                    update_contacts_fn=self.update_contacts, load_contacts_fn=self.load_contacts,
                    logout_fn=self.logout)  
        self.frames['navbar'] = navbar

        contact_panel = ContactPanel(self, self.ui_service, self.user_business_service, 
                                    self.contact_business_service, self.message_business_service,
                                    create_chat_area_frame_fn=self.create_chat_area_frame)        
        self.frames['contact_panel'] = contact_panel
    
    def show_login_frame(self):
        frame = self.frames['login']
        frame.pack(expand=True)

    def show_register_frame(self):
        frame = self.frames['register']
        frame.pack(expand=True)

    def show_navbar(self):
        frame = self.frames['navbar']
        frame.pack(fill='x', side='top', padx=0, pady=0)

    def show_contact_panel(self):
        frame: ContactPanel = self.frames['contact_panel']
        frame.pack(fill='y', side='left')
        frame.update_user_name_label()
        frame.load_contacts()

    def create_chat_area_frame(self, instance):
        self.frames['chat_area'] = instance

    def update_contacts(self, data):
        contact_panel: ContactPanel = self.frames['contact_panel']
        contact_panel.update_contacts(data)

    def load_contacts(self):
        contact_panel: ContactPanel = self.frames['contact_panel']
        contact_panel.load_contacts()

    def logout(self):
        self.user_business_service.current_user = None

        frame = self.frames['navbar']
        frame.pack_forget()

        frame = self.frames['contact_panel']
        frame.pack_forget()

        if 'chat_area' in self.frames.keys():
            frame = self.frames['chat_area']
            frame.pack_forget()
            
        self.show_login_frame()

       
