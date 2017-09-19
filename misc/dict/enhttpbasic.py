import base64
dic = 'weak100.txt'

with open(dic,'r') as f1:
	all = f1.readlines()
with open('en-'+dic,'w') as f2:
	c = 1
	for x in all:
		for y in all:
			t = x.strip('\n') + ':' + y.strip('\n')
			f2.write(base64.b64encode(t)+'\n')
		print str(c) + '  OK!\n'
		c += 1