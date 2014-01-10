#!/usr/bin/env python
#encoding=utf-8

from Tkinter import *
from ttk import *
import requests


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("pyRESTed")
        #最大窗口大小
        self.master.maxsize(1000, 400)
        #窗口大小
        self.master.geometry('1000x400')
        #上面的面板
        self.top_frame = PanedWindow(self.master, orient=HORIZONTAL)
        self.top_frame.pack(side=TOP)
        #左边控制区域
        self.init_constrol_frame(self.top_frame)
        #右边输出区域
        self.init_console_frame(self.top_frame)
        #底部区域
        self.init_bottom_frame()
        self.pack()

    def init_constrol_frame(self, parent):
        self.control_frame = Frame(parent)
        self.cf_top = Frame(self.control_frame)
        #url entry
        self.http_url = StringVar(parent, "https://kyfw.12306.cn/otn/login/checkUser")
        self.url_entry = Entry(self.cf_top, text=self.http_url, width=50)
        #self.url_entry.insert(0, "https://kyfw.12306.cn/otn/login/checkUser")
        self.url_entry.pack(side=LEFT)
        #method combox
        self.http_method = StringVar(self.cf_top, 'GET')
        self.method_cb = Combobox(self.cf_top, text=self.http_method, values=['GET', 'POST', 'PUT', 'DELETE'], width=8)
        self.method_cb.pack(side=LEFT)
        self.cf_top.pack(side=TOP, expand=YES, fill=BOTH)
        self.control_frame.pack(side=LEFT, expand=YES, fill=BOTH)

    def init_console_frame(self, parent):
        self.console_frame = Frame(parent)
        self.console_text = Text(self.console_frame)
        self.console_text.pack()
        self.console_frame.pack(side=RIGHT, expand=YES, fill=BOTH)

    def init_bottom_frame(self):
        self.bottom_frame = Frame(self.master)
        self.send_btn = Button(self.bottom_frame, text="发送", command=self.send_btn_click)
        #处理回车
        self.send_btn.bind('<Return>', self.send_btn_return)
        self.send_btn.pack(side=RIGHT)
        self.bottom_frame.pack(side=TOP, expand=YES, fill=BOTH, padx="2m", pady="2m", ipady="1m")

    def send_btn_click(self):
        url = self.url_entry.get()
        if url:
            r = None
            method = self.http_method.get()
            if method == 'GET':
                r = requests.get(url, verify=False)
            elif method == 'POST':
                r = requests.post(url, verify=False)
            elif method == 'PUT':
                r = requests.put(url, verify=False)
            else:
                r = requests.delete(url, verify=False)
            content = ""
            if r.status_code == 200:
                self.console_text.delete(1.0, END)
                content = self.http_method.get() + self.http_url.get() + "\n" + r.text
            else:
                content = self.http_method.get() + self.http_url.get() + "\n" + r.text
            self.console_text.insert(END, content)

    def send_btn_return(self, envent):
        self.send_btn_click()

if __name__ == '__main__':
    app = App()
    app.mainloop()
