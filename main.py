from Ui.ui_service import UiService
from Ui.view_container import ViewContainer
from DataAccess.user_repository import UserRepository
from DataAccess.contact_repository import ContactRepository
from DataAccess.message_repository import MessageRepository
from Business.user_business_service import UserBusinessService
from Business.contact_business_service import ContactBusinessService
from Business.message_business_service import MessageBusinessService

user_repository = UserRepository('messenger.db')
contact_repository = ContactRepository('messenger.db')
message_repository = MessageRepository('messenger.db')

user_business_service = UserBusinessService(user_repository)
contact_business_service = ContactBusinessService(contact_repository)
message_business_service = MessageBusinessService(message_repository)

ui_service = UiService()

def create_view():
    ViewContainer(ui_service, user_business_service, contact_business_service, message_business_service)

if __name__ == '__main__':
    create_view()
    # # ایجاد دو فرآیند جداگانه
    # p1 = multiprocessing.Process(target=create_view)
    # p2 = multiprocessing.Process(target=create_view)
    
    # # شروع فرآیندها
    # p1.start()
    # p2.start()
    
    # # انتظار برای اتمام (اختیاری)
    # p1.join()
    # p2.join()



