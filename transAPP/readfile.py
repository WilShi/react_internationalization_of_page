#! -*- coding: utf-8 -*-
import os
from sys import argv

class readfile():

    def __init__(self) -> None:
        self.files = []

    def allfile(self, path) -> None:
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                new_file = path+'/'+file
                if os.path.isdir(new_file):
                    self.allfile(new_file)
                else:
                    self.files.append(new_file)
        else:
            self.files.append(path)

    def listfiles(self, path) -> list:
        path = self.format_path(path)
        self.allfile(path)
        return self.files

    def format_path(self, path) -> str:
        path = os.path.abspath(path)
        path = path.replace('\\', '/')
        path = path.replace('//', '/')
        path = path[:-1] if path[-1] == '/' else path
        return path

    def last_path(self, path) -> str:
        path = path[path.rfind('/')+1:]
        return path

    def sub_path(self, path, rootpath) -> str:
        path = path[path.find(rootpath)+len(rootpath):]
        path = path[1:] if path[0] == '/' else path
        return path


if __name__ == "__main__":
    f = readfile()
    a = f.listfiles(argv[1])

    for i in a:
        print(i)
        # print(f.last_path(i))



