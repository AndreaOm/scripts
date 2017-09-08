#-*- coding:utf-8 -*-
import re
import requests
import HTMLParser  
from flask import Flask

app = Flask(__name__)

def getUrl(name):
	return HTMLParser.HTMLParser().unescape(re.findall('<a target="_blank" uigs="account_name_0" href="(.*)">',requests.get('http://weixin.sogou.com/weixin?type=1&query='+name).content)[0])

weixinName = [
	'懒人在思考','先知安全技术社区'
	]
# 微信公众号名字 id从0开始	

@app.route('/url/<int:id>')
def url(id):
	return '<script language="javascript"type="text/javascript">window.location.href="' + getUrl(weixinName[id]) + '";</script>'

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8001)


