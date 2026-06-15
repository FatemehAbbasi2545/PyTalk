from tkinter import Tk, Frame, Canvas, Scrollbar, Text, Button, Label, constants, messagebox
from Ui.Frames.base_frame import BaseFrame
from Ui.ui_service import UiService
from Business.contact_business_service import ContactBusinessService
from Business.message_business_service import MessageBusinessService
from Common.Entities.contact import ContactInfo
from Common.Entities.message import Message
from Common.DTO.response import Response

class ChatAreaFrame(BaseFrame):
    def __init__(self, container: Tk, ui_service: UiService, contact_business_service: ContactBusinessService,
                message_business_service: MessageBusinessService):
        super().__init__(container, ui_service)
              
        self.contact_business_service = contact_business_service  
        self.message_business_service = message_business_service  

        self.build_top_frame()
        self.build_chat_area()
        self.build_input_message_area()

        self.sys_label = None
        self.selected_contact = None
        self.chat_history: list[Message] = []

    def build_top_frame(self):
        self.top_frame = Frame(self, bg="#ffffff", height=20)
        self.top_frame.pack(fill='x', side='top', expand=False, pady=(10, 0), padx=5)
        self.top_frame.pack_propagate(False)

        self.top_frame.columnconfigure(0, weight=1)  
        self.top_frame.columnconfigure(1, weight=0)  

        self.refresh_button = Button(self.top_frame, text="Refresh", command=self.refresh, font=('Segoe UI', 11), bg='#4682B4', fg='#FFFFFF', activebackground='#4169E1', activeforeground='#FFFFFF', relief='raised', borderwidth=0)
        self.refresh_button.grid(row=0, column=1, padx=(5, 0))
    
    def build_chat_area(self):
        self.chat_canvas = Canvas(self, bg="white")
        self.chat_canvas.pack(fill='both', side=constants.TOP, expand=True)

        self.chat_scrollbar = Scrollbar(self.chat_canvas, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollbar.pack(side='right', fill='y')

        # فریم داخلی که گفتگوها در آن قرار می‌گیرند
        self.chat_frame = Frame(self.chat_canvas, bg="white")
        self.chat_frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=10)

        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)            

    def build_input_message_area(self):
        # فریم ورودی پیام (پایین چت)
        self.input_msg_frame = Frame(self, bg="#f0f0f0", height=50)
        self.input_msg_frame.pack(fill=constants.X, side=constants.BOTTOM, expand=False,pady=(10, 0), padx=10)
        self.input_msg_frame.pack_propagate(False)

        # کادر تایپ پیام
        self.input_msg_text = Text(
            self.input_msg_frame,
            height=5, # تعداد خطوط
            width=40,
            font=("Segoe UI", 12),
            wrap=constants.WORD, # شکستن کلمات کامل (پیش‌فرض: tk.CHAR)
            padx=5,
            pady=5,
            relief=constants.SUNKEN,
            borderwidth=1
        )
        self.input_msg_text.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # دکمه ارسال پیام
        self.send_msg_button = Button(self.input_msg_frame, text="Send", bg="#4682B4", fg="white", relief='flat', width=5, command=self.send_message)
        self.send_msg_button.pack(side="right")

    def on_contact_select(self, selected_contact: ContactInfo):
        self.selected_contact = selected_contact   
        self.clear_chat_screen()
        self.add_system_message(f"Chat with {self.selected_contact.audience_name} ...")
        self.get_history()  
        self.show_chat_histgory()
        self.update_scroll()           
    
    def add_system_message(self, text):
        """ نمایش پیام‌های سیستمی (مثل "گفتگو شروع شد") """
        if not self.sys_label:
            self.sys_label = Label(
                self.top_frame, 
                text=text, 
                bg="white", 
                fg="#888888",
                font=("Segoe UI", 11),
                wraplength=500,
                padx=10,
                pady=5
            )
            self.sys_label.grid(row=0, column=0, sticky="n")
        else:
            self.sys_label.config(text=text)  

    def send_message(self):
        msg_text = self.input_msg_text.get("1.0", constants.END).strip() # از خط 1 کاراکتر 0 تا انتها

        if not msg_text:
            return 
        
        msg = Message(message_id=None,
                    sender_id=self.selected_contact.user_id,
                    receiver_id=self.selected_contact.audience_id,
                    content=msg_text)
        
        response = self.message_business_service.save_message(msg)

        if not response.success:
            messagebox.showerror(title="Internal Server Error!", message=response.message)              
        else:            
            self.input_msg_text.delete("1.0", constants.END)
            # ساخت ویجت برای پیام جدید
            # یک فریم کوچک برای هر پیام می‌سازیم تا بتوانیم استایل‌بندی کنیم
            msg_label = Label(
                self.chat_frame, 
                text=msg_text, 
                bg="#f0f8ff",
                fg="black",
                wraplength=400, # طول لایه برای شکستن خط در پیام‌های طولانی
                justify="left",
                font=("Segoe UI", 11)
            )
            msg_label.pack(fill="x", padx=10, pady=5, ipadx=5, ipady=5)
            self.update_scroll()

    def clear_chat_screen(self):
        # به‌روزرسانی متن در قسمت چت 
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

    def get_history(self):
        if not self.selected_contact:
            return        
        response: Response = self.message_business_service.get_history(self.selected_contact.user_id, self.selected_contact.audience_id)
        self.chat_history = response.data            

    def show_chat_histgory(self):                
        for x in self.chat_history:
            if x.sender_id == self.selected_contact.user_id:
                bg_color = "#f0f8ff" # برای پیام هایی که همین کاربر فرستاده
                fg_color = "#000000"
                padx_right = 10
                padx_left = 50
            elif x.receiver_id == self.selected_contact.user_id:
                bg_color = "#f8f8ff" # برای پیام هایی که مخاطب فرستاده
                fg_color = "#000000"
                padx_right = 50
                padx_left = 10
        
            msg_content_frame = Frame(self.chat_frame, bg=bg_color)
            msg_content_frame.pack(fill="x", padx=(padx_left, padx_right), pady=5)

            msg_label = Label(
                msg_content_frame, 
                text = x.content, 
                wraplength = 400, # طول لایه برای شکستن خط در پیام‌های طولانی
                justify = "left",
                background = bg_color,
                foreground = fg_color,
                font=("Segoe UI", 11)
            )
            msg_label.pack(fill="x", padx=10, pady=5, ipadx=5, ipady=5)

    def update_scroll(self):
        # آپدیت محدوده اسکرول
        self.chat_frame.update_idletasks() # اطمینان از آپدیت ابعاد فریم
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1) # اسکرول به پایین‌ترین نقطه

    def refresh(self):
        self.clear_chat_screen()
        self.get_history()  
        self.show_chat_histgory()
        self.update_scroll() 
        