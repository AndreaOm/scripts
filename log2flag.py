# -*- coding: UTF-8 -*-
import re,urllib

log = 'access.log' # log filename
regx = '=' # = ! > <

with open(log,'r') as f:
    data = urllib.unquote(f.read())

regx += '([0-9]{2,3})'

def log2flag(org):
    flag = []
    index = len(org) - 1
    while 1:
        if index == 0:
            break
        if (abs(int(org[index]) - int(org[index-1])) == 1):
            index -= 1
            continue
        else:
            if int(org[index-1]) > 127:
                index -= 1
                continue
            flag.append(chr(int(org[index-1])))
            index -= 1
            continue
    return flag[::-1]


flag = ''.join(log2flag(re.findall(regx,data)))

print flag

# regexr
'''

1 查找=!>< 这四个字符其中一个或者2个  后面跟上 115 103 99 116 102 123 125 这7个数字其中一个
regx = r'[=!><]+(115|103|99|116|102|123|125)'

2 查找16进制字符串 例如0x6d697363
regx = r'0x([a-f0-9]{1,})|0X([a-f0-9]{1,})'

'''
