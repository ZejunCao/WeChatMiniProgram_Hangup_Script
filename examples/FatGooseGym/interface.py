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
            '进入主棋盘按钮': './imgs/2560+1600/main_chessboard_enter.png',
            '广告资源': './imgs/2560+1600/adver_resource.png',
            '广告能量': './imgs/2560+1600/adver_energy.png',
        })
        self.pos_map = {
            '会员档案': (618, 507),
            '卡牌总数': (98, 1060),
            '抽卡1': (470, 530),
            '抽卡2': (470, 720),
            '抽卡3': (470, 900),
            '抽卡继续': (320, 1100),
            '福利中心': (66, 450),
            '免费礼物': (470, 250),
            '广告观看键': (200, 1010),
            '广告退出键': (606, 111),
            '广告退出后好的键': (330, 910),
            '进入主棋盘按钮': [[35, 1040], [120, 1130]],  # 此为截图使用，记录进入主棋盘按钮边框坐标
            '广告资源': [[350, 350], [510, 460]],
            '广告能量': [[350, 570], [510, 700]],
            '免费礼物拖拽': [[330, 440], [330, 1000]]
        }


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
        botton_name = ['点击自动看资源广告', '点击自动看能量广告', '点击自动抽取卡牌']
        botton_func = [self.advertisement, self.advertisement, self.draw_card]
        func_args = ['广告资源', '广告能量', '']
        self.draw_windows(title=title, botton_name=botton_name, botton_func=botton_func, func_args=func_args)
        self.root.mainloop()

    def is_main_screen(self):
        max_val, max_loc = self.mouse.template_match(self.config.img_map['进入主棋盘按钮'])
        if max_val < 0.8:
            return False
        return True

    def draw_card(self):
        if not self.is_main_screen():
            self.text_write('请退回到主页面')
            return
        self.text_write('正在抽卡中!!!')
        # 放到动作集中，每个列表代表[点击位置，点击后延时时间]
        action_set = [
            [self.config.pos_map['会员档案'], 1],
            [self.config.pos_map['卡牌总数'], 1],
            [self.config.pos_map['抽卡1'], 4],
            [self.config.pos_map['抽卡继续'], 1],
                      ]
        start = 0
        while True:
            for action in action_set[start:]:
                # print(action)
                if start == 0:
                    start = 2
                self.mouse.click(action[0])
                if self.exit(action[1]): return

    def advertisement(self, kind):
        action_set = [
            [self.config.pos_map['福利中心'], 1],
            [self.config.pos_map['免费礼物'], 1],
                      ]
        for action in action_set:
            self.mouse.click(action[0])
            if self.exit(action[1]): return

        # if not os.path.exists(self.config.img_map['广告资源']) or not os.path.exists(self.config.img_map['广告能量']):
        #     for _ in range(2):
        #         self.mouse.drag(self, self.config.pos_map['免费礼物拖拽'][0], self.config.pos_map['免费礼物拖拽'][1], duration=0.2)
        #     self.mouse.config.printscreen('广告资源', pos=self.mouse.pos)
        #     self.mouse.config.printscreen('广告能量', pos=self.mouse.pos)

        while True:
            max_val, max_loc = self.mouse.template_match(self.config.img_map[kind])
            if max_val < 0.9:
                self.mouse.drag(self, self.config.pos_map['免费礼物拖拽'][0], self.config.pos_map['免费礼物拖拽'][1], delay=1, duration=0.2)
                self.mouse.drag(self, self.config.pos_map['免费礼物拖拽'][0], self.config.pos_map['免费礼物拖拽'][1], delay=1, duration=0.2)
                if self.exit(1): return
                # print(f'当前界面没有广告资源，max_val={max_val}')
            else:
                break
        adver_w = self.config.pos_map[kind][1][0] - self.config.pos_map[kind][0][0]
        adver_h = self.config.pos_map[kind][1][1] - self.config.pos_map[kind][0][1]
        click_pos_x = max_loc[0] + adver_w // 2
        click_pos_y = max_loc[1] + adver_h * 3 // 4
        for i in range(5):
            self.mouse.click([click_pos_x, click_pos_y])
            if self.exit(0.5): return
            self.mouse.click(self.config.pos_map['广告观看键'])
            if self.exit(35): return
            self.mouse.click(self.config.pos_map['广告退出键'])
            if self.exit(2): return
            self.mouse.click(self.config.pos_map['广告退出后好的键'])
            if self.exit(2): return




if __name__ == '__main__':
    main_interface = Interface()
