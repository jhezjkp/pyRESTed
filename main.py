#!/usr/bin/env python
#encoding=utf-8

from Tkinter import Frame, Label, Entry, Text, Button,\
    LEFT, RIGHT, TOP, BOTTOM, BOTH, YES, END
import requests


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("pyRESTed")
        #最大窗口大小
        self.master.maxsize(1000, 400)
        #窗口大小
        self.master.geometry('1000x400')
        #左边控制区域
        self.init_constrol_frame()
        #右边输出区域
        self.init_console_frame()
        #底部区域
        self.init_bottom_frame()
        self.pack()

    def init_constrol_frame(self):
        self.control_frame = Frame(self, bg='#ededed')
        self.cf_top = Frame(self.control_frame)
        #url entry
        self.url_entry = Entry(self.cf_top)
        self.url_entry.insert(0, "https://kyfw.12306.cn/otn/login/checkUser")
        self.url_entry.pack()
        self.cf_top.pack(side=TOP, expand=YES, fill=BOTH)
        self.control_frame.pack(side=LEFT, expand=YES, fill=BOTH)

    def init_console_frame(self):
        self.console_frame = Frame(self, bg='white')
        self.console_text = Text(self.console_frame)
        self.console_text.pack()
        self.console_frame.pack(side=RIGHT, expand=YES, fill=BOTH)

    def init_bottom_frame(self):
        self.bottom_frame = Frame(self, bg='#bfbfbf')
        self.send_btn = Button(self.bottom_frame, text="发送", command=self.send_btn_click)
        #处理回车
        self.send_btn.bind('<Return>', self.send_btn_return)
        self.send_btn.pack()
        self.bottom_frame.pack(side=BOTTOM, expand=YES, fill=BOTH)

    def send_btn_click(self):
        url = self.url_entry.get()
        if url:
            r = requests.get(url, verify=False)
            if r.status_code == 200:
                self.console_text.delete(1.0, END)
                self.console_text.insert(END, r.text)

    def send_btn_return(self, envent):
        self.send_btn_click()

if __name__ == '__main__':
    app = App()
    app.mainloop()
