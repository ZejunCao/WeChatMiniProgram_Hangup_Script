#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author      : Cao Zejun
# @Time        : 2024/1/29 14:18
# @File        : interface.py
# @Software    : Pycharm
# @description :
import os
import time

from base.interface import InterfaceBase
from base.config import ConfigBase
from base.mouse_control import MouseBase

'''
pip install pyautogui
pip install opencv-python==4.5.1.48
pip install pywin32
pip install Pillow
豆瓣源：-i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple
'''


# 继承，用于特定任务的新函数创建
class Config(ConfigBase):
    def __init__(self):
        super().__init__()
        self.img_map.update({
            '通关棋盘文件夹': './imgs/2560+1600',
        })


# 继承，用于特定任务的新函数创建
class Mouse(MouseBase):
    def __init__(self, config):
        super().__init__(config)


class Interface(InterfaceBase):
    def __init__(self):
        self.config = Config()
        self.mouse = Mouse(self.config)
        super().__init__(self.mouse, self.config)

        title = '肥鹅健身房自动化脚本'
        botton_name = ['点击自动看资源广告', '点击自动看能量广告']
        botton_func = [self.advertisement]
        func_args = ['广告资源', '广告能量']
        self.draw_windows(title=title, botton_name=botton_name, botton_func=botton_func, func_args=func_args)
        self.root.mainloop()

    def draw_card(self):
        if not self.mouse.is_main_screen():
            self.text_write('请退回到主页面')
            print('未在主页面')
            return
        self.executing = True
        self.text_write('正在抽卡中!!!')
        # 放到动作集中，每个列表代表[点击位置，点击后延时时间]
        action_set = [
            [pos_map['会员档案'], 1],
            [pos_map['卡牌总数'], 1],
            [pos_map['抽卡1'], 4],
            [pos_map['抽卡继续'], 1],
                      ]
        start = 0
        while True:
            for action in action_set[start:]:
                print(action)
                if start == 0:
                    start = 2
                self.mouse.click(action[0])
                time.sleep(action[1])
                if self.exit(): return

    def advertisement(self, kind):
        action_set = [
            [pos_map['福利中心'], 1],
            [pos_map['免费礼物'], 1],
                      ]
        for action in action_set:
            self.mouse.click(action[0])
            time.sleep(action[1])
            if self.exit(): return

        if not os.path.exists(img_map['广告资源']) or not os.path.exists(img_map['广告能量']):
            for _ in range(2):
                pyautogui.moveTo(pos_map['免费礼物拖拽'][0])
                pyautogui.mouseDown()
                pyautogui.dragTo(pos_map['免费礼物拖拽'][1], duration=0.2)
                pyautogui.mouseUp()
            self.mouse.config.printscreen('广告资源', pos=self.mouse.pos)
            self.mouse.config.printscreen('广告能量', pos=self.mouse.pos)

        if kind == '广告资源':
            img = ImageGrab.grab(self.mouse.pos)
            max_val, max_loc = self.mouse.template_match(img_map['广告资源'], img)
            if max_val < 0.8:
                print(f'当前界面没有广告资源，max_val={max_val}')
                return False
            adver_w = pos_map['广告资源'][1][0] - pos_map['广告资源'][0][0]
            adver_h = pos_map['广告资源'][1][1] - pos_map['广告资源'][0][1]
            click_pos_x = max_loc[0] + adver_w // 2
            click_pos_y = max_loc[1] + adver_h * 3 // 4
            self.mouse.click([click_pos_x, click_pos_y])
            time.sleep(0.5)
            self.mouse.click(pos_map['广告观看键'])

    def reward(self):
        # 找到最新复制进去的图片
        files = os.listdir(self.config.img_map['通关棋盘文件夹'])
        files = [f for f in files if f not in ['full_screen.png', 'top_tab_bar.png']]
        files.sort()
        map_size = parse_img(os.path.join(self.config.img_map['通关棋盘文件夹'], files[-1]))
        self.map = parse()
        if self.map is None:
            return
        top_left = [131, 383]
        bottom_right = [660, 917]
        grid_size = (bottom_right[0] - top_left[0]) // map_size
        pos = [0, 0]
        for i in range(map_size):
            for j in range(map_size):
                if self.map[i][j] == 'o':
                    pos[0] = top_left[0] + grid_size * j + grid_size // 2
                    pos[1] = top_left[1] + grid_size * i + grid_size // 2
                    self.mouse.click(pos)
                    time.sleep(0.05)

                    if self.exit(): return



if __name__ == '__main__':
    main_interface = Interface()
