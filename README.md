# react_internationalization_of_page

# 本脚本是帮助简化React页面制作国际化的过程

1. 使用本脚本前需要自行将jsx文件内xml格式字段的中文变更为 {“滚滚长江东逝水”} 格式

2. 本脚本目前是使用google翻译进行翻译，所以在中国境内使用本脚本需要使用翻墙工具 (后期迭代将会加入百度翻译的api以优化使用体验)

3. 本脚本使用到的依赖有：re，os, sys, csv, time, html, requests, json, panads

4. 启动本脚本需要有python 2.7及以上的环境

5. 脚本使用方式：python translate.py [test, path, format] file_path ['', dic_path(csv_file), appCode] ['', '', creator]

6. test指令仅用作测试，请勿使用

7. path指令是将输入的文件路径下的文件进行国际化标注和生成字典，如有现有字典可以再文件的路径后面再协商现有字典的路径

8. format指令是将国际化后生成的CSV指定去重并且转换成用来上传数据库的xls格式文件，执行时需要输入appCode和操作人姓名

如在操作时遇到任何困难或者发现bug欢迎与我联系
