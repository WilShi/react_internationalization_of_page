import re
import os
import sys
import csv
import time
import html
import requests, json
import pandas as pd
import execjs as ex
from react import jsx
import xml.sax as sax
import xml.sax.handler as saxh

import xml.dom.minidom


def find_render(path):
    path = path.replace('\\', '/')

    print("*"*50)
    print("从 {} 路径开始读取文件".format(path))
    print("*"*50)

    # with open(path, 'r', encoding='UTF-8') as f:
    #     # s = f.read()
    #     # print(s)
    #     # print(re.findall('return.*\n*.*<([a-z]+)*[^/]*.*\n*.*>', s))
        
    #     for line in f:
    #         if "return" in line or '<' in line or '>' in line and "=>" not in line:
    #             print(line)

    # jsx.execjs(path)
    jsx.transform_string(path)
    # parser = sax.make_parser()
    # parser.setFeature(saxh.feature_namespaces, 0)
    # dom = xml.dom.minidom.parse(path)
    # root = dom.documentElement
    # print("nodeName：",root.nodeName)




if __name__ == "__main__":

    # try:
    #     find_render("./new_/index.jsx")
    #     # find_render("./modules/crowdPackage/index.tsx")
    # except Exception as error:
    #     print(error)

    find_render("./new_/index.jsx")
