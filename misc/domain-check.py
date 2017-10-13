# -*- coding: utf-8 -*-
import requests as r

def remove_html_tags(text):
	import re
	clean = re.compile('<.*?>')
	return re.sub(clean, '', text)

def remove_trash_info(text):
	t = text.replace(' ','').replace('\r','').split('\n')
	while u'' in t:
		t.remove('')
	return t[4:]

def domain_check(domain,suffix=0):
	api = ['https://api1.hostker.com/zdomainCheck.php?type=1&domain=','https://api2.hostker.com/zdomainCheck.php?type=2&domain=','https://api3.hostker.com/zdomainCheck.php?type=3&domain=','https://api4.hostker.com/zdomainCheck.php?type=4&domain=']
	res = []
	can_reg = []
	for x in api:
		res.extend(remove_trash_info(remove_html_tags(r.get(x+domain).content.decode('utf-8'))))
	length = len(res)
	for index in list(xrange(0,length,4)):
		if len(res[index+3]) == 2:
			can_reg.append(res[index].split('.')[1])
	if suffix == 0:
		return can_reg
	else:
		if suffix in can_reg:
			return 1
		else:
			return 0
def get_one_suffix(domains,suffix):
	with open('one_suffix.txt','w+') as f:
		for x in domains:
			try:
				if domain_check(x,suffix) == 1:
					d = x+'.'+suffix
					f.write(d+'\n')
					print d+' Succ'
					continue
				else:
					print x+'.'+suffix+' Err'
			except:
				print x+'.'+suffix+' Err'
				continue


def get_all_suffix(domains):
	with open('all_suffix.txt','w+') as f:
		for x in domains:
			try:
				d = domain_check(x)
				if len(d) != 0:
					f.write(','.join([x+'.'+s for s in d])+'\n')
				print x+' Succ'
				continue
			except:
				print x+' Err'
				continue

if __name__ == '__main__':
	#print domain_check('zzz','ch')
	key = '0123456789abcdefghijklmnopqrstuvwxyz'
	three_domains = [str(x)+str(y)+str(z)  for x in key for y in key for z in key]
	two_domains = [str(x)+str(y)  for x in key for y in key]
	get_all_suffix(three_domains)