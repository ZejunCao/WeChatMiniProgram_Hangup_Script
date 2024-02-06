#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author      : Cao Zejun
# @Time        : 2024/1/29 15:59
# @File        : mouse_control.py
# @Software    : Pycharm
# @description : 鼠标控制base框架

import cv2
import time
import numpy as np
from PIL import ImageGrab
import pyautogui


class MouseBase:
    def __init__(self, config):
        self.config = config

    # 模板匹配（单个），只取top1
    def template_match(self, template_path, img=None):
        if img is None:
            img = ImageGrab.grab((self.game_windows_lefttop[0], self.game_windows_lefttop[1],
                                  self.game_windows_lefttop[0] + self.config.game_windows_size[0],
                                  self.game_windows_lefttop[1] + self.config.game_windows_size[1]))
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return max_val, max_loc

    # 定位小程序窗口位置
    def locate_windows(self):
        img = ImageGrab.grab((0, 0, self.config.windows_shape[0], self.config.windows_shape[1]))
        # imgs.show()
        max_val, max_loc = self.template_match(self.config.img_map['顶部标签栏'], img)
        if max_val < 0.8:
            return False
        self.game_windows_lefttop = max_loc
        return True

    def pos_shift(self, pos):
        x, y = [int(pos[0]) + self.game_windows_lefttop[0],
                int(pos[1]) + self.game_windows_lefttop[1]]
        return x, y

    def click(self, pos):
        x, y = self.pos_shift(pos)
        pyautogui.click(x, y)

    def move(self, pos):
        x, y = self.pos_shift(pos)
        pyautogui.moveTo(x, y)

    def drag(self, pos1, pos2, t, instance):
        '''
        鼠标拖拽，移动到 pos1 后鼠标按下，拖动到 pos2 后延时 t 秒松开，若 t == -1，则不松开
        :param pos1:
        :param pos2:
        :param t:
        :return:
        '''
        self.move(pos1)
        pyautogui.mouseDown()
        self.move(pos2)
        if t == -1:
            return
        # 0.5s检测频率，检测是否按下退出
        for i in range(2 * t):
            time.sleep(0.5)
            if instance.exit():
                pyautogui.mouseUp()
                return True
        pyautogui.mouseUp()