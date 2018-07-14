from HandlerBase import HandlerBase

class GiphyHandler(HandlerBase):
    def __init__(self, config):
        super(GiphyHandler, self).__init__(config)
    
    def on_chat_message(self, chat_handler, msg):
        pass