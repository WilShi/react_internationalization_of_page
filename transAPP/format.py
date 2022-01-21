#! -*- coding: utf-8 -*-
import csv
from sys import argv
from readfile import readfile
import pandas as pd

class format():
    def __init__(self, path) -> None:
        self.path = readfile().format_path(path)


    def format_csv(self, appCode, creator):
        self.duplicative_csv()
        print("开始执行将CSV文件制作从EXCEL格式文件......")

        head = ['appCode', 'langCode', 'langText', 'langType', 'createBy']
        rows = []
        csv_reader = csv.reader(open(r'%s'%self.path, encoding='utf-8'))

        for line in csv_reader:
            if line and line != ['Key', 'Chinese', 'English']:
                subrow = [appCode, line[0], line[1], "cn", creator]
                rows.append(subrow)
                subrow = [appCode, line[0], line[2], "en", creator]
                rows.append(subrow)

        dt = pd.DataFrame(rows, columns=head)

        fn = self.path[:self.path.rfind('/')]
        dt.to_excel("{}/lang.xls".format(fn), index=0)

        print("="*50)
        print("Excel格式文件导出成功！！！！")
        print("="*50)


    def duplicative_csv(self):
        print("开始给 {} 路径的文件去重......".format(self.path))

        dup = []

        csv_reader = csv.reader(open(self.path, encoding='utf-8'))
        for line in csv_reader:
            if line not in dup and line:
                dup.append(line)
            else:
                print(line, " 是重复的行，将会被删除！！！！")

        if dup:
            csvfile = open(self.path, 'w', encoding='utf-8')
            writer = csv.writer(csvfile)
            writer.writerow(dup[0])

            writer.writerows(dup[1:])
            csvfile.close

            print("="*50)
            print("成功将 {} 文件去重！！！！".format(self.path))
            print("="*50)


if __name__ == "__main__":
    f = format(argv[1])
    f.format_csv("TEST", "Wilson")
