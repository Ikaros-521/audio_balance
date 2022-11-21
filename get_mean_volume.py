# -*- coding: utf-8 -*-
import os
# import re
import sys
import subprocess

# 程序依赖 ffmpeg实现。请先安装ffmpeg并配置到环境变量后使用。（官方仓库：https://github.com/FFmpeg/FFmpeg）

# 音频文件路径
audio_file = ""


# 传参校验
def argv_check():
    global audio_file
    args = sys.argv
    if len(args) >= 2:
        audio_file = args[1]
        print("文件路径：" + audio_file)
    else:
        print('请传入需要获取平均音量的音频文件路径。例如：python get_mean_volume.py data/origin.mp3')
        return


argv_check()

cmd_str = 'ffmpeg -i {0} -filter_complex volumedetect -c:v copy -f null /dev/null'
cmd = cmd_str.format(audio_file)
print(cmd)
p = subprocess.Popen(cmd,
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     encoding='utf-8'
                     )

# 输出stdout
output = p.communicate()[0]
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
            print(audio_file + " 平均音量：" + str(mean_volume) + "dB")
