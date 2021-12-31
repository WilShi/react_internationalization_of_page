#! -*- coding: utf-8 -*-

import re
import os
import sys
import csv
import html
import requests, json

# from requests.api import request

def translate_cn_en(word):
    # 使用Google翻译翻译单词

    translateApi = "http://translate.google.cn/m?q=%s&tl=%s&sl=%s" % (word, 'en', 'zh-CN')

    # print(translateApi)

    info = requests.get(translateApi)
    data = info.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    # if (len(result) == 0):
    #     return ""

    print("成功翻译‘{}’至‘{}’".format(word, html.unescape(result[0])))

    return html.unescape(result[0])


def findChinese(ses):

    ans = []

    nocomm = re.findall("(.*?)//", ses)
    
    if nocomm:
        ses = str().join(nocomm)

    xx = u"([\u4e00-\u9fff]+)"
    pattern = re.compile(xx)
    results = pattern.findall(ses)

    if results:
        # print(results)
        for word in results:
            wd = {}
            wd['cn'] = word
            new_word = str(translate_cn_en(word))
            wd['en'] = new_word
            key = 'CRM_' + new_word.replace(' ', '_')
            wd['key'] = key
            ans.append(wd)

            key = "$t(/*{}*/'".format(word) + key + "')"
            
            f = ses.find(word[0])

            if ses[f-1] == "'" or ses[f-1] == '"' or ses[f-1] == "`":
                ses = ses.replace(ses[f-1], '')

            e = ses.find(word[-1])
            if ses[e+1] == "'" or ses[e+1] == '"' or ses[e+1] == "`":
                ses = ses.replace(ses[e+1], '')

            ses = ses.replace(word, key)

        # print(ses)
        # print('**'*50)

    # else:
    #     # print(ses)
    #     print("这里没有中文")

    return ses, ans


def mkdir(path):

    path = re.findall("(.*/)", path)[0]
    print("当前路径：", path)

    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("#"*50)
        print("建立新的文件路径于: {}".format(path))
        print("#"*50)


def writeFile(path, new_file):
    mkdir(path)
    with open(path, 'w', encoding='UTF-8') as f:
        f.write(new_file)
    f.close
    print("成功写入文件至: {}".format(path))


def writeCSV(path, lis):
    mkdir(path)
    csvfile = open(path, 'a+')
    writer = csv.writer(csvfile)
    writer.writerow(['Key', 'Chinese', 'English'])

    data = []
    for i in lis:
        if len(i) == 1:
            i = i[0]
            tmp = (i["key"], i["cn"], i["en"])
            if tmp not in data:
                data.append(tmp)
        else:
            for ii in i:
                tmp = (ii["key"], ii["cn"], ii["en"])
                if tmp not in data:
                    data.append(tmp)

    # print(data)
    writer.writerows(data)
    csvfile.close
    print("成功写入文件至: {}".format(path))


def readFile(path):

    path = path.replace('\\', '/')

    print("*"*50)
    print("从 {} 路径开始读取文件".format(path))
    print("*"*50)

    log = "{}\n".format(str(path))
    row = 1

    new_file = ""
    csv_info = []

    with open(path, 'r', encoding='UTF-8') as f:
        for line in f:
            ses, lis = findChinese(line)

            new_file += ses

            if lis:
                # print(lis)
                log += "{}行有改动: ".format(str(row)) + str(lis) + "\n"
                csv_info.append(lis)
            row += 1

    print("*"*50)
    print("开始写入文件")
    print("*"*50)

    writeCSV("new/keyPage/key.csv", csv_info)

    writeFile("new/{}".format(path), new_file)

    # fileName = re.findall("[^/]+", path)[-1]
    # fileName = fileName.replace('.', '_')
    fileName = path[2:]
    fileName = fileName.replace('/', '_')
    fileName = fileName.replace('.', '_')
    writeFile("new/logPage/{}_log.txt".format(fileName), log)

    print("翻译成功!!!!")


def startWork(new_path):
    if new_path[new_path.rfind('.')+1:] == 'js' or new_path[new_path.rfind('.')+1:] == 'jsx' or new_path[new_path.rfind('.')+1:] == 'tsx':
        print("路径 {} 的文件符合要求，开始运行程序......".format(new_path))
        readFile(new_path)


def showJsFile(path, file):
    path = path+'/'+file
    f = os.listdir(path)
    for i in f:
        print(path+'/'+i)
        allFile(path+'/'+i)



def allFile(path):
    path = path.replace('\\', '/')
    
    if os.path.isdir(path):
        files = os.listdir(path)

        for file in files:
            if os.path.isdir(path + '/' + file):
                showJsFile(path, file)
            else:
                new_path = path + '/' + file
                print(new_path)
                startWork(new_path)
                
    else:
        print(path)
        startWork(path)


def duplicative_csv(path):
    print("开始给 {} 路径的文件去重......".format(path))


if __name__ == '__main__':


    # readFile("index.jsx")

    if len(sys.argv) == 3:
        if sys.argv[1] == "test": # 本区域用于unit test
            # translate_cn_en('测试运行')
            # mkdir("new/keyPage/key.csv")
            allFile(".\conditions")

        elif sys.argv[1] == "path":
            allFile(sys.argv[2])

        # elif sys.argv[1] == "dup":

    else:
        print({"error": 1, "msg": "python translate.py env path"})

    

    # TestReChinese()
