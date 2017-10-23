#-*-coding:utf-8-*-

import pytesseract
from PIL import Image
import requests
import os

def vcode():
    pic_url = 'http://xxx/vcode.php'
    r = requests.get(pic_url)
    with open('tmp.png', 'wb') as pic:
        pic.write(r.content)
    try:
        im = pytesseract.image_to_string(Image.open('tmp.png'))
        im = im.replace(' ', '')
        '''
        if im != '':
            return im
        else:'''
        return vcode()
    except:
        return 'err'

print vcode()