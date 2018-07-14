import json

class Config:
    def __init__(self):
        with open('../Data/config.json', 'r') as jsonConfig:
            config = json.loads(jsonConfig.read())
            self.telegrma_data  = Telegram(config['telegram_bot'])
            papgoData = config['NaverApi']['papago']
            self.papago_api = PapagoApi(papgoData['client_id'], papgoData['client_secret'])
            self.torrent_config = TorrentConfig(config['torrent'])

    
    def get_telegram_data(self):
        return self.telegrma_data;

    def get_papago_data(self):
        return self.papago_api

    def get_torrent_config(self):
        return self.torrent_config

class Telegram:
    def __init__(self, telegram_config):
        self.telegrma_token = telegram_config['telegram_bot_token']
        self.telegram_command_list = telegram_config['command_list']

class PapagoApi:
    def __init__(self, id, secret):
        self.client_id = id
        self.client_secret = secret
    
    def get_client_id(self):
        return self.client_id
    
    def get_client_secret(self):
        return self.client_secret

class TorrentConfig:
    def __init__(self, torrent_config):
        self.valid_users = torrent_config['valid_user_id']
        self.base_url = torrent_config['base_url']

    def get_valid_user_list(self):
        return self.valid_users
    
    def get_base_url(self):
        return self.base_url