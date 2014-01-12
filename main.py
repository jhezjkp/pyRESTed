#!/usr/bin/env python
#encoding=utf-8

import Tkinter as tk
import ttk
import requests


#头部数据表格
class HeaderTable(tk.LabelFrame):

    def __init__(self, parent, rows=3, columns=3):
        tk.LabelFrame.__init__(self, parent, bg="gray")
        self.rows = rows
        self.columns = columns
        self._widgets = []
        self._checkbox_value = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                if row == 0:
                    self._checkbox_value.append(tk.IntVar())  # 占坑，无用
                    lable = tk.Label(self, text="" if column ==0 else "Header Field" if column == 1 else "Header Value")
                    lable.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(lable)
                else:
                    if column == 0:
                        self._checkbox_value.append(tk.IntVar())
                        checkbox = tk.Checkbutton(self, onvalue=1, offvalue=0,
                            variable=self._checkbox_value[row], command=lambda row=row: self.update_row_widget_state(row))
                        checkbox.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        current_row.append(checkbox)
                    elif column == 1:
                        combobox = ttk.Combobox(self, text="", values=['GET', 'POST', 'PUT', 'DELETE'], width=8)
                        combobox.grid(row=row, column=column, sticky="nsew", padx=1, pady=0)
                        current_row.append(combobox)
                    else:
                        combobox = ttk.Combobox(self, text="", values=[], width=8)
                        combobox.grid(row=row, column=column, sticky="nsew", padx=1, pady=0)
                        current_row.append(combobox)
            self._widgets.append(current_row)

        for column in range(columns):
            if column == 0:
                self.grid_columnconfigure(column, weight=1)
            else:
                self.grid_columnconfigure(column, weight=10)

    def add_row(self):
        current_row = []
        #col 1
        self._checkbox_value.append(tk.IntVar())
        checkbox = tk.Checkbutton(self, onvalue=1, offvalue=0,
            variable=self._checkbox_value[self.rows], command=lambda row=self.rows: self.update_row_widget_state(row))
        checkbox.grid(row=self.rows, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(checkbox)
        #col 2
        combobox = ttk.Combobox(self, text="", values=['GET', 'POST', 'PUT', 'DELETE'], width=8)
        combobox.grid(row=self.rows, column=1, sticky="nsew", padx=1, pady=0)
        current_row.append(combobox)
        #col 3
        combobox = ttk.Combobox(self, text="", values=[], width=8)
        combobox.grid(row=self.rows, column=2, sticky="nsew", padx=1, pady=0)
        current_row.append(combobox)
        self._widgets.append(current_row)
        #记录总行列数
        self.rows += 1
        self.columns += 1

    def update_row_widget_state(self, row):
        widget1 = self._widgets[row][1]
        widget2 = self._widgets[row][2]
        if self._checkbox_value[row].get() == 1:
            widget1.configure(state='normal')
            widget2.configure(state='normal')
        else:
            widget1.configure(state='disable')
            widget2.configure(state='disable')


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def get(self, row, column):
        widget = self._widgets[row][column]
        return widget.get()


class App(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("pyRESTed")
        #最大窗口大小
        self.master.maxsize(1000, 450)
        #窗口大小
        self.master.geometry('1000x450')
        #上面的面板
        self.top_frame = tk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.top_frame.pack(side=tk.TOP)
        #左边控制区域
        self.init_constrol_frame(self.top_frame)
        #右边输出区域
        self.init_console_frame(self.top_frame)
        #底部区域
        self.init_bottom_frame()
        self.pack()

    def init_constrol_frame(self, parent):
        self.control_frame = tk.Frame(parent)
        self.cf_top = tk.Frame(self.control_frame)
        #url entry
        self.http_url = tk.StringVar(parent, "https://kyfw.12306.cn/otn/login/checkUser")
        self.url_entry = tk.Entry(self.cf_top, text=self.http_url, width=50)
        self.url_entry.pack(side=tk.LEFT)
        #method combox
        self.http_method = tk.StringVar(self.cf_top, 'GET')
        self.method_cb = ttk.Combobox(self.cf_top, text=self.http_method, values=['GET', 'POST', 'PUT', 'DELETE'], width=8)
        self.method_cb.pack(side=tk.LEFT)
        self.cf_top.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        #header table
        self.cf_table = tk.Frame(self.control_frame)
        self.header_table = HeaderTable(self.cf_table)
        self.header_table.pack(fill=tk.BOTH)
        self.cf_table.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        #header button
        self.cf_button = tk.Frame(self.control_frame)
        self.header_add_btn = tk.Button(self.cf_button, text="+", command=lambda is_add=True: self.header_control_btn(is_add))
        self.header_add_btn.pack(side=tk.RIGHT)
        self.header_remove_btn = tk.Button(self.cf_button, text="-", command=lambda is_add=False: self.header_control_btn(is_add))
        self.header_remove_btn.pack(side=tk.RIGHT)
        self.cf_button.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.control_frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def init_console_frame(self, parent):
        self.console_frame = tk.Frame(parent)
        self.console_text = tk.Text(self.console_frame)
        #禁止输入
        self.console_text.bind("<KeyPress>", lambda e: "break")
        self.console_text.pack(padx="2m", pady="2m")
        self.console_frame.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

    def init_bottom_frame(self):
        self.bottom_frame = tk.Frame(self.master)
        self.send_btn = tk.Button(self.bottom_frame, text="发送", command=self.send_btn_click)
        #处理回车
        self.send_btn.bind('<Return>', self.send_btn_return)
        self.send_btn.pack(side=tk.RIGHT)
        self.bottom_frame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx="2m", pady="2m", ipady="1m")

    def header_control_btn(self, is_add):
        if is_add:
            self.header_table.add_row()
        else:
            pass

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
                self.console_text.delete(1.0, tk.END)
                content = self.http_method.get() + " " + self.http_url.get() + "\n\n" + r.text
            else:
                content = self.http_method.get() + self.http_url.get() + "\n" + r.text
            self.console_text.insert(tk.END, content)
            #上色
            self.console_text.tag_add("title", "1.0", "1.10")
            self.console_text.tag_config("title", foreground="blue")
            #header
            print self.header_table.get(1, 1)
            self.header_table.set(1, 2, "POST")

    def send_btn_return(self, envent):
        self.send_btn_click()

if __name__ == '__main__':
    app = App()
    app.mainloop()
