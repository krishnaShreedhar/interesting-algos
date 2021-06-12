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
from PIL import Image
import os
from utils import files as uf


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
    for img_index, img_path in list_images:
        img = cv2.imread(img_path)
        resized = image_resize(img)


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
    to_pdf(list_images, os.path.join("../outputs/", "to_pdf.pdf"))
    to_pdf_a4(list_images, os.path.join("../outputs/", "to_pdf_a4.pdf"))
    to_pdf_dpi(list_images, os.path.join("../outputs/", "to_pdf_dpi.pdf"), 350)


def main():
    save_pdfs()


if __name__ == '__main__':
    main()
