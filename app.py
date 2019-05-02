# -*- coding: UTF-8 -*-

import time
import hashlib
from lxml import etree
from flask import request
from flask import Flask, make_response

import Chatbot

access_token = "24.34fd763ea193f974cb69114f3ef3f4ef.2592000.1559315592.282335-16151243"

class Message(object):
    def __init__(self, req):
        self.request = req
        self.token = 'wechat'
        self.AppID = 'wx87afdf441a105b68'
        self.AppSecret = '17fe3ab3adb485981fafd177a8d6d85f'


class Get(Message):
    def __init__(self, req):
        super(Get, self).__init__(req)
        self.signature = req.args.get('signature')
        self.timestamp = req.args.get('timestamp')
        self.nonce = req.args.get('nonce')
        self.echostr = req.args.get('echostr')
        self.return_code = 'Invalid'

    def verify(self):
        data = sorted([self.token, self.timestamp, self.nonce])
        string = ''.join(data).encode('utf-8')
        hashcode = hashlib.sha1(string).hexdigest()
        if self.signature == hashcode:
            self.return_code = self.echostr


class Post(Message):
    def __init__(self, req):
        super(Post, self).__init__(req)
        self.xml = etree.fromstring(req.stream.read())
        self.MsgType = self.xml.find("MsgType").text
        self.ToUserName = self.xml.find("ToUserName").text
        self.FromUserName = self.xml.find("FromUserName").text
        self.CreateTime = self.xml.find("CreateTime").text
        self.MsgId = self.xml.find("MsgId").text

        hash_table = {
            'text': ['Content'],
            'image': ['PicUrl', 'MediaId'],
            'voice': ['MediaId', 'Format'],
            'video': ['MediaId', 'ThumbMediaId'],
            'shortvideo': ['MediaId', 'ThumbMediaId'],
            'location': ['Location_X', 'Location_Y', 'Scale', 'Label'],
            'link': ['Title', 'Description', 'Url'],
        }
        attributes = hash_table[self.MsgType]
        self.Content = self.xml.find("Content").text if 'Content' in attributes else ''
        self.PicUrl = self.xml.find("PicUrl").text if 'PicUrl' in attributes else ''
        self.MediaId = self.xml.find("MediaId").text if 'MediaId' in attributes else ''
        self.Format = self.xml.find("Format").text if 'Format' in attributes else ''
        self.ThumbMediaId = self.xml.find("ThumbMediaId").text if 'ThumbMediaId' in attributes else ''
        self.Location_X = self.xml.find("Location_X").text if 'Location_X' in attributes else ''
        self.Location_Y = self.xml.find("Location_Y").text if 'Location_Y' in attributes else ''
        self.Scale = self.xml.find("Scale").text if 'Scale' in attributes else ''
        self.Label = self.xml.find("Label").text if 'Label' in attributes else ''
        self.Title = self.xml.find("Title").text if 'Title' in attributes else ''
        self.Description = self.xml.find("Description").text if 'Description' in attributes else ''
        self.Url = self.xml.find("Url").text if 'Url' in attributes else ''
        self.Recognition = self.xml.find("Recognition").text if 'Recognition' in attributes else ''



class Reply(Post):
    def __init__(self, req):
        super(Reply, self).__init__(req)
        self.xml =\
            '<xml><ToUserName><![CDATA[%s]]></ToUserName>' \
            '<FromUserName><![CDATA[%s]]></FromUserName>'  \
            '<CreateTime>%s</CreateTime>' % (self.FromUserName, self.ToUserName, str(int(time.time())))

    def text(self, content):

        self.xml += '<MsgType><![CDATA[text]]></MsgType>' \
            '<Content><![CDATA[%s]]></Content></xml>' % content

    def image(self, MediaId):
        pass

    def voice(self, MediaId):
        pass

    def video(self, MediaId, Title, Description):
        pass

    def music(self, ThumbMediaId, Title='', Description='', MusicURL='', HQMusicUrl=''):
        pass

    def reply(self):
        response = make_response(self.xml)
        response.content_type = 'application/xml'
        return response

app = Flask(__name__)
app.debug = True


@app.route('/')  # default index
def index():
    return "Index Page"


@app.route('/wx', methods=["GET", "POST"])
def wechat_auth():
    if request.method == "GET":
        message = Get(request)
        message.verify()
        return message.return_code

    elif request.method == "POST":
        message = Reply(request)

        uid = message.FromUserName
        session_id = Chatbot.get_session_id(uid)

        get_message = message.Content
        session_key, reply_message = Chatbot.chatbot_reply(access_token, session_id, get_message)

        Chatbot.update_session_id(uid, session_key)

        message.text(reply_message)
        return message.reply()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)