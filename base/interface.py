#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author      : Cao Zejun
# @Time        : 2024/1/29 14:19
# @File        : interface.py
# @Software    : Pycharm
# @description : tkinter GUI控制界面base框架
import time
from pynput import keyboard
import threading
import tkinter as tk



class InterfaceBase:
    def __init__(self, mouse, config):
        self.mouse = mouse
        self.config = config
        self.executing = False   # 除主页面之外只能单进程执行任务，此变量记录是否有进程在执行
        self.need_close = False  # 用来判断是否按下停止键

        self.gap = int(60 * self.config.resolution_ratio[1])  # 按钮纵向间距
        self.y = int(25 * self.config.resolution_ratio[1])  # 按钮纵向坐标
        self.button_width = int(22 * self.config.resolution_ratio[0])  # 按钮宽度
        self.text_width = int(25 * self.config.resolution_ratio[0])  # 文本行宽度
        self.root = tk.Tk()
        t = threading.Thread(target=self.keyboard)
        t.start()

    def draw_windows(self, title: str, botton_name: list, botton_func: list, func_args: list=[]):
        botton_name.append('刷新小程序窗口位置')
        botton_func.append(self.detect_windows)
        botton_name.append('停止[ESC]')
        botton_func.append(self.stop_process)

        self.button_num = len(botton_name)+1 if len(botton_name)+1 > 5 else 5  # 按钮个数, 为了美观最低为5

        # 窗口左上角名称
        self.root.title(title)
        # 设置背景颜色
        self.root.configure(bg="#efefef")

        # 设置窗口大小
        win_size = f"{int(350 * self.config.resolution_ratio[0])}x{int(self.gap*self.button_num+100 * self.config.resolution_ratio[1])}+1500+200"
        self.root.geometry(win_size)

        # bd=0 设置边框宽度为0，highlightthickness=0 设置描边为0
        text_box = tk.Text(self.root, width=self.text_width, height=1, bd=0, highlightthickness=0)
        # relx,rely设置相对位置，anchor居中
        text_box.place(relx=0.5, y=self.y, anchor="center")
        # end只在之前的文本后面添加文本,其他选项有1.0,2.0等
        text_box.insert(tk.END, title)
        text_box.tag_configure("center", justify="center")
        text_box.tag_add("center", "1.0", "end")
        text_box.config(bg="#efefef")

        for i in range(len(botton_name)):
            self.y += self.gap
            if len(func_args) > i:
                button = tk.Button(self.root, text=botton_name[i], command=lambda index=i: self.start_thread(botton_func[index], func_args[index]),
                                   width=self.button_width, height=1)
            else:
                button = tk.Button(self.root, text=botton_name[i], command=lambda index=i: self.start_thread(self.wrapper, botton_func[index]),
                                   width=self.button_width, height=1)

            button.place(relx=0.5, y=self.y, anchor="center")

        self.y += self.gap * (5 - len(botton_name)) if len(botton_name)+1 < 5 else self.gap
        self.text_show = tk.Text(self.root, width=self.text_width, height=2)
        self.text_show.place(relx=0.5, y=self.y, anchor="center")

        self.detect_windows()

    # 最下方文本框打印，便于提示
    def text_write(self, s):
        self.text_show.delete("1.0", tk.END)  # 1.0代表删除整份文件
        self.text_show.update_idletasks()
        self.text_show.insert(tk.END, s)  # tk.END表示将字符串插入到文件末端位置
        self.text_show.tag_configure("center", justify="center")
        self.text_show.tag_add("center", "1.0", "end")

    def detect_windows(self):
        if self.mouse.locate_windows():
            self.text_write("已置于屏幕顶层")
        else:
            self.text_write("请将小程序置于屏幕顶层")

    # 监测按键，[ESC]及时退出
    def keyboard(self):
        def is_esc(key):
            if key == keyboard.Key.esc:
                self.stop_process()
                print('按下了esc')
        with keyboard.Listener(on_press=is_esc) as listener:
            listener.join()

    def a(self):
        for i in range(100):
            time.sleep(5)
            if self.exit(): return

    # 进程控制，保证单线程执行
    def start_thread(self, func, *args, **kwargs):
        if self.executing and args[0] != self.stop_process:
            self.text_write("请等待该进程结束或按下停止键")
            return
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.start()

    def wrapper(self, func, *args, **kwargs):
        print(threading.activeCount())
        if func != self.stop_process:
            self.executing = True
            func(*args, **kwargs)
            self.executing = False
        else:
            func(*args, **kwargs)

    # 按[ESC]或退出时，辅助进程控制变量
    def stop_process(self):
        if self.executing:
            self.need_close = True
        self.text_write("已停止！！")

    # 自编按键程序中判断是否按下[ESC]或退出
    # 代码循环中插入 if self.exit(): return
    # 若if self.exit(1): return，指定t==1，代表延时1秒后判断是否按下退出，用于复杂步骤无法for循环判断
    def exit(self, t=-1):
        if t != -1:
            time.sleep(t)
        if self.need_close:
            # self.text_write("正在退出~~")
            self.executing = False
            self.need_close = False
            return True
        else:
            return False


