# -*- coding:utf-8 -*-
# !/usr/bin/Python3
from PIL import Image
import glob, os

'''
    glob 主要用来遍历文件 glob.glob 返回所有匹配的文件路径列表
                         glob.iglob 一次只获取一个匹配路径
'''
im1 = Image.open('qq2.png', mode='RGBA')
im2 = Image.open('qq2.png', mode='RGBA')
im = Image.alpha_composite(im1, im2)
assert isinstance(im, Image.Image)
im.show()

# rotate 45 and show
# image = Image.open('QQ图片20191230142841.png')
# image.rotate(45).show()


# create thumbnails
# size = 128, 128
# for inFile in glob.glob('*.png'):
#     file, text = os.path.splitext(inFile)
#     im = Image.open(inFile)
#     assert isinstance(im, Image.Image)
#     im.thumbnail(size, Image.ANTIALIAS)
#     im.save(file + ".jpg", "PNG")
