#! -*- coding: utf-8 -*-

import re
import os
import sys
import csv
import time
import html
import requests, json
import pandas as pd

class translate():

    def __init__(self, tag) -> None:
        self.tag = tag
        self.csvpath = ''

    def translate_cn_en(self, word, cn_en_dic):

        if word in cn_en_dic:
            wd = {"cn": word, "en": cn_en_dic[word][2], "key": "{}_".format(self.tag) + cn_en_dic[word][2].replace(' ', '_')}
            return wd
        

        # 使用Google翻译翻译单词

        translateApi = "http://translate.google.cn/m?q=%s&tl=%s&sl=%s" % (word, 'en', 'zh-CN')

        # print(word, "&&"*50)

        info = requests.get(translateApi)
        data = info.text
        expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
        result = re.findall(expr, data)
        # if (len(result) == 0):
        #     return ""

        print("成功翻译‘{}’至‘{}’".format(word, html.unescape(result[0])))
        en = html.unescape(result[0])

        wd = {"cn": word, "en": en}

        key = "{}_".format(self.tag) + en.replace(' ', '_')
        key = key.replace("'", '')
        wd["key"] = key
        
        return wd


    def findChinese(self, ses, cn_en_dic):

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
                wd = self.translate_cn_en(word, cn_en_dic)

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


    def mkdir(self, path):

        path = re.findall("(.*/)", path)[0]
        print("当前路径：", path)

        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print("#"*50)
            print("建立新的文件路径于: {}".format(path))
            print("#"*50)


    def writeFile(self, path, new_file):
        self.mkdir(path)
        with open(path, 'w', encoding='UTF-8') as f:
            f.write(new_file)
        f.close
        print("成功写入文件至: {}".format(path))


    def writeCSV(self, path, lis):
        self.mkdir(path)
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
        self.duplicative_csv(path)
        self.csvpath = path


    def readFile(self, path, cn_en_dic):

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
                if '$t' not in line:
                    try:
                        ses, lis = self.findChinese(line, cn_en_dic)
                    except Exception as error:
                        print("出现了问题：{}".format(str(error)))
                        print("等待10秒重新连接网络！！！！！")
                        time.sleep(10)
                        ses, lis = self.findChinese(line, cn_en_dic)
                        
                    new_file += ses
                    if lis:
                        # print(lis)
                        log += "{} 行有改动: ".format(str(row)) + str(lis) + "\n"
                        csv_info.append(lis)
                else:
                    new_file += line
                row += 1

        print("*"*50)
        print("开始写入文件")
        print("*"*50)

        fn = path[2:path[2:].find('/')+2] if path[:2] == './' else path[:path.find('/')+2]
        self.writeCSV("new_{}/keyPage/key.csv".format(fn), csv_info)
        self.writeFile("new_{}/{}".format(fn, path), new_file)

        fileName = path[2:]
        fileName = fileName.replace('/', '_')
        fileName = fileName.replace('.', '_')
        self.writeFile("new_{}/logPage/{}_log.txt".format(fn, fileName), log)

        print("翻译成功!!!!")


    def startWork(self, new_path, cn_en_dic):
        try:
            if new_path[new_path.rfind('.')+1:] == 'js' or new_path[new_path.rfind('.')+1:] == 'jsx' or new_path[new_path.rfind('.')+1:] == 'tsx':
                print("路径 {} 的文件符合要求，开始运行程序......".format(new_path))
                self.readFile(new_path, cn_en_dic)
        except Exception as error:
            print("出现了问题：{}".format(str(error)))
            print("等待10秒重新连接网络！！！！！")
            time.sleep(10)
            if new_path[new_path.rfind('.')+1:] == 'js' or new_path[new_path.rfind('.')+1:] == 'jsx' or new_path[new_path.rfind('.')+1:] == 'tsx':
                print("路径 {} 的文件符合要求，开始运行程序......".format(new_path))
                self.readFile(new_path, cn_en_dic)


    def showJsFile(self, path, file, cn_en_dic_path):
        path = path+'/'+file
        f = os.listdir(path)
        for i in f:
            print(path+'/'+i)
            self.allFile(path+'/'+i, cn_en_dic_path)



    def allFile(self, path, cn_en_dic_path=''):
        cn_en_dic = {}
        
        if cn_en_dic_path:
            csv_reader = csv.reader(open(cn_en_dic_path))
            for line in csv_reader:
                if line:
                    cn_en_dic[line[1]] = line

        path = path.replace('\\', '/')
        
        if os.path.isdir(path):
            files = os.listdir(path)

            for file in files:
                if os.path.isdir(path + '/' + file):
                    self.showJsFile(path, file, cn_en_dic_path)
                else:
                    new_path = path + '/' + file
                    print(new_path)
                    self.startWork(new_path, cn_en_dic)
                    
        else:
            print(path)
            self.startWork(path, cn_en_dic)

        return self.csvpath

        
    def format_csv(self, path, appCode, creator):
        print("开始执行将CSV文件制作从EXCEL格式文件......")
        path = path.replace('\\', '/')

        head = ['appCode', 'langCode', 'langText', 'langType', 'createBy']
        rows = []
        csv_reader = csv.reader(open(path))

        for line in csv_reader:
            if line and line != ['Key', 'Chinese', 'English']:
                subrow = [appCode, line[0], line[1], "cn", creator]
                rows.append(subrow)
                subrow = [appCode, line[0], line[2], "en", creator]
                rows.append(subrow)

        dt = pd.DataFrame(rows, columns=head)
        # fn = path[2:path[2:].find('/')+2]
        # dt.to_excel("./{}/keyPage/lang.xls".format(fn), index=0)

        fn = path[:path.rfind('/')]
        dt.to_excel("{}/lang.xls".format(fn), index=0)

        # print(pd.read_excel("./new/keyPage/lang.xls"))
        print("="*50)
        print("Excel格式文件导出成功！！！！")
        print("="*50)


    def duplicative_csv(self, path):
        print("开始给 {} 路径的文件去重......".format(path))

        dup = []

        csv_reader = csv.reader(open(path))
        for line in csv_reader:
            if line not in dup and line:
                dup.append(line)
            else:
                print(line, " 是重复的行，将会被删除！！！！")

        if dup:
            csvfile = open(path, 'w')
            writer = csv.writer(csvfile)
            writer.writerow(dup[0])

            writer.writerows(dup[1:])
            csvfile.close

            print("="*50)
            print("成功将 {} 文件去重！！！！".format(path))
            print("="*50)


if __name__ == '__main__':


    # readFile("index.jsx")

    if len(sys.argv) > 2:
        trans = translate('WE')
        if sys.argv[1] == "test": # 本区域用于unit test
            # translate_cn_en('测试运行')
            # mkdir("new/keyPage/key.csv")
            cp = trans.allFile("testFile/index.jsx")
            print(cp, "*"*100)
            trans.format_csv(cp, "point", "Huiyong Sun")
            # duplicative_csv("./new/keyPage/key.csv")
            # format_csv("./new/keyPage/key.csv", "point", "Huiyong Sun")
            pass

        elif sys.argv[1] == "path":
            if len(sys.argv) == 4:
                trans.allFile(sys.argv[2], sys.argv[3])
            else:
                trans.allFile(sys.argv[2])

        elif sys.argv[1] == "format":
            trans.duplicative_csv(sys.argv[2])
            trans.format_csv(sys.argv[2], sys.argv[3], sys.argv[4])

        else:
            print({"error": 1, "msg": "python translate.py [test, path, format] file_path ['', dic_path(csv_file), appCode] ['', '', creator]"})

    else:
        print({"error": 1, "msg": "python translate.py [test, path, format] file_path ['', dic_path(csv_file), appCode] ['', '', creator]"})

    
