# -*- coding: utf-8 -*-
import os
from os.path import join, abspath, dirname, exists
import time

import cv2

import getkeys
import grabscreen

"""
录制整体流程视频
"""
if __name__ == '__main__':

    wait_time = 5
    L_t = 3
    save_step = 200
    # file_name = 'training_data_2_3.npy'
    data_path = 'data/dataset/jianhun/images'
    window_size = (0, 0, 1280, 800)  # 384,344  192,172 96,86

    data_path = join(abspath(dirname(__file__)), data_path)

    if not exists(data_path):
        os.makedirs(data_path)

    training_data = []
    save = True
    for i in list(range(wait_time))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    counter = 0

    org_num = len(os.listdir(data_path))
    while (True):
        output_key = getkeys.get_key(getkeys.key_check())  # 按键收集
        if output_key == 100:
            if save:
                print(len(training_data) + counter * save_step)
                for i, d in enumerate(training_data):
                    file_name = os.path.join(data_path,
                                             str(org_num + counter * save_step + i) + "_" + str(d[1]) + '.jpg')
                    cv2.imwrite(file_name, d[0])
                print("save finish")
            break

        screen_gray = cv2.cvtColor(grabscreen.grab_screen(window_size), cv2.COLOR_BGRA2BGR)  # 灰度图像收集
        screen_reshape = cv2.resize(screen_gray, (1280, 800))  # 1200, 750   600, 375

        training_data.append([screen_reshape, output_key])

        if len(training_data) % save_step == 0 and save:
            print(len(training_data))
            for i, d in enumerate(training_data):
                file_name = os.path.join(data_path, str(org_num + counter * save_step + i) + "_" + str(d[1]) + '.jpg')
                cv2.imwrite(file_name, d[0])
            training_data.clear()
            counter += 1
        cv2.imshow('window1', screen_reshape)

        # 测试时间用
        print('每帧用时 {} 秒'.format(time.time() - last_time))
        print("瞬时fps：", 1 / (time.time() - last_time))
        last_time = time.time()

        if cv2.waitKey(7) & 0xFF == ord('q'):
            break
    # 等待用户按下任意键，然后关闭窗口
    cv2.waitKey()
    cv2.destroyAllWindows()
