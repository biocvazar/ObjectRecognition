from  functools import reduce
import os
import sys
import cv2
import numpy
import operator

__author__ = 'Bio'

import math


def to_total(lst:list):
    total = 0
    for i in range(len(lst)):
        total += lst[i] ** 2 * lst.index(lst[i])
    return (total / len(lst)) ** 0.5

# def invert(lst):
#     return map(lambda x: 255 if x == 0 else 0, lst)

# class VectorCompare:
#     def magnitude(self, concordance):
#         total = 0
#         try:
#             lst = list(concordance.values())
#             lst = invert(lst)
#             for i in lst:
#                 total += int(i) ** 2
#             return total**0.5
#         except Exception as e:
#             print(e, total)
#             return 1
#
#
#     def relation(self, concordance1, concordance2):
#         topvalue = 0
#         for i1, i2 in zip(concordance1.values(), concordance2.values()):
#             i1 = 0 if i1 == 255 else 255
#             i2 = 0 if i2 == 255 else 255
#             topvalue += i1 * i2
#         return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
def buildvector(im):
        d1 = {}
        count = 0
        for i in im.getdata():
            d1[count] = i
            count += 1
        return d1

def invert(number):
    if number:
        return 0
    else:
        return 255

class VectorCompare:

    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += invert(count) ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += invert(count) * invert(concordance2[word])
        try:
            return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
        except Exception as e:
            return 0

from PIL import Image
import hashlib
import time


def recognize(file_name, flag=False, path='.'):
    im = Image.open(file_name).convert('LA')
    im2 = Image.new("P", im.size, 255)
    # im2.save("text.gif")
    # im = Image.open("text.gif")
    # im2 = Image.new("P", im.size, 255)
    # im = im.convert('P', colors=5)

    temp = {}
    pixels = im.load()

    # print(im.histogram())

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            if sum(pixels[y, x]) / 3 > 127:
                pixels[y, x] = (255, 255)
            else:
                pixels[y, x] = (0, 0)

    im = im.convert('P')

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            temp[pix] = pix
            # print(x, y, pix)
            if pix <= 200:  # these are the numbers to get
                im2.putpixel((y, x), 0)

    im2.save("text.gif")

    inletter = False
    foundletter = False
    start = 0
    end = 0

    letters = []
    spaces = []
    end_space = start_space = 0
    print(im2.size[0], im2.size[1])
    lines = [0]
    for y in range(im2.size[1]):
        for x in range(im2.size[0]):
            # print(x, y)
            if im2.getpixel((x, y)) == 255:
                if x + 1 == im2.size[1]:
                    lines.append(y)
                    # print(y)
                    break
            else:
                break

    print(lines)
    line = []
    for i in range(len(lines) - 1):
        if lines[i + 1] - lines[i] > 5:
            line.append(lines[i])
            line.append(lines[i+1])

    # del line[0]
    print(line)
    # sys.exit()
    for i in range(len(line) - 1):
        start_x = 0
        start_y = 0
        y_mx_mn = []
        for x in range(im2.size[0]):  # slice across
            for y in range(line[i], line[i + 1] + 1):  # slice down
                pix = im2.getpixel((x, y))
                if pix <= 220:
                    y_mx_mn.append(y)
                    inletter = True
                    print(y)
            # print(y_mx_mn)
            if not y_mx_mn:
                continue
            if foundletter == False and inletter == True:
                foundletter = True
                start_x = x
                # start_y = min(y_mx_mn)#line[i]
                end_space = x - 1
                if end_space > start_space:
                    spaces.append(len(letters))
            if foundletter == True and inletter == False:
                foundletter = False
                end_x = x
                start_y = min(y_mx_mn)
                end_y = max(y_mx_mn)+1#line[i + 1]
                y_mx_mn = []
                start_space = end
                letters.append((start_x, end_x, start_y, end_y))
            inletter = False

    # New code is here. We just extract each image and save it to disk with
    # what is hopefully a unique name

    print(letters)

    im_files = []
    count = 0
    for letter in letters:
        m = hashlib.md5()
        im3 = im2.crop((letter[0], letter[2], letter[1], letter[3]))
        try:
            m.update(("%s%s" % (time.time(), count)).encode())
            hex_dig = m.hexdigest()
            im3.save("./sets/%s.png" % hex_dig)
            im3.save("%s/%s.png" % (path, hex_dig))
            if not flag:
                im_files.append("./sets/%s.png" % hex_dig)
            count += 1
        except Exception as e:
            pass



    # sys.exit()



    v = VectorCompare()

    iconset = ['а', 'ж', "в", "е", "и", "і", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ь",
               #",", ".", "'", "0", "9", "8", "7", "6", "5", "4", "3", "2", "1",
               "я", "ю", "щ", "ш",
               "ц", "х", "ф", "ї", "й", "з", "є", "д", "г", "б",]# "Л", "Д", "Ж", "Ю", "Б", "Ь", "Т",
               # "И", "М", "С", "Ч", "Я", "Ф", "І", "В", "А", "П", "Р", "О", "Є", "Ї", "Х", "З", "Щ",
               # "Ш", "Г", "Н", "Е", "К", "У", "Ц", "Й"]

    imageset = []

    for letter in iconset:
        for img in os.listdir('iconset/%s/' % (letter)):
            temp = []
            if img != "Thumbs.db":
                temp.append(buildvector(Image.open("./iconset/%s/%s" % (letter,img))))
        # else:
        #     temp.append(buildvector(Image.open("./alphas/1%s.png" % letter)))
            imageset.append({letter: temp})

    count = 0
    alpha = []
    for letter in letters:
        m = hashlib.md5()
        im3 = im2.crop((letter[0], letter[2], letter[1], letter[3]))

        guess = []
        for image in imageset:

            for x, y in dict(image).items():
                # image = list(image.values())[0]
                # image = image[0]
                # print(y)
                guess.append((v.relation(y[0], buildvector(im3)), x))

        guess.sort(reverse=True)
        # print(guess)
        alpha.append(guess[0][1])
        count += 1

    text = []
    for i in range(len(alpha)):
        text.append(alpha[i])
        if i == spaces[i]:
            text.append(' ')
    str_text = ''.join(text)
    print(str_text)


    for files in im_files:
        os.remove(files)

    return str_text

# print(recognize('text2.png', True, './sets'))