import re
import requests
from bs4 import BeautifulSoup
import traceback
import lxml

class V2EX(object):
    headers = {
        'User-Agent': (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        ),
        'Origin': 'https://www.v2ex.com',
        'Referer': 'https://www.v2ex.com/signin',
        'Host': 'www.v2ex.com'
    }

    def __init__(self, usrname, passwd):
        self.usrname = usrname
        self.passwd = passwd

    def login(self):
        try:
            login_url = 'https://www.v2ex.com/signin'
            s = requests.Session()
            login_html = s.get(login_url, headers = self.headers)
            login_html.raise_for_status()
            login_soup = BeautifulSoup(login_html.text, 'lxml')

            usrname_code = login_soup.find('input', {'class' : 'sl'})['name']
            passwd_code = login_soup.find('input', {'type' : 'password'})['name']
            once_code = login_soup.find('input', {'type' : 'hidden'})['value']

            form_data = {
                usrname_code:self.usrname,
                passwd_code:self.passwd,
                'once':once_code,
                'next':'/'
            }

            s.post(login_url, headers = self.headers, data = form_data)
            html_setting = s.get('https://www.v2ex.com/settings')
            pattern = re.compile('github')
            mat = pattern.search(html_setting.text)
            status = True if mat else False

            if status:
                soup = BeautifulSoup(requests.get('https://www.v2ex.com').text, 'lxml')
                # print(soup.prettify())
            return [s, status]

        except:
            traceback.print_exc()

    def get_daily(self, s):
        '''
        :param s: session 
        :return: None
        '''
        try:
            url_mission = 'https://www.v2ex.com/mission/daily'
            html_mission = s.get(url_mission, headers = self.headers)

            soup_mission = BeautifulSoup(html_mission.text, 'lxml')
            url_once = soup_mission.find('input', {'type': 'button'})['onclick'].split('\'')
            if url_once:
                url_once = url_once[1]
            url_get = 'https://www.v2ex.com' + url_once

            res = s.get(url_get, headers = {'Referer': 'https://www.v2ex.com/mission/daily'})
            if res.text.find('成功领取'):
                print('成功领取')
            else:
                print('领取失败')
        except:
            traceback.print_exc()

name = input('请输入id：')
passwd = input('密码：')

login = V2EX(name, passwd)
sess = login.login()

if sess[1] == True:
    print('登陆成功，正在领取奖励...')
    login.get_daily(sess[0])
else:
    print('登录失败，检查原因。')

'''
腾讯云centos安装python3 和 pip3

sudo yum install epel-release
sudo yum install python34
python3 -v


wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip3 -V

pip3 install requests bs4 lxml

添加定时任务
crontab -e
在下面加一行

6 6 * * * python3 /path/to/this/file

表示每年每月每星期六点六分执行该python脚本
具体作用请百度
'''
