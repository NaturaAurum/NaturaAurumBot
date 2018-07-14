

from HandlerBase import HandlerBase
from enum import Enum
from googletrans import Translator
from NaverApi import NaverApi
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot import glance
from googletrans import Translator
from NaverApi import NaverApi

class TranslateMode(Enum):
    Back = -1
    Default = 0
    WaitSource = 1
    

class TranslateHandler(HandlerBase):
    def __init__(self, config):
        self.mode = TranslateMode.Default
        self.google_trans = Translator()
        self.naver_api = NaverApi(config)
        self.supported_langs = ['ko', 'en', 'ja']
        super(TranslateHandler, self).__init__(config)

    def check_supported_langs(self, langCode):
        for lang in self.supported_langs:
            if lang == langCode:
                return True
        return False

    def on_chat_message(self, chat_handler, msg):
        if msg.startswith('/'):
            self.mode = TranslateMode.Default
        self.chat_handler = chat_handler
        if self.mode == TranslateMode.Default:

            self.mode = TranslateMode.WaitSource
            chat_handler.sender.sendMessage("번역할 문장과 언어 코드를 입력해주세요!\n 형식은 {번역할 문장} {번역할 언어 코드} 입니다!")

        elif self.mode == TranslateMode.WaitSource:
            self.target_source = msg
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='구글', callback_data='google'), 
                InlineKeyboardButton(text='파파고', callback_data='papago')]
            ])

            chat_handler.sender.sendMessage("골라주세요!", reply_markup=markup)
    
    def send_retry_message(self):
        markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='다시 시도', callback_data='retry')]
                ])
        self.chat_handler.sender.sendMessage("아쉽게도 지원하지 않아요 ㅠㅠ 다시 시도 해보실래요?", reply_markup=markup)

    def get_result_markup(self):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='다른 문장 번역', callback_data='other_try')]
        ])

        return markup

    def get_google_result(self):
        source = self.target_source[:-2]
        dest = self.target_source[-2:]

        if not self.check_supported_langs(dest):
            self.send_retry_message()
            return None
        
        result = self.google_trans.translate(source, dest=dest)
        return result
    def get_papago_result(self):
        source = self.target_source[:-2]
        dest = self.target_source[-2:]

        if not self.check_supported_langs(dest):
            self.send_retry_message()
            return None
        
        result = self.naver_api.papago(source, dest)
        return result
        
    def on_callback_query(self, msg):
        query_id, from_id, data = glance(msg, flavor='callback_query')
        print(data)
        data.strip().lower()
        #send_condtion = (self.mode != TranslateMode.Default and data == 'retry') or data == 'google' or data == 'papago'
        if data == 'google':
            result = self.get_google_result()
            if result == None : return
            self.chat_handler.sender.sendMessage("{0}\n[{1}]".format(result.text, result.pronunciation), reply_markup=self.get_result_markup())
        elif data == 'papago':
            result = self.get_papago_result()
            if result == None : return
            self.chat_handler.sender.sendMessage(result, reply_markup=self.get_result_markup())
        elif data == 'retry' or data == 'other_try':
            self.mode == TranslateMode.WaitSource
            self.chat_handler.sender.sendMessage("번역할 문장과 언어 코드를 입력해주세요!\n 형식은 {번역할 문장} {번역할 언어 코드} 입니다!")
        