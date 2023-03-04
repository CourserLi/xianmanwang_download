#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Author: Xiaotuan

"""
下载的库可以参考：
https://www.jianshu.com/p/4ea8ba9bed71
https://www.jianshu.com/p/3d586eae7583

1. 下载漫画到文件夹中
2. 将全部漫画转换成一张 PDF
"""

import requests
import os
import re
import time
from PIL import Image
from lxml import etree
import execjs
import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

# 漫画名字（可修改）
# 漫画网址（可修改）
name = "如胶似漆小夫妻"
url = "https://www.xianmanwang.com/rujiaosiqixiaofuqi/"


# 漫画话数
all_html = requests.get(url).text
all_et = etree.HTML(all_html)
all_li = all_et.xpath('//*[@id="detail-list-select-1"]/li[1]/a/@href')
nums = int(re.search(r"\d+", all_li[0]).group()) + 1

# 在当前目录下，创建文件夹
dirs = os.listdir()
if(name not in dirs):
    os.mkdir(name)
    os.chdir(name)
    for i in range(1, nums+1):
        chapter_name = "chapter_" + str(i)
        os.mkdir(chapter_name)
    os.chdir("..")
os.chdir(name)

# 下载漫画
for num in range(nums):
    html = requests.get(url + str(num) + ".html").text
    et = etree.HTML(html)
    li = et.xpath("/html/head/script[4]/text()")[0]
    js = li
    obj = execjs.compile(js)
    result = obj.eval("picdata")
    # print(result)

    os.chdir("chapter_" + str(num+1))
    print("正在下载第" + str(num+1) + "章节内容")
    for i in range(len(result)):
        item = "https://res.xiaoqinre.com/" + result[i]
        suffix = result[i][-4:]
        f = open(str(i)+suffix, "wb")
        data = requests.get(item).content
        f.write(data)
    os.chdir("..")
f.close()
print("全部下载完成", end="\n\n")

# 将漫画转换成 PDF
print("正在将漫画转换成 PDF")
image_list=[] # 建立空白列表用于保存图片信息
for num in range(1, len(os.listdir())+1):
    os.chdir("chapter_" + str(num))
    if num==1:
        pdf_poster = Image.open(os.path.join(os.path.abspath('.'), os.listdir()[0]))#传入的第一张图片
        for i in range(1, len(os.listdir())):
            try:
                img_url = os.path.join(os.path.abspath('.'), os.listdir()[i])
                imgfile = Image.open(img_url) # 打开对应图片
            except:
                continue
            image_list.append(imgfile) # 按照文件名序号传入图片，并保存到 image_lis 列表
    else:
        for i in range(0, len(os.listdir())):
            try:
                img_url = os.path.join(os.path.abspath('.'), os.listdir()[i])
                imgfile = Image.open(img_url) # 打开对应图片
            except:
                continue
            image_list.append(imgfile) # 按照文件名序号传入图片，并保存到 image_lis 列表
    os.chdir("..")
    time.sleep(0.5)
pdf_poster.save("./" + str(name) + ".pdf", 'pdf', save_all=True, append_images=image_list) # 将列表中的图片以 pdf 格式按序保存

print("全部执行完成！！")
