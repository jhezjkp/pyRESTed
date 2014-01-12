#!/usr/bin/env python
#encoding=utf-8

import Tkinter as tk
import ttk
import requests

header_field_map = {"Accept": ["text/plain", "text/html"], 
                    "User-Agent": ["Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36", 
                                    "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0"]}


#头部数据表格
class HeaderTable(tk.LabelFrame):

    def __init__(self, parent, rows=2, columns=3):
        tk.LabelFrame.__init__(self, parent, bg="gray")
        self.rows = 0
        self.columns = columns
        self._widgets = []
        self._checkbox_value = []
        #表头
        current_row = []
        for column in range(columns):
            self._checkbox_value.append(tk.IntVar())  # 占坑，无用
            lable = tk.Label(self, text="" if column ==0 else "Header Field" if column == 1 else "Header Value")
            lable.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(lable)
        self._widgets.append(current_row)
        self.rows += 1  # 表格头算一行
        for row in range(1, rows):
            self.add_row()
        #设置各列的列宽
        for column in range(columns):
            if column == 0:
                self.grid_columnconfigure(column, weight=1)
            else:
                self.grid_columnconfigure(column, weight=10)
        #预先选定一个header头
        self._widgets[1][1].current(1)
        self.head_field_selected(None, self._widgets[1][1], self._widgets[1][2])

    def head_field_selected(self, event, name_combobox, value_combobox):
        field_name = name_combobox.get()
        if field_name is None or len(field_name.strip()) == 0:
            return
        value_combobox.configure(values=header_field_map.get(field_name))
        value_combobox.current(0)

    def add_row(self):
        current_row = []
        #col 1
        checkbox_variable = tk.IntVar()
        self._checkbox_value.append(checkbox_variable)
        checkbox = tk.Checkbutton(self, onvalue=1, offvalue=0,
            variable=self._checkbox_value[self.rows])
        checkbox.grid(row=self.rows, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(checkbox)
        #col 2
        name_combobox = ttk.Combobox(self, text="", values=header_field_map.keys(), width=8)
        name_combobox.grid(row=self.rows, column=1, sticky="nsew", padx=1, pady=0)
        current_row.append(name_combobox)
        #col 3
        value_combobox = ttk.Combobox(self, text="", values=[], width=8)
        value_combobox.grid(row=self.rows, column=2, sticky="nsew", padx=1, pady=0)
        current_row.append(value_combobox)
        self._widgets.append(current_row)
        #事件绑定
        checkbox.configure(command=lambda checkbox_variable=checkbox_variable, name_combobox=name_combobox,
                            value_combobox=value_combobox:
                            self.update_row_widget_state(checkbox_variable, name_combobox, value_combobox))
        name_combobox.bind("<<ComboboxSelected>>", lambda event: self.head_field_selected(event, name_combobox, value_combobox))
        #记录总行列数
        self.rows += 1
        self.columns += 1

    def remove_selected_rows(self):
        mark = False
        while not mark:
            for row in reversed(range(self.rows)):
                if self._checkbox_value[row].get() == 1:
                    #self.grid_columnconfigure(column, weight=1)
                    for obj in self._widgets[row]:
                        obj.destroy()
                    del self._widgets[row]
                    del self._checkbox_value[row]
                    self.rows -= 1
                    break
                if row == 0:
                    mark = True

    def update_row_widget_state(self, checkbox_variable, name_combobox, value_combobox):
        if checkbox_variable.get() == 1:
            name_combobox.configure(state='normal')
            value_combobox.configure(state='normal')
        else:
            name_combobox.configure(state='disable')
            value_combobox.configure(state='disable')


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def get(self, row, column):
        widget = self._widgets[row][column]
        return widget.get()

    def get_header_params(self):
        result = dict()
        if self.rows == 1:
            return result
        for row in range(1, self.rows):
            field_name = self._widgets[row][1].get()
            if field_name is not None and len(field_name.strip()) > 0:
                result[field_name] = self._widgets[row][2].get()
        #print result
        return result


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
            self.header_table.remove_selected_rows()

    def send_btn_click(self):
        url = self.url_entry.get()
        if url:
            headers = self.header_table.get_header_params()
            r = None
            method = self.http_method.get()
            if method == 'GET':
                r = requests.get(url, headers=headers, verify=False)
            elif method == 'POST':
                r = requests.post(url, headers=headers,  verify=False)
            elif method == 'PUT':
                r = requests.put(url, headers=headers,  verify=False)
            else:
                r = requests.delete(url, headers=headers,  verify=False)
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

    def send_btn_return(self, envent):
        self.send_btn_click()

if __name__ == '__main__':
    app = App()
    app.mainloop()
