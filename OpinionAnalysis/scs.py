#! /usr/bin/env python
#coding:utf-8

import sys
import re
import urllib2
import urllib
import requests
import cookielib

## 这段代码是用于解决中文报错的问题
reload(sys)
sys.setdefaultencoding("utf8")
#####################################################
#登录人人
loginurl = 'http://bm.scs.gov.cn/2015/StudentLogin.aspx'
logindomain = 'bm.scs.gov.cn'
valicode_url ='http://bm.scs.gov.cn/2015/StudentLogin.aspx'
class Login(object):

    def __init__(self):
        self.name = ''
        self.passwprd = ''
        self.domain = ''
        httpHandler = urllib2.HTTPHandler(debuglevel=0)
        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj),httpHandler)
        urllib2.install_opener(self.opener)


    #获取验证码
    def get_valicode(self):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 '
                                     'Safari/537.36',
                    'Referer':'http://bm.scs.gov.cn/2015/StudentLogin.aspx',
                    'Origin':'http://bm.scs.gov.cn',
                    'Host':'bm.scs.gov.cn'
        }
        req = urllib2.Request(valicode_url, headers = headers)
        html = urllib2.urlopen(req).read()
        regex = re.compile('<img id="Loginbystudent1_Image1" src="(.*?)".*?/>')
        for match in re.findall(regex,html):
            if  not match:
                print('wrong')
                exit()
            valicode_true_url = "http://bm.scs.gov.cn/2015/%s" %match

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 '
                                     'Safari/537.36',
                    'Referer':'http://bm.scs.gov.cn/2015/StudentLogin.aspx',
                    'Origin':'http://bm.scs.gov.cn',
                    'Host':'bm.scs.gov.cn'
                }

        req = urllib2.Request(valicode_true_url, headers= headers)
        response= urllib2.urlopen(req)
        response_head = response.headers
        res_list = response_head['Set-Cookie'].split(';')
        valicode_str = res_list[0].split('=').pop()

        print('获取'+valicode_str+'验证码')
        #模拟登陆
        self.login(valicode_str)



    def login(self,vcode):
        '''登录网站'''
        loginparams = {'__EVENTTARGET':'Loginbystudent1$btn_Login',
                        '__EVENTARGUMENT':'',
                        '__VIEWSTATE':'/wEPDwUJNDE0NzE3NzcwD2QWAgIBD2QWAgIBDw8WBh4RQnVpbGRNYW5hZ2VySW1hZ2VnHgZLZXlYbWwFCGdrcnNha2V5HhBNYW5hZ2VyVmFsaWRDb2RlBQU0UVRVQ2QWAmYPZBYEAgMPDxYCHgRUZXh0BUINCgkJCQkJPGltZyBzcmM9IkltYWdlcy9uZXdpbWFnZXMvU3R1ZGVudExvZ2luXzA2LmdpZiIgYm9yZGVyPSIwIj4WAh4Hb25jbGljawV6amF2YXNjcmlwdDpyZXR1cm4gU1JBRW5jcnlwdCgnTG9naW5ieXN0dWRlbnQxX3R4dF9JZGVudGlmeScsJ0xvZ2luYnlzdHVkZW50MV90eHRQYXNzd29yZCcsJ0xvZ2luYnlzdHVkZW50MV9oaWRfcGFzc3dvcmQnKTtkAgsPDxYCHghJbWFnZVVybAUxLi4vdmFsaXRjb2RlaW1hZ2UuYXNweD92YWxpdGRhdGU9a3o1YWpsJTJmOTIzOCUzZGRkZFekAGHTXHdx/1ZHOWaZuBIuOAYf',
                        '__EVENTVALIDATION':'/wEWCAKzsqbIDALj96u0CwK8hJHrDwL0jfXMCQL1z8S4CwLhudf5DgLC9KjRBQK36eqIDArPIJ+NZZcTkqkr0ozaI21C3e+B',
                        'Loginbystudent1$txt_Identify':'',
                        'Loginbystudent1$txtPassword':'',
                        'Loginbystudent1$txt_vcode':vcode,
                'Loginbystudent1$hid_password':'9f87c2888e88cbfcbdac34d1eb1574da0b38b14aa3774c2223edfd49aa1e59fedaa9a59540cef263bfa8b9ae5ccafd756f50b4686bcf0e004223cc7c038120c0bb632cd22b1eec8b89377d59c676ac25a9c083e18a642c51fb5fb78798913155b5130a3c4e0a1a92d96b7dc60ded09c844ea38a9409532985c407919aecaf158'
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
                    'cookie':'BIGipServergk_pool=3530752266.38943.0000; ValicodeCookie=ValicodeCookie='+vcode
        }
        req = urllib2.Request(loginurl, urllib.urlencode(loginparams),headers=headers)
        response = urllib2.urlopen(req)
        f = open('./a.html','w')
        f.write(response.read())
        f.close()
        exit()
        self.operate = self.opener.open(req)
        thePage = response.read()

    def request_html(self):
        '''请求数据'''
        url ='http://bm.scs.gov.cn/2015/UserControl/Student/StudentManager.aspx'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        request_info = urllib2.Request(url,headers=headers)
        html = urllib2.urlopen(request_info).read()
        f = open('./a.html','w')
        f.write(html)
        f.close()



if __name__ == '__main__':
    userlogin = Login()
    userlogin.get_valicode()
    # username = 'zhuguojie1989@163.com'
    # password = 'zhuguojie1989'
    # domain = logindomain
    # userlogin.setLoginInfo(username,password,domain)
    # userlogin.login()
    # userlogin.request_html()


