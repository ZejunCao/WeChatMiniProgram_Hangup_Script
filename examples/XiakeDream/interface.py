#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author      : Cao Zejun
# @Time        : 2024/1/29 14:18
# @File        : interface.py
# @Software    : Pycharm
# @description :

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
            '英雄榜': './imgs/common/hero.png',
            '财富榜': './imgs/common/money.png',
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

        title = '侠客梦奖励领取脚本'
        botton_name = ['每日初始奖励', '江湖打怪']
        botton_func = [self.reward, self.high]
        self.draw_windows(title=title, botton_name=botton_name, botton_func=botton_func)
        self.root.mainloop()


    def reward(self):
        pos_list = [
            [507, 243], [336, 1080], [336, 1080], [621, 210],  # 邮件
            [520, 1180],  # 门派
            [220, 1070], [330, 670], [330, 670], [600, 240],  # 门派事务
            [332, 1070], [474, 819], [474, 819],  # 门派俸禄
            [338, 362], [135, 1053], [135, 1053], [270, 1060], [270, 1060], [576, 551],  # 门派交谈1
            [165, 581], [161, 1060], [161, 1060], [576, 551],  # 门派交谈2
            [506, 581], [161, 1060], [161, 1060], [576, 551],  # 门派交谈3
            [197, 840], [200, 1060], [161, 1060], [576, 551],  # 门派交谈4
            [500, 865], [200, 1060], [161, 1060], [576, 551],  # 门派交谈5
            [618, 1178],  # 玩法
            [128, 707], [600, 1158], [500, 800], [500, 800], [53, 183],  # 铜人阵
            [269, 1065], [534, 580], [102, 1095], [102, 1095], [102, 1095], [68, 206],  # 武馆争霸
            [400, 1065], [500, 576], [98, 1158], [98, 1158], [98, 1158], [98, 1158], [70, 207],  # 皇城争霸战
        ]
        for pos in pos_list:
            self.mouse.click(pos)
            time.sleep(2)

            if self.exit(): return

    def high(self):
        self.mouse.click([66, 1176])
        if self.exit(2): return
        # 走到最右边，点击荒兽入侵
        if self.mouse.drag([336, 837], [390, 837], 15, self): return
        if self.exit(1): return
        self.mouse.click([160, 330])
        if self.exit(1): return
        self.mouse.click([320, 1040])
        if self.exit(3): return

        # 走到最上面打怪,等待打完后点击退出
        if self.mouse.drag([320, 1053], [320, 966], 3, self): return
        for i in range(130):
            if self.exit(1): return
        self.mouse.click([330, 1170])
        if self.exit(3): return

        # 英雄榜点赞
        for i in range(100):
            if self.mouse.drag([336, 837], [280, 837], 1, self): return
            time.sleep(0.5)  # 游戏延迟补偿
            max_val, max_loc = self.mouse.template_match(self.config.img_map['英雄榜'])
            if max_val >= 0.8:
                break
            if self.exit(): return
        if self.exit(2): return
        pos_list = [max_loc, [330, 795], [330, 795], [330, 795], [330, 795], [330, 795], [330, 795], [60, 117]]
        for pos in pos_list:
            self.mouse.click(pos)
            if self.exit(2): return

        # 财富榜点赞
        for i in range(100):
            if self.mouse.drag([336, 837], [280, 837], 1, self): return
            time.sleep(0.5)  # 游戏延迟补偿
            max_val, max_loc = self.mouse.template_match(self.config.img_map['财富榜'])
            if max_val >= 0.8:
                break
            if self.exit(): return
        if self.exit(2): return
        for pos in pos_list:
            self.mouse.click(pos)
            if self.exit(2): return


if __name__ == '__main__':
    main_interface = Interface()
