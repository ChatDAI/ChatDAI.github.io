import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket  # 使用websocket_client



class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

class Spark():
    def __init__(self, appid, api_key, api_secret, Spark_url,domain, question):
        self.wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
        self.answer = ""
        websocket.enableTrace(False)
        self.wsUrl = self.wsParam.create_url()
        self.ws = websocket.WebSocketApp(self.wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close, on_open=self.on_open)
        self.ws.appid = appid
        self.ws.question = question
        self.ws.domain = domain
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    # 收到websocket错误的处理
    def on_error(self, _,  error):
        self.answer = "### error:"+str(error)


    # 收到websocket关闭的处理
    def on_close(self, one, two, three):
        pass


    # 收到websocket连接建立的处理
    def on_open(self, _):
        thread.start_new_thread(self.run, (self.ws,))


    def run(self, _, *args):
        data = json.dumps(self.gen_params())
        self.ws.send(data)


    # 收到websocket消息的处理
    def on_message(self, _, message):
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            self.answer = f'请求错误: {code}, {data}'
            self.ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            for item in content:
                self.answer += item
            if status == 2:
                self.ws.close()

    def gen_params(self):
        """
        通过appid和用户的提问来生成请参数
        """
        data = {
            "header": {
                "app_id": self.ws.appid,
                "uid": "1234"
            },
            "parameter": {
                "chat": {
                    "domain": self.ws.domain,
                    "random_threshold": 0.5,
                    "max_tokens": 2048,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": self.ws.question
                }
            }
        }
        return data



