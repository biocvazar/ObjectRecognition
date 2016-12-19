import os

__author__ = 'Bio'

import math


class VectorCompare:
    def magnitude(self, concordance):
        total = 0
        # print("magn   ", concordance)
        lst = list(concordance.values())[0]
        try:
            lst = list(lst[0].values())
            # print("lst", lst)
            for i in lst:
                # print(i)
                total += int(i) ** 2
            return math.sqrt(total)
        except:
            return 1


    def relation(self, concordance1, concordance2):
        relevance = 0
        topvalue = 0
        # print(concordance2)
        for word, cnt in concordance1.items():
            # print(cnt, concordance2)
            for i1, i2 in zip(cnt[0].values(), concordance2.values()):
                topvalue += i1 * i2
                # print(cnt, concordance2)
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


from PIL import Image
import hashlib
import time

im = Image.open("text2.png").convert('LA')
im2 = Image.new("P", im.size, 255)

temp = {}
pixels = im.load()

for x in range(im.size[1]):
    for y in range(im.size[0]):
        # print(sum(pixels[y, x]) / 3)
        if sum(pixels[y, x]) / 3 > 127:
            pixels[y, x] = (255, 255)
        else:
            pixels[y, x] = (0, 0)

im = im.convert('P')

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        temp[pix] = pix
        if pix <= 200:  # these are the numbers to get
            im2.putpixel((y, x), 0)

im2.save("text.gif")


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

# print(lines)
line = [0]
for i in range(len(lines) - 1):
    if lines[i + 1] - lines[i] > 1:
        line.append(lines[i + 1])

# del line[0]
print(line)


inletter = False
foundletter = False
start = end = 0
end_space = start_space = 0
letters = []
spaces = []

for i in range(len(line) - 1):
    start_x = 0
    start_y = 0
    for x in range(im2.size[0]):  # slice across
        for y in range(im2.size[1]):  # slice down
            pix = im2.getpixel((x, y))
            if pix <= 220:
                inletter = True
                break

        if foundletter == False and inletter == True:
            foundletter = True
            start_x = x
            start_y = line[i]
            end_space = y - 1
            if end_space > start_space:
                spaces.append(len(letters))
        if foundletter == True and inletter == False:
            foundletter = False
            end_x = x
            end_y = line[i + 1]
            start_space = end
            letters.append((start_x, end_x, start_y, end_y))
        inletter = False

# New code is here. We just extract each image and save it to disk with
# what is hopefully a unique name

im_files = []
count = 0
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0], letter[2], letter[1], letter[3]))
    m.update(("%s%s" % (time.time(), count)).encode())
    hex_dig = m.hexdigest()
    im3.save("./%s.png" % hex_dig)
    im_files.append("./%s.png" % hex_dig)
    count += 1


def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


v = VectorCompare()

iconset = ['а', 'ж', "в", "е", "и", "і", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ь",
           ",", ".", "'", "0", "9", "8", "7", "6", "5", "4", "3", "2", "1", "я", "ю", "щ", "ш",
           "ц", "х", "ф", "ї", "й", "з", "є", "д", "г", "б", "Л", "Д", "Ж", "Ю", "Б", "Ь", "Т",
           "И", "М", "С", "Ч", "Я", "Ф", "І", "В", "А", "П", "Р", "О", "Є", "Ї", "Х", "З", "Щ",
           "Ш", "Г", "Н", "Е", "К", "У", "Ц", "Й"]

imageset = []

for letter in iconset:
    temp = []
    if not letter.istitle():
        temp.append(buildvector(Image.open("./alphas/%s.png" % letter)))
        imageset.append({letter: temp})
    else:
        temp.append(buildvector(Image.open("./alphas/1%s.png" % letter)))
        imageset.append({letter: temp})

count = 0
alpha = []
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0], letter[2], letter[1], letter[3]))

    guess = []

    for image in imageset:
        # print(image)

        for x, y in dict(image).items():
            # print(x, y)
            guess.append((v.relation(image, buildvector(im3)), x))

    guess.sort(reverse=True)
    print("", guess[0][1])
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