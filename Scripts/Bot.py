import telepot
import asyncio


from configs import Config
from HandlerBase import HandlerBase
from TorrentHandler import TorrentHandler
from TwitterHandler import TwitterHandler
from WeatherHandler import WeatherHandler
from TranslateHandler import TranslateHandler
from GiphyHandler import GiphyHandler
from telepot.delegate import per_chat_id, create_open, pave_event_space, call, include_callback_query_chat_id
from telepot.aio.loop import MessageLoop
from enum import Enum

class BotMode(Enum):
    Default = -1
    Torrent = 0
    Twitter = 1
    Weather = 2
    Translate = 3
    Giphy = 4


class ChatHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(ChatHandler, self).__init__(*args, **kwargs)
        self.config = Config()
        self.mode = BotMode.Default
        self.handler = HandlerBase(self.config)
    
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        # 텍스트 이외의 콘텐츠가 오면 무시하자
        if content_type != 'text':
            self.sender.sendMessage("죄송합니다 이해 불가능")
            return

        command = msg['text'].strip().lower()
        if command.startswith('/'):
            commandList = self.config.telegrma_data.telegram_command_list
            # 설정 파일에서 지정된 커맨드 목록을 불러와 체크해준다.
            for i in range(0, len(commandList)):
                if commandList[i] == command:
                    self.set_mode(i)

        # 현재 무슨 모드인가 체크
        if self.mode != BotMode.Default:
            self.handler.on_chat_message(self, msg['text'])

        # 커맨드가 설정된 커맨드가 아닐 경우는 안내메세지 보내주기.
        if self.mode == BotMode.Default:
            self.sender.sendMessage("명령어를 입력해주세요!")
    def on_callback_query(self, msg):
        self.handler.on_callback_query(msg)

    def set_mode(self, mode):
        self.mode = mode
        if mode == 0:
            self.handler = TorrentHandler(self.config)
        elif mode == 1:
            self.handler = TwitterHandler(self.config)
        elif mode == 2:
            self.handler = WeatherHandler(self.config)
        elif mode == 3:
            self.handler = TranslateHandler(self.config)
        elif mode == 4:
            self.handler = GiphyHandler(self.config)
        else:
            self.handler = HandlerBase(self.config)

class Bot(telepot.DelegatorBot):
    def __init__(self, token):
        super(Bot, self).__init__(token, [
            include_callback_query_chat_id(
            pave_event_space())(per_chat_id(), create_open, ChatHandler, timeout=120)
        ])

# 설정 파일 불러오기
config = Config()

# 설정 파일에서 토큰을 가져와 봇 객체를 만들어주기
bot = Bot(config.telegrma_data.telegrma_token)
# 봇 실행
bot.message_loop(run_forever='Listening')