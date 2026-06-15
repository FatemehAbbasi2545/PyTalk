class UiService:
    def set_add_contact_container_instance(self, instance):
        self.add_contact_container_instance = instance

    def add_contact_container_destroy(self):
        if self.add_contact_container_instance:
            self.add_contact_container_instance.destroy()

    def set_block_contacts_manager_container_instance(self, instance):
        self.block_contacts_manager_container = instance

    def block_contacts_manager_container_destroy(self):
        if self.block_contacts_manager_container:
            self.block_contacts_manager_container.destroy()
        
    def set_change_password_window_instance(self, instance):
        self.change_password_window = instance

    def change_password_window_destroy(self):
        if self.change_password_window:
            self.change_password_window.destroy()

    

  