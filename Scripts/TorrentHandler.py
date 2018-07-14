from HandlerBase import HandlerBase

class TorrentHandler(HandlerBase):
    def __init__(self, config):
        super(TorrentHandler, self).__init__(config)
    
    def on_chat_message(self, chat_handler, msg):
        pass