#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2019. All rights reserved.
Created by C. L. Wang on 2020/3/13
"""


def init_vid(vid_path):
    """
    初始化视频
    """
    import cv2
    cap = cv2.VideoCapture(vid_path)
    n_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    fps = int(cap.get(cv2.CAP_PROP_FPS))  # 26

    return cap, n_frame, fps, h, w


def unify_size(h, w, ms):
    """
    统一最长边的尺寸

    :h 高
    :w 宽
    :ms 最长尺寸
    """
    # 最长边修改为标准尺寸
    if w > h:
        r = ms / w
    else:
        r = ms / h
    h = int(h * r)
    w = int(w * r)

    return h, w


def get_fixes_frames(n_frame, max_gap):
    """
    等比例抽帧

    :param n_frame: 总帧数
    :param max_gap: 抽帧数量
    :return: 帧索引
    """
    from math import floor

    idx_list = []
    if n_frame > max_gap:
        v_gap = float(n_frame) / float(max_gap)  # 只使用100帧
        for gap_idx in range(max_gap):
            idx = int(floor(gap_idx * v_gap))
            idx_list.append(idx)
    else:
        for gap_idx in range(n_frame):
            idx_list.append(gap_idx)
    return idx_list


def sigmoid_thr(val, thr, gap, reverse=False):
    """
    数值归一化

    thr: 均值
    gap: 区间，4~5等分
    """
    import numpy as np
    x = val - thr
    if reverse:
        x *= -1
    x = x / gap
    sig = 1 / (1 + np.exp(x * -1))
    return round(sig, 4)  # 保留4位


def write_frames(vid_path, frames, fps, w, h):
    """
    写入视频
    :param vid_path: 输入视频的URL
    :param frames: 帧列表
    :param fps: FPS
    :param w: 视频宽
    :param h: 视频高
    :return: 写入完成的视频路径
    """
    import cv2
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # note the lower case，可以
    vw = cv2.VideoWriter(filename=vid_path, fourcc=fourcc, fps=fps, frameSize=(w, h), isColor=True)

    for frame in frames:
        vw.write(frame)

    vw.release()
    return vid_path


def save_excel_to_file(file_name, titles, res_list):
    """
    存储excel

    :param file_name: 文件名
    :param titles: title
    :param res_list: 数据
    :return: None
    """
    import xlsxwriter

    wk = xlsxwriter.Workbook(file_name)
    ws = wk.add_worksheet()

    for i, t in enumerate(titles):
        ws.write(0, i, t)

    for n_rows, res in enumerate(res_list):
        n_rows += 1
        try:
            for idx in range(len(titles)):
                ws.write(n_rows, idx, res[idx])
        except Exception as e:
            print(e)
            continue

    wk.close()
    print('[Info] 文件保存完成: {}'.format(file_name))
