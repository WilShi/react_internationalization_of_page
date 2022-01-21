#! -*- coding: utf-8 -*-
import csv
import os
from sys import argv
import time
from readfile import readfile
from lang import lang
from createfile import createfile
from format import format

class main():
    def __init__(self, path, tag, dic='', appCode='', creator='', outputpath='..') -> None:
        self.dic = {}
        if dic:
            csv_reader = csv.reader(open(dic))
            for line in csv_reader:
                if line:
                    self.dic[line[1]] = line

        self.tag = tag
        self.allfiles = readfile().listfiles(path)
        self.root_file = readfile().last_path(readfile().format_path(path)).replace('.', '_')
        self.path = readfile().format_path(path)
        self.csvpath = ''
        self.logpath = ''
        self.newpath = ''
        self.appCode = appCode
        self.creator = creator
        self.outputpath = outputpath

    def start(self):
        for file in self.allfiles:
            filetp = readfile().last_path(file)
            filetp = filetp[filetp.rfind('.')+1:]
            right_type = ['js', 'jsx', 'tsx']
            if filetp in right_type:
                self.transfile(file)

        format(self.csvpath).format_csv(self.appCode, self.creator)
        

    
    def transfile(self, path):
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
                        ses, lis = lang(self.dic, self.tag).transChinese(line)
                    except Exception as error:
                        print("出现了问题：{}".format(str(error)))
                        print("等待5秒重新连接网络！！！！！")
                        time.sleep(5)
                        ses, lis = lang(self.dic, self.tag).transChinese(line)
                        
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

        root_file = "{}/new_{}".format(self.outputpath, self.root_file)

        self.csvpath = createfile().writeCSV("{}/keyPage/key.csv".format(root_file), csv_info)

        subpath = readfile().sub_path(path, self.root_file) if os.path.isdir(self.path) else readfile().last_path(path)
        self.newpath = createfile().writeFile("{}/{}".format(root_file, subpath), new_file)

        fileName = subpath.replace('/', '_')
        fileName = fileName.replace('.', '_')
        self.logpath = createfile().writeFile("{}/logPage/{}_log.txt".format(root_file, subpath), log)


if __name__ == "__main__":

    f = main(argv[1], 'TEST', argv[2], "CRM", "Wilson Shi").start()
