import cv2
import os
import numpy as np
import argparse
import pytesseract.pytesseract
from pytesseract import image_to_string, image_to_boxes
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def fuck_up_image(img, filename):
    HSV_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(HSV_img)
    v = cv2.GaussianBlur(v, (1, 1), 0)
    thresh = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite('{}.png'.format(filename), thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(10, 10))
    thresh = cv2.dilate(thresh, kernel)
    return thresh

def show_found_text(img):
    img = cv2.resize(img, (600, 360))
    hImg, wImg = img.shape

    boxes = image_to_boxes(img, lang='eng', config='--psm 12 --oem 3 -c tessedit_char_whitelist=0123456789')
    for b in boxes.splitlines():
        b = b.split(' ')
    # print(b)
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
    cv2.putText(img, b[0], (x, hImg - y + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 205, 50), 1)

    cv2.imshow('Detected text', img)
    cv2.waitKey(0)

def getText(full_path, filename):
    img = cv2.imread(f"{full_path}\\{filename}")
    # gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # try_out = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    thresher = fuck_up_image(img, filename)
    # show_found_text(thresher)
    txt = image_to_string(thresher, lang='eng', config='--psm 6 digits')
    # txt = image_to_string(thresh)
    print(txt)
    return txt


def do_stuff(skip_video_cap):
    # parse all args
    source = "video_origin/aztec_786000_dmg.mp4"
    destination = "frame_destination/"

    # get file path for desired video and where to save frames locally

    path_to_save = os.path.abspath(destination)
    current_frame = 1

    files = []
    if not skip_video_cap:
        cap = cv2.VideoCapture(source)
        if (cap.isOpened() == False):
            print('Cap is not open')
        # cap opened successfully
        while (cap.isOpened()):

            # capture each frame
            ret, frame = cap.read()
            if (ret == True):

                # Save frame as a jpg file
                name = 'frame' + str(current_frame) + '.jpg'
                print(f'Creating: {name}')
                cv2.imwrite(os.path.join(path_to_save, name), frame)
                files.append(name)
                # keep track of how many images you end up with
                current_frame += 1

            else:
                break

        # release capture
        cap.release()

    # manual_file = files[228]
    manual_file = "frame_8297.png"
    getText(path_to_save, manual_file)
    print('done')


if __name__ == '__main__':
    print("HELLO")
    do_stuff(True)
