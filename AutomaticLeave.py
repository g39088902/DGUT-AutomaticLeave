import requests
import json
import sys
import re
import datetime
import time

# Global Params
username = '201811112222'
password = '33332222FFFF'
xueYuan='5013333306935158270'
zhuanYe='网络工程'
banJi='2018母猪护理3班'
xingMing='42566661507815567'
lianXiDianHua='18028637777'

shiJian= str(datetime.date.today() + datetime.timedelta(days=1))
jiaZhang='13302222215'
shenPi='42593960257911111,42593960442461111,42593961277121111,42593960148861111,123711910972481111'
loginUrl = 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/ibpstest/state/home'
homeUrl = 'http://e.dgut.edu.cn'

order_data ={"parameters":[
    {"key":"defId","value":"758369743466921984"},
    {"key":"version","value":"0"},
    {"key":"data","value":"{\"id\":\"\",\"xueYuan\":\""+xueYuan+"\",\"zhuanYe\":\""+zhuanYe+"\",\"banJi\":\""+banJi+"\",\"xingMing\":\""+xingMing+"\",\"lianXiDianHua\":\""+lianXiDianHua+"\",\"liXiaoShiJian\":\""+shiJian+"\",\"fanXiaoShiJian\":\""+shiJian+"\",\"qingJiaTianShu\":0,\"qingJiaLeiXing\":\"探亲\",\"liXiaoMuDiDi\":\"{\\\"street\\\":\\\"松山湖\\\",\\\"province\\\":\\\"44\\\",\\\"city\\\":\\\"4419\\\",\\\"district\\\":\\\"\\\"}\",\"qingJiaYuanYin\":\"与父母见面\",\"jiaChangDianHua\":\""+jiaZhang+"\",\"jiaTingZhuZhi\":\"{\\\"street\\\":\\\"松山湖\\\",\\\"province\\\":\\\"44\\\",\\\"city\\\":\\\"4419\\\",\\\"district\\\":\\\"440113\\\"}\",\"liXiaoChengZuoJTGJ\":\"自驾车\",\"liXiaoLuXian\":\"松山湖\",\"fanXiaoChengZuoJTGJ\":\"自驾车\",\"fanXiaoLuXian\":\"松山湖\",\"shenPiRen\":\""+shenPi+"\",\"xueHao\":\""+username+"\"}"}]}

def login():
    global homeUrl
    session = requests.session()
    html = session.get(loginUrl).content.decode('utf-8')
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    cookies = {"languageIndex": "0", "last_oauth_appid": "illnessProtectionHome", "last_oauth_state": "home"}
    pattern = re.compile(r"var token = \"(.*?)\";$", re.MULTILINE | re.DOTALL)
    data = {'username': username, 'password': password, '__token__': pattern.search(html).group(1),
            'wechat_verif': ''}
    response = json.loads(session.post(url=loginUrl, headers=headers, cookies=cookies, data=data).json())
    session.close()
    if response['message'] != '验证通过':
        console_msg('登录验证失败', 1)
        return 1
    console_msg('登录验证成功', 0)
    homeUrl = response['info']
    return 0


def order():
    session = requests.session()
    html = session.get(url=homeUrl)

    pattern = re.compile(r"access_token=(.*?)&refresh_token", re.MULTILINE | re.DOTALL)
    token = pattern.search(html.url).group(1)
    headers = {'Accept': 'application/json, text/plain, */*','Host': 'e.dgut.edu.cn', 'Referer': 'http://e.dgut.edu.cn/draftForm/758369743466921984',
               'Origin': 'http://e.dgut.edu.cn', 'Content-type': 'application/json; charset=utf-8',
               'Accept-Encoding': 'gzip, deflate', 'X-Authorization-access_token': token}
    response = session.post(url='http://e.dgut.edu.cn/ibps/business/v3/bpm/instance/start', headers=headers,data=json.dumps(order_data),timeout=20)
    print(response.content.decode('utf-8'))
    return 0;


def console_msg(msg, level=2):
    header = ('[SUCCESS]', '[ERROR]', '[INFO]')
    color = ("\033[32;1m", "\033[31;1m", "\033[36;1m")
    print(color[level], header[level], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg + "\033[0m")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if login() != 0:
        console_msg('登录失败, 退出程序', 1)
        exit(1)
    if order() != 0:
        console_msg('请假失败, 退出程序', 1)
        exit(1)