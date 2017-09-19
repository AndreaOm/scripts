import sys
filename = sys.argv[1]
with open(filename,'r') as f1:
	all = f1.readlines()
with open('done-'+filename,'w') as f2:
	for x in all:
		if x == '\n':
			continue
		f2.write(x)