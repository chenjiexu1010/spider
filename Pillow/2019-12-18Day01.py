# -*- coding:utf-8 -*-
# !/usr/bin/Python3
from PIL import Image
from PIL import ImageFilter
import os, sys, glob

im = Image.open('001.jpg', mode='r')
im.rotate(90).show()

# size = 128, 128
# for infile in glob.glob('*.jpg'):
#     file, ext = os.path.splitext(infile)
#     im = Image.open(infile)
#     im.thumbnail(size)
#     im.save(file + ".png", "JPEG")


# def roll(image, delta):
#     """Roll an image sideways."""
#     xsize, ysize = image.size
#
#     delta = delta % xsize
#     if delta == 0: return image
#
#     part1 = image.crop((0, 0, delta, ysize))
#     part2 = image.crop((delta, 0, xsize, ysize))
#     image.paste(part1, (xsize - delta, 0, xsize, ysize))
#     image.paste(part2, (0, 0, xsize - delta, ysize))
#
#     return image
# im = roll(im, 500)


# a = sys.argv[1:]
# print(a)
