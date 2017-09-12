# -*- coding: UTF-8 -*-
import re,urllib

log = 'access.log' # log filename
regx = '([0-9]{1,3}),1\)\)=([0-9]{1,3})' 


'''
匹配数据同时记录匹配所在行号
返回的数据格式为 list
[(a,b,行号),(a,b,行号),...]

'''
def log2line():
	index = 1
	data = []
	with open(log,'r') as f:
		for line in f:
			r = re.findall(regx,urllib.unquote(line))
			if r:
				data.append((r[0][0],r[0][1],index))
			index += 1
	return data


'''
接受匹配的数据 通过判断移动指针 index
判断 指针所指与下一个 a 是否相等
相等不做操作 指针后移一位
不相等则记录指针所指位的b加入flag 在判断b是否大于127 是则输出b及其行号 指针后移一位

'''
def log2flag(ori):
	width = len(ori) - 1
	index = 0
	flag = []
	while 1:
		if (index == (width - 1)):
			break
		if (ori[index][0] == ori[index+1][0]):
			index += 1
			continue
		else:
			t = int(ori[index][1])
			if t > 127:
				print '[+] ascii:\033[1;32m'+str(t)+'\033[0m line:\033[1;33m'+str(ori[index][2]) + '\033[0m'
			flag.append(chr(t))
			index += 1
			continue
	return flag

flag = ''.join(log2flag(log2line()))

print flag

