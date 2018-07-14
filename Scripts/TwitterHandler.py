
from HandlerBase import HandlerBase

class TwitterHandler(HandlerBase):
    def __init__(self, config):
        super(TwitterHandler, self).__init__(config)
    
    def on_chat_message(self, chat_handler, msg):
        pass