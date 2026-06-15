from abc import ABC
from tkinter import Tk, Frame
from Ui.ui_service import UiService

class BaseFrame(ABC, Frame):
    def __init__(self, container: Tk, ui_service: UiService):      
        super().__init__(container)         
        self.ui_service = ui_service       
        self["bg"] = '#F0F0F0'

        self.create_labels()
        self.create_entries()
        self.create_buttons()    

    def create_labels(self):
        pass

    def create_entries(self):
        pass

    def create_buttons(self):
        pass