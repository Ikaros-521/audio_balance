# -*- coding: utf-8 -*-
import os
# import re
import sys
import subprocess

# 思路参考：https://wenku.baidu.com/view/ac883e43986648d7c1c708a1284ac850ad02042e.html?_wkts_=1668941587940&bdQuery=python%E8%8E%B7%E5%8F%96%E9%9F%B3%E9%A2%91%E9%9F%B3%E9%87%8F%E5%A4%A7%E5%B0%8F
# ffmpeg参考：https://blog.csdn.net/ternence_hsu/article/details/91407681
# 遍历文件参考：https://blog.csdn.net/weixin_41521681/article/details/92768157

# 程序依赖 ffmpeg实现。请先安装ffmpeg并配置到环境变量后使用。（官方仓库：https://github.com/FFmpeg/FFmpeg）
# 如果你本地装了格式工厂，可以直接把格式工厂安装路径配置到环境变量path中（格式工厂自带ffmpeg）
# 注意：使用时请清空 out文件夹（即输出音频的文件夹）

# 待处理音频路径
audio_path = "data\\"
# 输出音频路径
out_path = "out\\"

# 目标平均音量
tgt_db = -10


# 传参校验
def argv_check():
    global audio_path, out_path, tgt_db
    args = sys.argv
    if len(args) == 2:
        tgt_db = round(float(args[1]), 1)
    elif len(args) == 3:
        tgt_db = round(float(args[1]), 1)
        audio_path = args[2]
    elif len(args) >= 4:
        tgt_db = round(float(args[1]), 1)
        audio_path = args[2]
        out_path = args[3]
    else:
        print('请依次传入 目标平均音量（默认-10dB，做为基准，实际不会调至此） 待处理音频路径（默认data\\) 输出音频路径（默认out\\） 。例如：python audio_balance.py -10 '
              'data\\ out\\')
        os.system("pause")
        return False

    print("待处理音频路径：" + audio_path)
    print("输出音频路径：" + out_path)
    print("目标平均音量：" + str(tgt_db) + "dB")
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


# 创建文件夹
def create_dir(data_list):
    for file_path in data_list:
        file_path_arr = file_path.split("\\")
        # print(file_path_arr)
        path = "out\\"
        for i in range(len(file_path_arr) - 1):
            if i == len(file_path_arr) - 2:
                path += file_path_arr[i]
                break
            else:
                path += file_path_arr[i] + "\\"
        # print("path:" + path)
        # 判断路径是否存在 存在True 不存在False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print(path + ' 创建成功')


# 音频调音处理
def audio_handle(audio_file):
    global out_path, tgt_db
    cmd_str = 'ffmpeg -i {0} -filter_complex volumedetect -c:v copy -f null /dev/null'
    cmd = cmd_str.format(audio_file)
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         encoding='utf-8'
                         )

    # 输出stdout
    output = p.communicate()[0]
    # print(output)
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
                print(audio_file + " 平均音量：" + str(mean_volume) + "dB")

                cmd_str = 'ffmpeg -i {0} -filter:a "volume={1}dB" {2}{0}'
                cmd = cmd_str.format(audio_file, round((tgt_db - mean_volume), 1), out_path)
                print(cmd)
                p = subprocess.Popen(cmd,
                                     shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     encoding='utf-8'
                                     )

                # 输出stdout
                output = p.communicate()[0]
                # print(output)
                print("转换完毕，输出至：" + out_path + audio_file)


if __name__ == '__main__':
    if argv_check():
        data_list = get_filelist(audio_path, [])
        print("待处理音频文件总数：" + str(len(data_list)))
        create_dir(data_list)
        for file_path in data_list:
            # print(file_path)
            audio_handle(file_path)

        print("运行完毕")
        os.system("pause")
