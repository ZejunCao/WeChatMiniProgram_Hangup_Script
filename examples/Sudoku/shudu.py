#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author      : Cao Zejun
# @Time        : 2024/1/8 1:12
# @File        : shudu.py
# @Software    : Pycharm
# @description :
import os

import cv2
import numpy as np

# row: 左边数字   col: 上边数字
# row = [2, '2 4', '6 6', '6 1', '1 3 1', '1 1 4', '2 1 2', '2 2 3 1', '2 3', '1 1 3', '2 3 3 2', '3 2 2 3', '2 1 5 2', '6 3', '3 5']
# col = ['2 2', '2 3 4', '3 2 3', '4 3 2', '2 2 5', '2 3 2 2', 2, 3, '1 1', '1 1 1 5', '2 1 8', '3 2 4 2', '3 1 2 2', '7 3', '1 2 2']
# row = ['1 1', '1 1', '2 2', 3, 5, 7, 9, 12, 14, '3 7 2', '2 7 1', '1 7', 5, 3, 1]
# col = [3, 3, 3, 3, '3 7', '1 9', 11, 12, 11, '1 9', '3 7', 3, 2, 3, 3]
# row = [[1, 1], [4], [4], [6], [6], [8], [2], [4]]
# col = [[1], [3], [5, 1], [8], [8], [5, 1], [3], [1]]

# row = [[int(i) for i in s.split()] if type(s) is str else [s] for s in row]
# col = [[int(i) for i in s.split()] if type(s) is str else [s] for s in col]
row = []
col = []
#
map_size = 15
# row_maxlen = max([len(i) for i in row])
# col_maxlen = max([len(i) for i in col])
row_maxlen = 0
col_maxlen = 0
map_default_str = '-'
map = np.full([map_size, map_size], map_default_str)
num = [0]
map_pos = [131, 383, 660, 917, 5, 260]  # 主棋盘左上角(x1, y1, x2, y2)， 不带行/列前数字, 最后两个为行前数字格最左边x坐标和列前数字格最上边y坐标


def map_print():
    candi_list = [1] * map_size  # col中是否有超过10的数字，需要额外多一个空格
    for i in range(map_size):
        for j in col[i]:
            if j >= 10:
                candi_list[i] = 2

    f = ''
    for i in range(1, col_maxlen + 1):
        cur_num_str = ''
        for j in range(map_size):
            if len(col[j]) >= i:
                cur_num_str += str(col[j][-i]) + ' ' + ' ' * candi_list[j]
                if col[j][-i] >= 10:
                    cur_num_str = cur_num_str[:-1]
            else:
                cur_num_str += ' ' * 2 + ' ' * candi_list[j]
        f = '     ' + '   ' * (row_maxlen - 1) + cur_num_str + '\n' + f
    print(f)

    f = ''
    for i in range(map_size):
        cur_num_str = ''
        for j in range(row_maxlen):
            if len(row[i]) >= row_maxlen - j:
                if row[i][j + len(row[i]) - row_maxlen] >= 10:
                    cur_num_str = cur_num_str[:-1]
                cur_num_str += str(row[i][j + len(row[i]) - row_maxlen]) + ' ' * 2
            else:
                cur_num_str += ' ' * 2 + ' ' * candi_list[j]
        cur_num_str += ' '
        for j in range(map_size):
            # cur_num_str += str(int(map[i][j])) + '  '
            cur_num_str += ' ' * candi_list[j] + map[i][j] + ' '
        f += cur_num_str + '\n'
    print(f)

def simple_scan(idx, is_row=True):
    map_list_tmp = np.full(map_size, 'x')  # 当前行或列的值，用'x'初始化后，循环用'o'替换
    cur_list = [set() for _ in range(map_size)]  # 扫描多次保存可能填充的值
    if is_row:
        row_col_tmp = row.copy()
        map_row_col = map[idx]
    else:
        row_col_tmp = col.copy()
        map_row_col = map[:, idx]

    if len(row_col_tmp[idx]) == 1:
        for i in range(map_size - sum(row_col_tmp[idx]) + 1):
            map_list_tmp[i: i + row_col_tmp[idx][0]] = 'o'
            if is_require(map_list_tmp, map_row_col):
                cur_list = merge_list(cur_list, map_list_tmp)
            map_list_tmp = np.full(map_size, 'x')
    elif len(row_col_tmp[idx]) == 2:
        for i in range(map_size - sum(row_col_tmp[idx]) + 1 - len(row_col_tmp[idx]) + 1):
            for j in range(i + row_col_tmp[idx][0] + 1, map_size - row_col_tmp[idx][1] + 1):
                map_list_tmp[i: i + row_col_tmp[idx][0]] = 'o'
                map_list_tmp[j: j + row_col_tmp[idx][1]] = 'o'
                if is_require(map_list_tmp, map_row_col):
                    cur_list = merge_list(cur_list, map_list_tmp)
                map_list_tmp = np.full(map_size, 'x')
    elif len(row_col_tmp[idx]) == 3:
        for i in range(map_size - sum(row_col_tmp[idx]) + 1 - len(row_col_tmp[idx]) + 1):  # 8-2+1-2+1
            for j in range(i + row_col_tmp[idx][0] + 1, map_size - sum(row_col_tmp[idx][1:]) + 1 - len(row_col_tmp[idx][1:]) + 1):
                for k in range(j + row_col_tmp[idx][1] + 1, map_size - sum(row_col_tmp[idx][2:]) + 1 - len(row_col_tmp[idx][2:]) + 1):
                    map_list_tmp[i: i + row_col_tmp[idx][0]] = 'o'
                    map_list_tmp[j: j + row_col_tmp[idx][1]] = 'o'
                    map_list_tmp[k: k + row_col_tmp[idx][2]] = 'o'
                    if is_require(map_list_tmp, map_row_col):
                        cur_list = merge_list(cur_list, map_list_tmp)
                    map_list_tmp = np.full(map_size, 'x')
    elif len(row_col_tmp[idx]) == 4:
        for i in range(map_size - sum(row_col_tmp[idx]) + 1 - len(row_col_tmp[idx]) + 1):  # 8-2+1-2+1
            for j in range(i + row_col_tmp[idx][0] + 1, map_size - sum(row_col_tmp[idx][1:]) + 1 - len(row_col_tmp[idx][1:]) + 1):
                for k in range(j + row_col_tmp[idx][1] + 1, map_size - sum(row_col_tmp[idx][2:]) + 1 - len(row_col_tmp[idx][2:]) + 1):
                    for l in range(k + row_col_tmp[idx][2] + 1, map_size - sum(row_col_tmp[idx][3:]) + 1 - len(row_col_tmp[idx][3:]) + 1):
                        map_list_tmp[i: i + row_col_tmp[idx][0]] = 'o'
                        map_list_tmp[j: j + row_col_tmp[idx][1]] = 'o'
                        map_list_tmp[k: k + row_col_tmp[idx][2]] = 'o'
                        map_list_tmp[l: l + row_col_tmp[idx][3]] = 'o'
                        if is_require(map_list_tmp, map_row_col):
                            cur_list = merge_list(cur_list, map_list_tmp)
                        map_list_tmp = np.full(map_size, 'x')
    elif len(row_col_tmp[idx]) == 5:
        for i in range(map_size - sum(row_col_tmp[idx]) + 1 - len(row_col_tmp[idx]) + 1):  # 8-2+1-2+1
            for j in range(i + row_col_tmp[idx][0] + 1, map_size - sum(row_col_tmp[idx][1:]) + 1 - len(row_col_tmp[idx][1:]) + 1):
                for k in range(j + row_col_tmp[idx][1] + 1, map_size - sum(row_col_tmp[idx][2:]) + 1 - len(row_col_tmp[idx][2:]) + 1):
                    for l in range(k + row_col_tmp[idx][2] + 1, map_size - sum(row_col_tmp[idx][3:]) + 1 - len(row_col_tmp[idx][3:]) + 1):
                        for p in range(l + row_col_tmp[idx][3] + 1, map_size - sum(row_col_tmp[idx][4:]) + 1 - len(row_col_tmp[idx][4:]) + 1):
                            map_list_tmp[i: i + row_col_tmp[idx][0]] = 'o'
                            map_list_tmp[j: j + row_col_tmp[idx][1]] = 'o'
                            map_list_tmp[k: k + row_col_tmp[idx][2]] = 'o'
                            map_list_tmp[l: l + row_col_tmp[idx][3]] = 'o'
                            map_list_tmp[p: p + row_col_tmp[idx][4]] = 'o'
                            if is_require(map_list_tmp, map_row_col):
                                cur_list = merge_list(cur_list, map_list_tmp)
                            map_list_tmp = np.full(map_size, 'x')

    for i in range(map_size):
        if is_row:
            if len(cur_list[i]) == 1 and map[idx][i] == map_default_str:
                map[idx][i] = list(cur_list[i])[0]
                num[0] += 1
        else:
            if len(cur_list[i]) == 1 and map[i][idx] == map_default_str:
                map[i][idx] = list(cur_list[i])[0]
                num[0] += 1

def merge_list(l, n):
    for i in range(len(l)):
        l[i] = l[i].union(set(n[i]))
    return l

def is_require(l1, l2):
    for i in range(map_size):
        if l2[i] != map_default_str and l1[i] != l2[i]:
            return False
    return True

def parse():
    global map, num
    map = np.full([map_size, map_size], map_default_str)
    num = [0]
    for i in range(30):
        for i in range(map_size):
            simple_scan(i, is_row=True)
        for j in range(map_size):
            simple_scan(j, is_row=False)
        map_print()
        if num[0] == map_size * map_size:
            break
    else:
        print('ocr识别错误，请检查！！！')
        return None
    return map

def parse_img_old(img_path):
    # global raw, col
    thr = 0.8
    img = cv2.imread(img_path)
    if map_size == 15:
        top_left = [131, 383]
        bottom_right = [660, 917]
        grid_size = (bottom_right[0] - top_left[0]) // map_size
        # row解析
        for i in range(map_size):
            # if i == 2:
            #     print()
            img_tmp = img[top_left[1] + i * grid_size: top_left[1] + (i + 1) * grid_size, :top_left[0]]
            cur_num = []
            for j in range(map_size+1):
                # if j == 5:
                #     print()
                img_path = f'./imgs/{map_size}_number/{j}.png'
                if os.path.exists(img_path):
                    template = cv2.imread(img_path, cv2.IMREAD_COLOR)
                    result = cv2.matchTemplate(img_tmp, template, cv2.TM_CCOEFF_NORMED)
                    pos = find_match(result, thr)
                    for p in pos:
                        cur_num.append([j] + p)
            cur_num.sort(key=lambda x: x[2])
            cur_num_new = []
            for c in cur_num:
                if not cur_num_new:
                    cur_num_new.append(c)
                else:
                    if c[2] > cur_num_new[-1][2] + 10:
                        cur_num_new.append(c)
                    else:
                        if c[3] > cur_num_new[-1][3]:
                            cur_num_new[-1] = c
            row.append([k[0] for k in cur_num_new])
            # cv_show(img_tmp)

        # col解析
        for i in range(map_size):
            img_tmp = img[260: top_left[1], top_left[0] + i * grid_size: top_left[0] + (i + 1) * grid_size]
            cur_num = []
            for j in range(map_size+1):
                img_path = f'./imgs/{map_size}_number/{j}.png'
                if os.path.exists(img_path):
                    template = cv2.imread(img_path, cv2.IMREAD_COLOR)
                    result = cv2.matchTemplate(img_tmp, template, cv2.TM_CCOEFF_NORMED)
                    pos = find_match(result, thr, axis=1)
                    for p in pos:
                        cur_num.append([j] + p)
            cur_num.sort(key=lambda x: x[1])
            cur_num_new = []
            for c in cur_num:
                if not cur_num_new:
                    cur_num_new.append(c)
                else:
                    if c[1] > cur_num_new[-1][1] + 10:
                        cur_num_new.append(c)
                    else:
                        if c[3] > cur_num_new[-1][3]:
                            cur_num_new[-1] = c
            col.append([k[0] for k in cur_num_new])
            # cv_show(img_tmp)

    print(f'row: {row}')
    print(f'col: {col}')
    global row_maxlen, col_maxlen
    row_maxlen = max([len(i) for i in row])
    col_maxlen = max([len(i) for i in col])

def find_match(res, thr, axis=0):
    '''

    :param res: 模板匹配相似度矩阵
    :param thr: 匹配阈值
    :param axis: 行/列匹配，axis=1代表匹配row（棋盘左边），axis=0代表匹配col（棋盘上边）
    :return: [[匹配左上角x坐标, 左上角y坐标, 相似度分数], []]
    '''
    # axis=0：raw
    loc_ = np.where(res >= thr)
    loc = []
    for i in zip(loc_[0], loc_[1]):
        loc.append(i)
    if not loc:
        return []
    loc.sort(key=lambda x: x[axis])
    pos = [[loc[0][0], loc[0][1], res[loc[0][0], loc[0][1]]]]
    for i in range(1, len(loc)):
        pix = [loc[i][0], loc[i][1], res[loc[i][0], loc[i][1]]]
        if pix[axis] >= pos[-1][axis] + 10:
            pos.append(pix)
        else:
            if pix[-1] > pos[-1][-1]:
                pos[-1] = pix

    return pos


def cv_show(img, name='img'):
    # img = cv2.resize(img, (int(img.shape[1]/1.5), int(img.shape[0]/1.5)))
    # 图像的显示,也可以创建多个窗口
    cv2.imshow(name,img)
    # 等待时间，毫秒级，0表示任意键终止
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def match_num(img, thr=0.9, axis=0):
    '''
    传入某一行/列前的整个数字图片，一一比对与哪个数字匹配
    :param img: 某一行/列前的整个数字图片
    :param thr: 匹配阈值
    :param axis: 行/列匹配，axis=1代表匹配row（棋盘左边），axis=0代表匹配col（棋盘上边）
    :return: 匹配的数字和坐标, [[数字, 左上角x坐标, 左上角y坐标], []]
    '''
    cur_num = []
    for j in range(map_size + 1):
        img_path = f'./imgs/{map_size}_template/{j}.png'
        if os.path.exists(img_path):
            template = cv2.imread(img_path, cv2.IMREAD_COLOR)
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            pos = find_match(result, thr, axis=axis)
            for p in pos:
                cur_num.append([j] + p)

    cur_num.sort(key=lambda x: x[axis+1])
    cur_num_new = []
    for c in cur_num:
        if not cur_num_new:
            cur_num_new.append(c)
        else:
            if c[axis+1] > cur_num_new[-1][axis+1] + 10:
                cur_num_new.append(c)
            else:
                # 两个都小于10，比概率
                if c[0] < 10 and cur_num_new[-1][0] < 10 and c[3] > cur_num_new[-1][3]:
                    cur_num_new[-1] = c
                # 两个都大于10，比概率
                elif c[0] > 10 and cur_num_new[-1][0] > 10 and c[3] > cur_num_new[-1][3]:
                    cur_num_new[-1] = c
                # 当前数大于10，上一次存储的数小于10，直接替换
                elif c[0] >= 10 and cur_num_new[-1][0] < 10:
                    cur_num_new[-1] = c
    res = [k[:3] for k in cur_num_new]
    return res


def img_transform(img, axis=0):
    '''
    对图像进行阈值分割、闭运算、轮廓提取并返回轮廓
    :param img_ori:
    :param axis: 行/列匹配，axis=1代表匹配row（棋盘左边），axis=0代表匹配col（棋盘上边）
    :return:
    '''
    ret, img1 = cv2.threshold(src=img, thresh=127, maxval=255, type=cv2.THRESH_BINARY_INV)
    # 闭运算，先膨胀，再腐蚀
    kernel = np.ones((7, 7), np.uint8)
    img1 = cv2.morphologyEx(img1, cv2.MORPH_CLOSE, kernel)
    # cv_show(img1)
    # 图像轮廓
    contours, hierarchy = cv2.findContours(img1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    positions = []
    for c in contours:
        c = np.squeeze(c, axis=1)
        pos = [np.min(c[:, 0]), np.min(c[:, 1]), np.max(c[:, 0]), np.max(c[:, 1])]  # (x1, y1, x2, y2)
        if pos[3] - pos[1] < 5:
            continue
        elif pos[2] - pos[0] < 5 or pos[3] - pos[1] > 30:
            continue
        positions.append(pos)
    return positions


def zero_judge(positions, axis=0):
    '''
    传入图像分割得到的每个数字的坐标，判断哪个位置会出现0
    :param positions:
    :param axis: 行/列匹配，axis=1代表匹配row（棋盘左边），axis=0代表匹配col（棋盘上边）
    :return:
    '''
    # axis = 1
    # positions = [[104, 18, 113, 31], [87, 18, 93, 30], [102, 62, 113, 74], [85, 62, 91, 74], [104, 106, 113, 119],
    #              [85, 106, 94, 119], [104, 150, 113, 163], [87, 150, 93, 163], [103, 194, 113, 207], [84, 194, 93, 207],
    #              [103, 239, 113, 251], [104, 283, 113, 295], [103, 327, 113, 339], [93, 371, 113, 384], [107, 415, 112, 428],
    #              [85, 415, 95, 428], [104, 459, 113, 472], [104, 503, 113, 516]]
    _gap = []  # 预热阶段，得到数字之间的间隔，用于处理数字0颜色过暗无法识别问题
    zero_index = []
    for i in range(1, len(positions)):
        if positions[i][axis] > positions[i - 1][axis] + 10:
            _gap.append(positions[i][axis] - positions[i - 1][axis])
    _gap_mean = np.mean(_gap)
    cur_pos, index = 0, 0
    for i in range(len(positions)):
        if i > 0 and positions[i][axis] < positions[i - 1][axis] + 10:
            continue
        i_add = 0
        while positions[i][axis] - cur_pos > _gap_mean * 1.3:
            zero_index.append(index + i_add)
            cur_pos += _gap_mean
            i_add += 1
        cur_pos = positions[i][axis]
        index += 1
    while map_pos[axis+2] - map_pos[axis] - cur_pos > _gap_mean * 1.3:
        zero_index.append(index)
        cur_pos += _gap_mean
        index += 1
    return zero_index

def parse_img(img_path):
    img_ori = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
    map_size_local = 1
    # 存储行和列的map_info，大小为2的列表
    map_info_row_col = []

    # 读取列上数字，col
    positions = img_transform(img[map_pos[5]: map_pos[1], map_pos[0]: map_pos[2]], axis=0)
    positions.sort(key=lambda x: x[0])
    zero_index = zero_judge(positions, axis=0)
    # 存储每列每个数字的位置和种类
    map_info = [[positions[0]]]
    for i in range(1, len(positions)):
        if positions[i][0] > positions[i - 1][0] + 10:
            map_info.append([positions[i]])
        else:
            map_info[-1].append(positions[i])
            map_info[-1].sort(key=lambda x: x[1])
    for i in zero_index:
        map_info.insert(i, [[0, 0, 0, 0, 0]])
    map_info_row_col.append(map_info)

    # 读取行前数字，row
    positions = img_transform(img[map_pos[1]:map_pos[3], 5:map_pos[0]], axis=1)
    positions.sort(key=lambda x: x[1])
    zero_index = zero_judge(positions, axis=1)
    # 存储每行每个数字的位置和种类
    map_info = [[positions[0]]]
    for i in range(1, len(positions)):
        if positions[i][1] > positions[i-1][1] + 10:
            map_size_local += 1
            map_info.append([positions[i]])
        else:
            map_info[-1].append(positions[i])
            map_info[-1].sort(key=lambda x: x[0])
    for i in zero_index:
        map_info.insert(i, [[0, 0, 0, 0, 0]])
    map_info_row_col.append(map_info)

    global map_size, row, col
    map_size = map_size_local
    print(f'map_size: {map_size}')
    grid_size = (map_pos[2] - map_pos[0]) // map_size
    if not os.path.exists(f'./imgs/{map_size}_template'):
        os.mkdir(f'./imgs/{map_size}_template')

    for col_row in range(2):
        for i in range(map_size):
            if col_row == 1:
                img_tmp = img_ori[map_pos[1] + i * grid_size: map_pos[1] + (i + 1) * grid_size, map_pos[4]: map_pos[0]]
            else:
                img_tmp = img_ori[map_pos[5]: map_pos[1], map_pos[0] + i * grid_size: map_pos[0] + (i + 1) * grid_size]
            res = match_num(img_tmp, thr=0.9, axis=col_row)
            for r_idx in range(len(res)):
                for mapinfo_idx in range(len(map_info_row_col[col_row][i])):
                    if col_row == 1:
                        dis = abs(res[r_idx][2] - map_info_row_col[col_row][i][mapinfo_idx][0])
                    else:
                        dis = abs(res[r_idx][1] - map_info_row_col[col_row][i][mapinfo_idx][1])
                    if dis < 5:
                        if map_size >= 10 and map_info_row_col[col_row][i][mapinfo_idx][2] - map_info_row_col[col_row][i][mapinfo_idx][0] > 13 and res[r_idx][0] < 10:
                            continue
                        map_info_row_col[col_row][i][mapinfo_idx].append(res[r_idx][0])

            for mapinfo_idx in range(len(map_info_row_col[col_row][i])):
                if len(map_info_row_col[col_row][i][mapinfo_idx]) == 4:
                    pos = map_info_row_col[col_row][i][mapinfo_idx]  # (x1, y1, x2, y2)
                    if col_row == 0:
                        pos_new = [map_pos[0] + pos[0], map_pos[5] + pos[1], map_pos[0] + pos[2], map_pos[5] + pos[3]]
                    else:
                        pos_new = [map_pos[4] + pos[0], map_pos[1] + pos[1], map_pos[4] + pos[2], map_pos[1] + pos[3]]
                    cv_show(img_ori[pos_new[1]-5: pos_new[3]+5, pos_new[0]-5: pos_new[2]+5])
                    n = input()
                    map_info_row_col[col_row][i][mapinfo_idx].append(int(n))
                    cv2.imwrite(f'./imgs/{map_size}_template/{n}.png', img_ori[pos_new[1]-3: pos_new[3]+3, pos_new[0]-3: pos_new[2]+3])
        row = [[l[-1] for l in k] for k in map_info_row_col[1]]
        col = [[l[-1] for l in k] for k in map_info_row_col[0]]

    print(f'row: {row}')
    print(f'col: {col}')
    global row_maxlen, col_maxlen
    row_maxlen = max([len(i) for i in row])
    col_maxlen = max([len(i) for i in col])

    return map_size


if __name__ == '__main__':
    parse_img('imgs/2560+1600/img.png')
    # while True:
    #     for i in range(map_size):
    #         simple_scan(i, is_row=True)
    #     map_print()
    #     for j in range(map_size):
    #         simple_scan(j, is_row=False)
    #     map_print()
    #     if num[0] == map_size * map_size:
    #         break