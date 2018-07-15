import giphy_client
from enum import Enum
from giphy_client.rest import ApiException

from HandlerBase import HandlerBase

class GiphyMode(Enum):
    Default = 0
    WaitKeyword = 1
    End = 2

class GiphyHandler(HandlerBase):
    def __init__(self, config):
        self.api_key = config.giphy_api_key
        self.giphy_api_instance = giphy_client.DefaultApi()
        self.mode = GiphyMode.Default
        super(GiphyHandler, self).__init__(config)

    def on_chat_message(self, chat_handler, msg):
        if self.mode == GiphyMode.Default:
            chat_handler.sender.sendMessage("검색 키워드를 입력해주세요!")
            self.mode = GiphyMode.WaitKeyword
            return
        if self.mode == GiphyMode.WaitKeyword:
            api_response = self.giphy_api_instance.gifs_search_get(self.api_key, msg, limit=10, offset=0, rating='g', fmt='json')
            mediaGroup = []
            for gifData in api_response.data:
                data = {}
                data["type"] = "video"
                #origin_url = gifData.images.original.url.split('?')
                #data["media"] = origin_url[0]
                data["media"] = gifData.images.original.mp4
                print(data["media"])
                mediaGroup.append(data)
            chat_handler.sender.sendMediaGroup(mediaGroup)
            self.mode = GiphyMode.Default
        