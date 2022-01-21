#! -*- coding: utf-8 -*-

import html
import re
import time
import requests

class lang():
    def __init__(self, dic, tag) -> None:
        self.dic = dic if dic else {}
        self.tag = tag

    def transChinese(self, ses):
        ans = []
        nocomm = re.findall("(.*?)//", ses)
        
        if nocomm:
            new_ses = str().join(nocomm)
        else:
            new_ses = ses

        nocomm = re.findall("(.*?)\*", new_ses)
        if nocomm:
            new_ses = str().join(nocomm)


        xx = u"([(（\-]*\w*[\u4e00-\u9fff]+[.。，,;；)）>=\/\、\-(（\d:：？?\u4e00-\u9fff\w]*[\u4e00-\u9fff]+[.。，,;；(（+=\-)）~？?\w\d]*)"
        pattern = re.compile(xx)
        results = pattern.findall(new_ses)

        if results:
            # print(results)
            for word in results:
                wd = self.translate(word)
                ans.append(wd)
                key = "$t(/*{}*/'{}')".format(word, wd.get("key"))
                f = ses.find(word[0])
                if ses[f-1] == "'" or ses[f-1] == '"' or ses[f-1] == "`":
                    ses = ses.replace(ses[f-1], '', 1)
                e = ses.rfind(word[-1])
                if ses[e+1] == "'" or ses[e+1] == '"' or ses[e+1] == "`":
                    ses = ses.replace(ses[e+1], '', 1)
                ses = ses.replace(word, key, 1)
        return ses, ans


    def translate(self, word, from_='cn', to_='en'):

        if word in self.dic:
            wd = {from_: word, to_: self.dic[word][2], "key": "{}_".format(self.tag) + self.dic[word][2].replace(' ', '_')}
            return wd
        

        # 使用Google翻译翻译单词
        translateApi = "http://translate.google.cn/m?q=%s&tl=%s&sl=%s" % (word, to_, 'zh-CN')
        try:
            info = requests.get(translateApi)
        except Exception as error:
            time.sleep(1)
            info = requests.get(translateApi)
        data = info.text
        expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
        result = re.findall(expr, data)
        # if (len(result) == 0):
        #     return ""

        print("成功翻译‘{}’至‘{}’".format(word, html.unescape(result[0])))
        en = html.unescape(result[0])
        wd = {"cn": word, to_: en}

        key = "{}_".format(self.tag) + en.replace(' ', '_')
        key = key.replace("'", '')
        wd["key"] = key
        
        return wd
    