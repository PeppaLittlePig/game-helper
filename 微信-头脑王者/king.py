#!/usr/bin/env python3
import json
from mitmproxy import ctx
from urllib.parse import quote
import string
import requests

#mitmdump 监听方法
def response(flow):
    #获得当前请求路径
    path = flow.request.path
    #获得题目请求路径
    question_path = '/question/bat/findQuiz'
    if(path == question_path):
        data = json.loads(flow.response.text)
        #问题
        question = data['data']['quiz']
        #选项
        options = data['data']['options']
        ctx.log.info('question : %s, options : %s'%(question, options))
        options = ask(question, options)
        data['data']['options'] = options
        #回写选项
        flow.response.text = json.dumps(data)

#百度查询答案，修改response返回结果
def ask(question, options):
    url = quote('https://www.baidu.com/s?wd=' + question, safe = string.printable)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    content = requests.get(url, headers=headers).text
    answer = []
    counts = []
    flag = True
    #题目包含“不是”，则答案取count最少
    if(question.find("不是") != -1):
        flag = False

    for option in options:
        #获取对应选项答案数量
        count = content.count(option)
        counts.append(count)
        ctx.log.info('option : %s, count : %s' % (option, count))


    for index,option in enumerate(options):
        answer.append(option + getResultStr(counts,counts[index],flag))

    return answer

#返回最优选，当题目包含“不是”，则最优选是count最少的选项，否则当选项不为0时，数量最多的选项为最优选
def getResultStr(counts,indexCount,flag):
    best = '[最优]'
    if (flag):
        return best if indexCount == max(counts) and indexCount != 0 else '[' + str(indexCount) + ']'
    else:
        return best if indexCount == min(counts) else '[' + str(indexCount) + ']'

