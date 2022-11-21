# 前言
<div align="center">

# audio_balance
  
_✨ 基于ffmpeg开发的多音频文件音量均衡程序 ✨_
  

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/tkgs0/nonebot-plugin-antiinsult.svg" alt="license">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
</a>

</div>

## 使用说明
Python：3.9+  
程序依赖 ffmpeg实现。请先安装ffmpeg并配置到环境变量后使用。（官方仓库：https://github.com/FFmpeg/FFmpeg）  
如果你本地装了格式工厂，可以直接把格式工厂安装路径配置到环境变量path中（格式工厂自带ffmpeg）  
注意：使用时请清空 out文件夹（即输出音频的文件夹）

## 使用参考

### 1、获取期待音量分贝
使用 `get_mean_volume.py` 获取音频文件平均音量。此处建议传入你认为合适音量的音频文件获取信息，以做为基准。
```
# 打开cmd，在工程路径下运行以下命令，其中 data/origin.mp3 为需要解析的音频文件
python get_mean_volume.py data/origin.mp3
```

命令执行返回关键内容截取    
```
[Parsed_volumedetect_0 @ 000001d73eb72840] n_samples: 5329246
[Parsed_volumedetect_0 @ 000001d73eb72840] mean_volume: -20.7 dB
[Parsed_volumedetect_0 @ 000001d73eb72840] max_volume: -2.0 dB
[Parsed_volumedetect_0 @ 000001d73eb72840] histogram_2db: 57
[Parsed_volumedetect_0 @ 000001d73eb72840] histogram_3db: 390
[Parsed_volumedetect_0 @ 000001d73eb72840] histogram_4db: 1226
[Parsed_volumedetect_0 @ 000001d73eb72840] histogram_5db: 3330
[Parsed_volumedetect_0 @ 000001d73eb72840] histogram_6db: 6770
id3v2_parse

data/origin.mp3 平均音量：-20.7dB
```

### 2、执行多音频均衡
在步骤1中我们看到 data\origin.mp3的mean_volume（平均音量）为 -20.7dB，我们期望音量为 -10dB。
```
# 打开cmd，在工程路径下运行以下命令
# 请依次传入 目标平均音量（默认-10dB，做为基准，实际不会调至此） 待处理音频路径（默认data\) 输出音频路径（默认out\）
python audio_balance.py -10 data\ out\
```

运行完毕后输出内容  
```
待处理音频路径：data\
输出音频路径：out\
目标平均音量：-10.0dB
待处理音频文件总数：4
out\data\1 创建成功
data\1\origin.mp3 平均音量：-20.7dB
ffmpeg -i data\1\origin.mp3 -filter:a "volume=10.7dB" out\data\1\origin.mp3
转换完毕，输出至：out\data\1\origin.mp3
data\high.mp3 平均音量：-11.1dB
ffmpeg -i data\high.mp3 -filter:a "volume=1.1dB" out\data\high.mp3
转换完毕，输出至：out\data\high.mp3
data\low.mp3 平均音量：-30.7dB
ffmpeg -i data\low.mp3 -filter:a "volume=20.7dB" out\data\low.mp3
转换完毕，输出至：out\data\low.mp3
data\origin.mp3 平均音量：-20.7dB
ffmpeg -i data\origin.mp3 -filter:a "volume=10.7dB" out\data\origin.mp3
转换完毕，输出至：out\data\origin.mp3
运行完毕
请按任意键继续. . .`
```

然后可以使用 `get_mean_volume.py` 再获取下输出文件的平均音量查看情况


### 3、批量查看文件夹下音频信息（平均音量等）
在步骤1中我们只看了一个，如果你觉得看起来有点慢，基准文件需要批量参考，可以使用这个命令
```
# 打开cmd，在工程路径下运行以下命令
# 请传入 需要获取平均音量的音频文件夹路径 是否只显示平均音量（是1 否0）
python get_mean_volume_plus.py data\ 1
```

输出内容  
```
文件夹路径：data\
音频文件总数：4
data\1\origin.mp3 平均音量：-20.7dB
data\high.mp3 平均音量：-11.1dB
data\low.mp3 平均音量：-30.7dB
data\origin.mp3 平均音量：-20.7dB
```

# 参考文档
思路参考：https://wenku.baidu.com/view/ac883e43986648d7c1c708a1284ac850ad02042e.html?_wkts_=1668941587940&bdQuery=python%E8%8E%B7%E5%8F%96%E9%9F%B3%E9%A2%91%E9%9F%B3%E9%87%8F%E5%A4%A7%E5%B0%8F  
ffmpeg参考：https://blog.csdn.net/ternence_hsu/article/details/91407681  
遍历文件参考：https://blog.csdn.net/weixin_41521681/article/details/92768157  