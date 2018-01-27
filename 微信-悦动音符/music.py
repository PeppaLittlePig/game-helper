#!/usr/bin/env python3
'''
微信小程序-悦动音符刷分
'''
import requests
import json

headers = {
    "Host": "mp.weixin.qq.com",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wxd3ae9f954fda16cc/9/page-frame.html",
    "Accept-Language": "zh-cn"
}

session_id = '' #抓包获取session_id
openid = ''  #抓包获取openid
score = 9999 #填写需要刷的分数

base_req = '{"base_req":{"session_id":"%s","openid":"%s"}}' % (session_id,openid)
req_info = '{"base_req":{"session_id":"'+session_id+'","openid":"'+openid+'"},"score_info":[{"type":0,"score":'+str(score)+'},{"type":1,"score":7}],"stage_id":"%s"}'

base_resp = requests.post("https://mp.weixin.qq.com/wxagame/wxagame_getmusiclist",data=base_req,headers=headers,verify=False)
json_result = json.loads(base_resp.text)
#遍历歌曲列表刷分
for temp in json_result['music']:
    r = requests.post("https://mp.weixin.qq.com/wxagame/wxagame_settlement", data=req_info % temp['music_id'], headers=headers, verify=False)
    print(r)


