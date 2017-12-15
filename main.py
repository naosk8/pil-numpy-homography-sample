#!/usr/bin/python
# -*- coding: utf-8 -*-

from homography import transform
import numpy as np
from PIL import Image
from argparse import ArgumentParser


if __name__ == '__main__':
    usage = 'python {} [--input file_path] [--corner_list list]' \
        ' [--dest_list list] [--output file_path] [--gray_scale] [--help]'.format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('-i', '--input', type=str, help='input image file path', required=True)
    argparser.add_argument('-c', '--corner_list', type=str, help='corner list for the crop area\n"[x1, y1, x2, y2, x3, y3, x4, y4]"', required=True)
    argparser.add_argument('-d', '--dest_list', type=str, help='destination rectangle\'s corner list(optional)')
    argparser.add_argument('-o', '--output', type=str, help='output image file path')
    argparser.add_argument('-L', '--gray_scale', action='store_true', help='output image file path')
    args = argparser.parse_args()

    img = Image.open(args.input)
    corner_list = np.array(args.corner_list.split(',')).reshape((4,2)).astype(int).tolist()
    if args.dest_list is not None:
        dest_list = np.array(args.dest_list.split(',')).reshape((4,2)).astype(int).tolist()
    else:
        dest_list = None
    if args.gray_scale is not None and args.gray_scale == True:
        img = img.convert('L')
    transformed_img = transform(img, corner_list, dest_list)
    if args.output is not None:
        transformed_img.save(args.output)
    else:
        transformed_img.show()
