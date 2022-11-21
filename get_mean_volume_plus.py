# -*- coding: utf-8 -*-
import os
# import re
import sys
import subprocess

# 程序依赖 ffmpeg实现。请先安装ffmpeg并配置到环境变量后使用。（官方仓库：https://github.com/FFmpeg/FFmpeg）
# 程序功能：批量获取一个文件夹下所有文件的音频信息

# 音频文件夹路径
audio_path = ""
# 是否只显示平均音量
show_flag = 1


# 传参校验
def argv_check():
    global audio_path, show_flag
    args = sys.argv
    if len(args) == 2:
        audio_path = args[1]
    elif len(args) >= 3:
        audio_path = args[1]
        show_flag = int(args[2])
    else:
        print('请传入 需要获取平均音量的音频文件夹路径 是否只显示平均音量（是1 否0）。例如：python get_mean_volume_plus.py data 1')
        return False
    print("文件夹路径：" + audio_path)
    return True


# 遍历文件夹及其子文件夹中的文件，并存储在一个列表中
# 输入文件夹路径、空文件列表[]
# 返回 文件列表Filelist,包含文件名（完整路径）
def get_filelist(dir, Filelist):
    newDir = dir
    if os.path.isfile(dir):
        Filelist.append(dir)
        # # 若只是要返回文件文，使用这个
        # Filelist.append(os.path.basename(dir))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue
            newDir = os.path.join(dir, s)
            get_filelist(newDir, Filelist)
    return Filelist


if argv_check():
    data_list = get_filelist(audio_path, [])
    print("音频文件总数：" + str(len(data_list)))
    for file_path in data_list:
        # print(file_path)
        cmd_str = 'ffmpeg -i {0} -filter_complex volumedetect -c:v copy -f null /dev/null'
        cmd = cmd_str.format(file_path)
        # print(cmd)
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             encoding='utf-8'
                             )

        # 输出stdout
        output = p.communicate()[0]
        # 是否显示所有输出
        if show_flag != 1:
            print(output)
        if output:
            lines = output.splitlines()
            for line in lines:
                index = line.find('mean_volume: ')
                if index != -1:
                    # print(line)
                    line_arr = line.split("mean_volume: ")
                    # print(line_arr)
                    # 平均音量
                    mean_volume = float(line_arr[1][:-3])
                    print(file_path + " 平均音量：" + str(mean_volume) + "dB")
