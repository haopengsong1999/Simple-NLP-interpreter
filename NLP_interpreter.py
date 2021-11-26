# -*- coding:utf-8 -*-
from tkinter import filedialog
from tkinter import *

import requests
from requests.exceptions import RequestException
import tkinter as tk
import jieba
import jieba.posseg as pseg
import pandas as pd


class NLP_interpreter():
    def __init__(self):
        # 窗口设置
        self.window = tk.Tk()  # 创建window窗口
        self.window.title("NLP处理器")  # 定义窗口名称
        self.window.resizable(0, 0)  # 禁止调整窗口大小
        self.input = tk.Entry(self.window, width=80)  # 创建一个输入框,并设置尺寸

        self.output = tk.Text(self.window, height=18)  # 创建一个文本展示框，并设置尺寸

        self.analyse = tk.Text(self.window, height=18)  # 创建一个文本展示框，并设置尺寸

        # 添加一个按钮，用于触发翻译功能
        self.t_button = tk.Button(self.window, text='分词', relief=tk.RAISED, width=10, height=1, command=self.tokenize)
        # 添加一个按钮，用于触发清空输入框功能
        self.c_button1 = tk.Button(self.window, text='清空输入', relief=tk.RAISED, width=10, height=1,
                                   command=self.clear_input)
        # 添加一个按钮，用于触发清空输出框功能
        self.c_button2 = tk.Button(self.window, text='清空输出', relief=tk.RAISED, width=10, height=1,
                                   command=self.clear_output)
        # 添加一个按钮，用于触发上传txt功能
        self.c_button3 = tk.Button(self.window, text='上传文件', relief=tk.RAISED, width=10, height=1,
                                   command=self.upload_txt)
        # 添加一个按钮，用于触发清空分析功能
        self.c_button4 = tk.Button(self.window, text='清空分析', relief=tk.RAISED, width=10, height=1,
                                   command=self.clear_analyse)
        # 添加一个按钮，用于触发全部清空功能
        self.c_button5 = tk.Button(self.window, text='全部清空', relief=tk.RAISED, width=10, height=1,
                                   command=self.clear_all)

        # 添加一张图标
        # self.image_file = tk.PhotoImage(file='py128.png')
        self.label_image = tk.Label(self.window)

    def gui_arrang(self):
        """完成页面元素布局，设置各部件的位置"""
        self.input.grid(row=0, sticky="W", padx=1)
        self.output.grid(row=1)
        self.analyse.grid(row=2)
        self.t_button.grid(row=1, column=1, padx=1)
        self.c_button1.grid(row=3, column=1, padx=1)
        self.c_button2.grid(row=4, column=1, padx=1)
        self.c_button3.grid(row=0, column=1, padx=1)
        self.c_button4.grid(row=5, column=1, padx=1)
        self.c_button5.grid(row=2, column=1, padx=1)

        self.label_image.grid(row=1, column=1, columnspan=3)

    def tokenize(self):
        original_str = self.input.get()
        '''分词output展示'''
        try:
            n = ("/".join(jieba.lcut(original_str)))
            self.output.delete(1.0, "end")  # 输出翻译内容前，先清空输出框的内容
            self.output.insert('end', n)  # 将翻译结果添加到输出框中
        except RequestException:
            self.output.insert('end', "发生错误")

        '''分词analyse展示'''
        try:
            flag_delete_list = ['x', 'uj', 'm']
            list = []
            n = ("/".join(jieba.lcut(original_str)))
            words = jieba.cut(original_str)

            words = pseg.cut(original_str)
            for w in words:
                if w.flag not in flag_delete_list:
                    list.append(w.word)

            dict = {}
            for key in list:
                dict[key] = dict.get(key, 0) + 1
            sorted(dict.items(), key=lambda item: item[1], reverse=True)
            self.analyse.delete(1.0, "end")  # 输出翻译内容前，先清空输出框的内容
            self.analyse.insert('end',
                                str(sorted(dict.items(), key=lambda item: item[1], reverse=True)))  # 将翻译结果添加到输出框中
        except RequestException:
            self.analyse.insert('end', "发生错误")

    def clear_input(self):
        """定义一个函数，用于清空输入框的内容"""
        self.input.delete(0, "end")

    def clear_output(self):
        """定义一个函数，用于清空输出框的内容"""
        self.output.delete(1.0, "end")  # 从第一行清除到最后一行

    def clear_all(self):
        self.input.delete(0, "end")
        self.output.delete(1.0, "end")  # 从第一行清除到最后一行
        self.analyse.delete(1.0, "end")

    def clear_analyse(self):
        """定义一个函数，用于清空分析框的内容"""
        self.analyse.delete(1.0, "end")  # 从第一行清除到最后一行

    def upload_txt(self):
        """定义一个函数，用于上传txt文件"""
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=[("All files", "*.*")])
        if filename.endswith(".txt"):
            print("txt")
            try:
                fin = open(filename, 'r', encoding='UTF-8')
                line = fin.readline()

                self.input.delete(0, "end")  # 将输入框清空

                ss = ''
                while line:
                    ss += line
                    line = fin.readline()

                fin.close()
                self.input.insert('end', ss)  # 将txt内容放入输入框
            except RequestException:
                self.output.insert('end', "发生错误")

        elif filename.endswith(".xlsx"):
            print("excel")
            try:
                df = pd.read_excel(filename, engine='openpyxl')
                self.input.delete(0, "end")  # 将输入框清空

                ss = ''
                ss += df.to_string(index=False).strip()
                ss = ss.strip(" ")

                self.input.insert('end', ss)  # 将txt内容放入输入框
            except RequestException:
                self.output.insert('end', "发生错误")



def main():
    t = NLP_interpreter()
    t.gui_arrang()
    tk.mainloop()


if __name__ == '__main__':
    main()
