import urllib.request
import json
from bs4 import BeautifulSoup
import lxml
from configs import Config

class NaverApi:
    def __init__(self, config : Config):
        self.config = config
        self.client_id = self.config.papago_api.client_id
        self.client_secret = self.config.papago_api.client_secret

    def papago(self, source, target_lang):
        return self._papago_translate(self.papgo_langDetect(source), target_lang, source)

    def _papago_translate(self, source_lang, target_lang, source):
        data = "source={source_lang}&target={target_lang}&text={source}"
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)
        response = urllib.request.urlopen(request, 
            data=(data.format(source_lang=source_lang, target_lang=target_lang, source=source).encode('utf-8')))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            result = response_body.decode('utf-8')
            print(result)
            return json.loads(result)["message"]["result"]["translatedText"]
        else:
            print("Error Code: " + rescode)
            return "Error Code: " + rescode
            
    def papgo_langDetect(self, query):
        data = "query={0}".format(query)
        url = "https://openapi.naver.com/v1/papago/detectLangs"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if rescode==200:
            response_body = response.read()
            result = response_body.decode('utf-8')
            return json.loads(result)["langCode"]
        else:
            print("Error Code: " + rescode)
            return "Error Code: " + rescode
    def get_currency(self):
        url = urllib.request.urlopen("http://info.finance.naver.com/marketindex/exchangeList.nhn")
        source = url.read()
        url.close()
        class_list = ["tit", "sale"]
        soup = BeautifulSoup(source, 'lxml')
        soup = soup.find_all("td", class_=class_list)
        money_data={}
        for data in soup:
            if soup.index(data) % 2 == 0:
                data = data.get_text().replace('\n', '').replace('\t', '')
                money_key = data
            elif soup.index(data) % 2 == 1:
                money_value = data.get_text()
                money_data[money_key] = money_value
                money_key = None
                money_value = None
        return money_data