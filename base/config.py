#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author      : Cao Zejun
# @Time        : 2024/1/29 15:59
# @File        : config.py
# @Software    : Pycharm
# @description :

import os
import cv2
import win32gui, win32con, win32print, win32api
import pyautogui

class ConfigBase:
    def __init__(self):
        self.img_map = {
            '小程序': './imgs/2560+1600/full_screen.png',
            '顶部标签栏': './imgs/2560+1600/top_tab_bar.png',
        }
        # 获取屏幕绝对分辨率，乘上缩放倍数之后的
        hDC = win32gui.GetDC(0)
        w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)  # 横向分辨率
        h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)  # 纵向分辨率
        self.windows_shape = (w, h)
        self.zoom_size = round(w / win32api.GetSystemMetrics(0), 2)
        self.resolution = pyautogui.size()
        self.resolution_ratio = (self.resolution[0] / 2560, self.resolution[1] / 1600)

        # 找到顶部标签栏剪切保存，用于后续定位
        if not os.path.exists(self.img_map['顶部标签栏']):
            full_screen_origin = cv2.imread(self.img_map['小程序'])
            full_screen = full_screen_origin.copy()
            full_screen = cv2.cvtColor(full_screen, cv2.COLOR_BGR2GRAY)
            full_screen = cv2.resize(full_screen, (int(full_screen.shape[1] // self.zoom_size), int(full_screen.shape[0] // self.zoom_size)))

            ret, full_screen = cv2.threshold(full_screen, 250, 255, cv2.THRESH_TOZERO)
            contours, hierarchy = cv2.findContours(full_screen, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contour = sorted(contours, key=lambda x: -x.shape[0])[0][:, 0, :].tolist()

            contour.sort(key=lambda x: x[0])
            x = [int(contour[0][0]*self.zoom_size), int(contour[-1][0]*self.zoom_size)]
            contour.sort(key=lambda x: x[1])
            y = [int(contour[0][1]*self.zoom_size), int(contour[-1][1]*self.zoom_size)]

            cv2.imwrite(self.img_map['顶部标签栏'], full_screen_origin[y[0]: y[1], x[0]: x[1]])
            print(f"写入{self.img_map['顶部标签栏']}完成！")

        full_screen_origin = cv2.imread(self.img_map['小程序'])
        self.game_windows_size = full_screen_origin.shape[:2][::-1]  # [w, h]