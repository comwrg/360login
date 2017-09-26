# coding=utf-8
"""
@author: comwrg
@license: MIT
@time : 2017/08/14 15:25
@desc : 360 login api
"""

import re

import requests
from . import utils


class _360:
    def __init__(self, user, pwd):
        self._session = requests.session()
        self._session.verify = False
        self._user = user
        self._pwd = pwd

    def verify(self):
        """To check captcha whether need or not.

        :return: If need captcha, return img of captcha, else return empty string.
        :rtype: str
        """
        url = 'http://login.360.cn/?callback=&src=pcw_360ssp&from=pcw_360ssp&charset=utf-8&requestscema=http&o=sso&m=checkNeedCaptcha&account={user}&captchaapp=i360&_=1502695550342'.format(
                user=self._user)
        r = self._session.get(url)
        # {"errno":"0","errmsg":"ok","errinfo":{"en":"ok"},"captchaflag":true,"captchaurl":"http:\/\/passport.360.cn\/captcha.php?m=create&app=i360&scene=login&userip=i7vjrgshxd1iby6btw%2bftg%3d%3d&level=default&sign=ffe89b&r=1502696036"}
        j = r.json()
        if j['errno'] is not '0':
            raise Exception(j)
        if j['captchaFlag']:
            return self._session.get(j['captchaUrl']).content
        else:
            return ''

    def _get_token(self):
        """Get token, needed when login.

        error code
        219 : user not exist

        :return: token
        :rtype: str
        """
        url = 'https://login.360.cn/?func=()&src=pcw_360ssp&from=pcw_360ssp&charset=UTF-8&requestscema=https&o=sso&m=getToken&username={user}&_=1502695550343'.format(
                user=self._user)
        r = self._session.get(url)
        # {"errno":0,"errmsg":"","token":"e27aa689169e6060"}
        j = r.json()
        errno = j['errno']
        if errno is 0:
            return j['token']
        else:
            Exception(j)

    def login(self, captcha):
        """
        login error code
        78002 : need captcha

        :type captcha: str
        :return: If login success return empty string, else return response body.
        :rtype: str
        """
        r = self._session.post(
                url='https://login.360.cn/',
                data={
                    'src'         : 'pcw_360ssp',
                    'from'        : 'pcw_360ssp',
                    'charset'     : 'UTF-8',
                    'requestScema': 'https',
                    'o'           : 'sso',
                    'm'           : 'login',
                    'lm'          : '0',
                    'captFlag'    : '1',
                    'rtype'       : 'data',
                    'validatelm'  : '0',
                    'isKeepAlive' : '1',
                    'captchaApp'  : 'i360',
                    'userName'    : self._user,
                    'smDeviceId'  : '',
                    'type'        : 'normal',
                    'account'     : self._user,
                    'password'    : utils.md5(self._pwd),
                    'captcha'     : captcha,
                    'token'       : self._get_token(),
                    'proxy'       : 'http://ssp.360.cn/psp_jump.html',
                    'callback'    : 'QiUserJsonp695550467',
                    'func'        : 'QiUserJsonp695550467'
                },
                headers={
                    'referer'     : 'http://ssp.360.cn/webmaster/index',
                    'accept'      : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'content-type': 'application/x-www-form-urlencoded',
                }
        )

        if r.text.find('errno=0') is -1:
            return r.text

        m = re.search("href='(.*?)'", r.text)
        url = m.group(1)
        self._session.get(url)
        return ''
