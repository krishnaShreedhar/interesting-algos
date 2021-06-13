"""
References:
    1. https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
    2. https://www.pyimagesearch.com/2015/02/02/just-open-sourced-personal-imutils-package-series-opencv-convenience-functions/
    3. https://www.geeksforgeeks.org/python-convert-image-to-pdf-using-img2pdf-module/
    4. https://docs.opencv.org/master/d3/df2/tutorial_py_basic_ops.html
    5.
"""

import cv2
import img2pdf
import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from utils import files as uf

DICT_COLORS = {
    'RED': [255, 0, 0],
    'GREEN': [0, 255, 0],
    'BLUE': [0, 0, 255],
}


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    """

    :param image:
    :param width:
    :param height:
    :param inter:   INTER_AREA to shrink
                    INTER_LINEAR (fast, ok) or INTER_CUBIC (slow, better) to enlarge
    :return:
    """
    # initialize the dimensions of the image to be resized and
    # grab the image size
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def resize_images(list_images):
    for img_index, img_path in enumerate(list_images):
        img = cv2.imread(img_path)
        resized = image_resize(img, width=100)
        cv2.imwrite(f"../outputs/{img_index}.jpg", resized)


def border(img, color):
    white = [255, 255, 255]
    constant = cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=white)
    constant = cv2.copyMakeBorder(constant, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=color)
    return constant


def plot_images(df_imgs):
    list_imgs = [border(cv2.imread(row["img_path"]), row["color"]) for row_index, row in df_imgs.iterrows()]
    print(type(list_imgs[0]))
    fig, axs = plt.subplots(8, 4, figsize=(10, 18))
    axs = axs.flatten()
    print(axs)
    for index, (ax, interp) in enumerate(zip(axs, list_imgs[:32])):
        print(ax)
        ax.imshow(list_imgs[index])  # , interpolation=interp)
        ax.set_title(f"index:{index}")
        ax.grid(True)


def arrange(df_imgs, batch_size=32):
    num_batches = int(math.ceil(len(df_imgs) / batch_size))
    for batch in range(num_batches):
        start = batch_size * batch
        end = start + batch_size
        if end > len(df_imgs):
            break
        plot_images(df_imgs[batch: batch + batch_size])
        plt.savefig(f"../outputs/imgs/batch_{batch}.jpg")
        plt.close()


def sub_plot_example():
    A = np.random.rand(5, 5)

    fig, axs = plt.subplots(1, 3, figsize=(10, 3))
    for ax, interp in zip(axs, ['nearest', 'bilinear', 'bicubic']):
        ax.imshow(A, interpolation=interp)
        ax.set_title(interp.capitalize())
        ax.grid(True)

    plt.show()


def mark_images(list_images):
    list_more = []
    for img_index, img_path in enumerate(list_images):
        r_int = random.randint(10, 20)
        list_more.extend([img_path] * r_int)
    list_records = []
    for img_index, img_path in enumerate(list_more):
        r_color = DICT_COLORS[random.choice(list(DICT_COLORS.keys()))]
        dict_tmp = {
            "id_img": img_index,
            "color": r_color,
            "img_path": img_path,
        }
        list_records.append(dict_tmp)
    df_images = pd.DataFrame.from_records(list_records)
    print(df_images)
    return df_images


def to_pdf(list_images, file_path):
    with open(file_path, "wb") as f:
        f.write(img2pdf.convert(list_images))


def to_pdf_a4(list_images, file_path):
    # specify paper size (A4)
    a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    with open(file_path, "wb") as f:
        f.write(img2pdf.convert(list_images, layout_fun=layout_fun))


def to_pdf_dpi(list_images, file_path, dpi=300):
    # use a fixed dpi of 300 instead of reading it from the image
    dpix = dpiy = dpi
    layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
    with open(file_path, "wb") as f:
        f.write(img2pdf.convert(list_images, layout_fun=layout_fun))


def save_pdfs():
    list_images = uf.get_all_files_glob("../data/examples_circle_detection", ["jpg"])
    # to_pdf(list_images, os.path.join("../outputs/", "to_pdf.pdf"))
    # to_pdf_a4(list_images, os.path.join("../outputs/", "to_pdf_a4.pdf"))
    # to_pdf_dpi(list_images, os.path.join("../outputs/", "to_pdf_dpi.pdf"), 350)

    resize_images(list_images)
    list_images = uf.get_all_files_glob("../outputs/", ["jpg"])
    df_imgs = mark_images(list_images)
    # sub_plot_example()
    arrange(df_imgs)
    list_images = uf.get_all_files_glob("../outputs/imgs/", ["jpg"])
    to_pdf_a4(list_images, os.path.join("../outputs/", "collate_.pdf"))
    to_pdf(list_images, os.path.join("../outputs/", "collate_2.pdf"))


def main():
    save_pdfs()


if __name__ == '__main__':
    main()
