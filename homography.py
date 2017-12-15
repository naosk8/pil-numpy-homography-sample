#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ホモグラフィ変換のモジュール
以下の2点から、指定した切り出し範囲の描画内容を引き伸ばした、変換元画像と同サイズの画像を生成する。
1. 変換元画像
2. 変換元画像中の切り出し対象物の四隅(頂点)の座標と、各座標の移動先となる座標のペア
"""

import numpy as np
from PIL import Image


def transform(img, origin_corner_list, destination_corner_list=None):
    # type: (Image.Image, list, list) -> Image.Image
    """
    :param img: base image object
    :param origin_corner_list: crop corner list for the area [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    :param destination_corner_list: destination corner list for the area [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    :return: transformed image object
    """
    assert len(origin_corner_list) == 4

    if destination_corner_list is None:
        width, height = img.size
        destination_corner_list = [[0, 0], [0, height], [width, height], [width, 0]]

    # ホモグラフィ変換に必要な切り出し座標・変換先座標のパラメータを生成。
    origin_corner_list = np.array(origin_corner_list)
    origin = __convert_corner_list_to_homography_param(origin_corner_list.T)
    destination_corner_list = np.array(destination_corner_list)
    dest = __convert_corner_list_to_homography_param(destination_corner_list.T)

    # ホモグラフィ変換行列(変換先 -> 変換元 の変換用)を取得
    # いずれの切り出し座標にも通じる、変換後の座標との関係を示す数式(行列)を求めるイメージ。
    homography_matrix = __calculate_homography_matrix(origin, dest)
    # 逆行列を作る(変換元 -> 変換先 の変換用)
    inv_homography_matrix = np.linalg.inv(homography_matrix)
    inv_homography_matrix /= inv_homography_matrix[2, 2]
    homography_param = inv_homography_matrix.ravel()

    # 出力する画像サイズを計算する。変換後の画像がすっぽりと収まるサイズへと変換する。
    x_list = destination_corner_list[:, 0]
    y_list = destination_corner_list[:, 1]
    new_width = np.max(x_list) - np.min(x_list)
    new_height = np.max(y_list) - np.min(y_list)

    # 精度と負荷のバランスから、BICUBICを採用(ケースバイケース)
    # BILINEAR だと 数百x数百px の画像処理で、数十ms程度高速にはなる。
    transformed_img = img.transform(
        size=(new_width, new_height),
        method=Image.PERSPECTIVE,
        data=homography_param,
        resample=Image.BICUBIC
    )
    return transformed_img


def __calculate_homography_matrix(origin, dest):
    # type: (np.ndarray, np.ndarray) -> np.ndarray
    """
　　線形DLT法にて、 変換元を変換先に対応づけるホモグラフィ行列を求める
    :param origin: start points for homography
    :param dest: destination points for homography
    :return: calculated homography matrix(3 x 3)
    """
    assert origin.shape == dest.shape

    # 点を調整する（数値計算上重要）
    origin, c1 = __normalize(origin)  # 変換元
    dest, c2 = __normalize(dest)      # 変換先
    # 線形法のための行列を作る。対応ごとに2つの行になる。
    nbr_correspondences = origin.shape[1]
    a = np.zeros((2 * nbr_correspondences, 9))
    for i in range(nbr_correspondences):
        a[2 * i] = [-origin[0][i], -origin[1][i], -1, 0, 0, 0, dest[0][i] * origin[0][i], dest[0][i] * origin[1][i],
                    dest[0][i]]
        a[2 * i + 1] = [0, 0, 0, -origin[0][i], -origin[1][i], -1, dest[1][i] * origin[0][i], dest[1][i] * origin[1][i],
                        dest[1][i]]
    u, s, v = np.linalg.svd(a)
    homography_matrix = v[8].reshape((3, 3))
    homography_matrix = np.dot(np.linalg.inv(c2), np.dot(homography_matrix, c1))
    homography_matrix = homography_matrix / homography_matrix[2, 2]
    return homography_matrix


def __normalize(point_list):
    # type: (np.ndarray) -> (np.ndarray, np.ndarray)
    """
    正規化処理
    :param point_list: point list to be normalized
    :return: normalization results
    """
    m = np.mean(point_list[:2], axis=1)
    max_std = max(np.std(point_list[:2], axis=1)) + 1e-9
    c = np.diag([1 / max_std, 1 / max_std, 1])
    c[0][2] = -m[0] / max_std
    c[1][2] = -m[1] / max_std
    return np.dot(c, point_list), c


def __convert_corner_list_to_homography_param(point_list):
    # type: (np.ndarray) -> np.ndarray
    """ 点の集合（dim * n の配列）を同次座標系に変換する
    :param point_list: point list to be converted to homography parameters
    :return: matrix of homography param (3 x N). N = width x height.
    """
    return np.vstack((point_list, np.ones((1, point_list.shape[1]))))

