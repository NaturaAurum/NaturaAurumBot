class HandlerBase:
    def __init__(self, config):
        self.config = config

    def get_greeting_message(self, mode_name : str):
        return "{} 모드 입니다! 메뉴를 골라주세요!".format(mode_name)

    def create_button(self, l : list):
        l.append("처음으로")
        return l

    def on_chat_message(self, chat_handle, msg):
        pass

    def on_callback_query(self, msg):
        pass