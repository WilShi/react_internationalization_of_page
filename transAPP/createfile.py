#! -*- coding: utf-8 -*-

import csv
import os
import re


class createfile():
    def __init__(self) -> None:
        pass

    
    def mkdir(self, path):
        path = re.findall("(.*/)", path)[0]
        print("当前路径：", path)
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print("#"*50)
            print("建立新的文件路径于: {}".format(path))
            print("#"*50)


    def writeFile(self, path, file):
        self.mkdir(path)
        with open(path, 'w', encoding='UTF-8') as f:
            f.write(file)
        f.close
        print("成功写入文件至: {}".format(path))
        return path


    def writeCSV(self, path, lis):
        self.mkdir(path)
        csvfile = open(path, 'a+', encoding='UTF-8')
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
        return path