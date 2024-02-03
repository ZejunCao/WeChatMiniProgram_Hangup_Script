#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author      : Cao Zejun
# @Time        : 2024/1/29 14:18
# @File        : interface.py
# @Software    : Pycharm
# @description :
import os
import time

from shudu import parse, parse_img
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

        title = '数独游戏闯关脚本'
        botton_name = ['自动完成数独']
        botton_func = [self.reward]
        self.draw_windows(title=title, botton_name=botton_name, botton_func=botton_func)
        self.root.mainloop()

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
