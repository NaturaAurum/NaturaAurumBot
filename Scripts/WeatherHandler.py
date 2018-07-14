
from HandlerBase import HandlerBase

class WeatherHandler(HandlerBase):
    def __init__(self, config):
        super(WeatherHandler, self).__init__(config)
    
    def on_chat_message(self, chat_handler, msg):
        pass