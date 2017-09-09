#coding:utf-8

import requests,re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class v2ex:
    s=requests.Session()
    def login(self):
        loginpage = self.s.get("https://www.v2ex.com/signin", verify=False).text
        payload={
            re.findall('type="text" class="sl" name="([a-f0-9]{64,64})"', loginpage)[0]:self.u,
            re.findall('type="password" class="sl" name="([a-f0-9]{64,64})"', loginpage)[0]:self.p,
            "next":"/",
            "once":re.findall('value="(\d+)" name="once"',loginpage)[0]
            }
        signin=self.s.post("https://www.v2ex.com/signin",data=payload,headers={'Referer': 'https://www.v2ex.com/signin'}, verify=False)
        if signin.text.find("signout")==-1:
            print "[+] : "+self.u+" Login Faild"
        else:
            print "[+] : "+self.u+" Login Success"
            self.sign()

    def sign(self):
        if self.s.get("https://www.v2ex.com/mission/daily", verify=False).text.find("fa-ok-sign")!=-1:
            print "[+] : "+self.u+" Has Been Checked In"
        else:
            try:
                daily=re.findall('(/mission/daily/redeem\?once=\d+)',self.s.get("https://www.v2ex.com/mission/daily", verify=False).text)[0]
                a=self.s.get("https://www.v2ex.com"+daily,headers={"Referer":"https://www.v2ex.com/mission/daily"}, verify=False)
                print "[+] : "+self.u+" Checkin Success"
            except:
                print "[+] : "+self.u+" Checkin Faild"

    def __init__(self,u,p):
        self.u=u
        self.p=p
        self.login()


v2ex("username","password")
