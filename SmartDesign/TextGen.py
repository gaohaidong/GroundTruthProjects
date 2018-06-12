# -*- coding: utf-8 -*-
import sys
import math
from random import randint
from PIL import Image,ImageDraw,ImageFont

text_nums = '0123456789'

def get_num_strs(x, step):
    digs = []
    while x:
        y = int(x / step)
        digs.append(x - y * step)
        x = y
    return len(digs)
'''
    rets = []
    dLEN = len(digs)
    for i in range(0, dLEN):
'''


# way 1: the number of characters
def get_num1():
    f = open('res.txt', 'r')
    f.readline()#first line
    num_x = 0
    for line in f:
        num_x += len(line.strip().split(',')[1].split(';'))
    num_x = num_x * 4
    print(num_x)
    f.close()

def get_num2():
    f = open('res.txt', 'r')
    f.readline()#first line
    num_x = 0
    num_line = 1
    step = 2
    for line in f:
        result = line.strip().split(',')[1]
        num_line += 1
        if result == '':
            print(str(num_line) + '=>Empty')
            num_x += get_num_strs(0, step)
            continue
        num_xywh = 0
        for xywh in result.split(';'):
            digs = xywh.split('_')
            if len(digs) != 4:
                print(str(line) + ':<' + xywh + ',error>')
                continue
            num_xywh += 1
            for x in digs:
                try:
                    l = get_num_strs(int(x), step)
                    num_x += l
                    num_x += get_num_strs(l, step)
                except ValueError:
                    print('----')
                    print(line)
                    print(num_line)
        num_x += get_num_strs(num_xywh, step)
    print(num_x)
    f.close()

get_num2()
get_num1()

# Read font_names
#f = open('font_names_hz.txt', 'r')
#font_names_zh = [r'C:/Windows/Fonts/' + item.strip() for item in f.readlines()]
#f.close()
f = open('font_names_en.txt', 'r')
font_names_en = [r'C:/Windows/Fonts/' + item.strip() for item in f.readlines()]
f.close()

# Read characters
#f = open('hz_3500.txt', 'r')
#text_zh = f.read()
#f.close()
#f = open('en_52.txt', 'r')
#text_en = f.read()
#f.close()
#print(hans)
#print(len(hans))

# Create Image
img_w = 1920
img_h = 1080

##############################  way 0: input characters  ##############################
step_w = 4
step_h = 4
back_v = 0
img = Image.new("RGB", (img_w, img_h), "#000000").convert('L')
for i in range(0, img_w, step_w):
    for j in range(0, img_w, step_h):
        if randint(0, 1) == 0:
            back_v = 0
        else:
            back_v = 255
        img.paste(back_v, (i, j, i + step_w, j + step_h))
        back_v = 255-back_v
img.save(r'text2images_pixels.png', 'PNG')
exit(0)

##############################  way 1: input characters  ##############################
f = 20 / 30
text_size = int(30 * f)
text_num = int(1100 / (f * f))

step_w = 15.3 * f#15.3
step_h = 25.0 * f#25.0
h_idx = 10

text_font = ImageFont.truetype(font_names_en[0], text_size)
print(font_names_en[0])
while True:
    img = Image.new("RGB", (img_w, img_h), "#000000").convert('L')
    #print(type(img))

    draw = ImageDraw.Draw(img)
    #text_rand = text_nums[randint(0, 9)]
    #print(text_rand)
    #draw.text((100, 100), text_rand, fill=(100), font=text_font)

    str_l = ''
    len_l = 0
    for i in range(0, text_num):
        text_xywh = str(randint(0, 4000))
        text_digs = str(len(text_xywh)) + text_xywh
        if (len_l + len(text_digs)) * step_w >= img_w:
            print(str(len(str_l)) + ':' + str_l)
            draw.text((10, h_idx), str_l, fill=(255), font=text_font)
            str_l = ''
            len_l = 0
            h_idx += step_h
        else:
            str_l += text_digs
            len_l += len(text_digs)

    '''
    for i in range(0, img_w, step_w):
        if i + step_w > img_w:
            text_w = img_w - i;
        else:
            text_w = step_w;
        for j in range(0, img_h, step_h):
            if j + step_h > img_h:
                text_h = img_h - j;
            else:
                text_h = step_h;

            # Chinese or English text?
            rand_type = randint(0, 1)
            if rand_type == 0:
                font_name = font_names_zh[randint(0, len(font_names_zh) - 1)]
                rand_text = text_zh[randint(0, len(text_zh) - 1)]
            else:
                font_name = font_names_en[randint(0, len(font_names_en) - 1)]
                rand_text = text_en[randint(0, len(text_en) - 1)]
            #print(font_name)

            # Font with size
            rand_scale = randint(30, 100)
            rand_font = ImageFont.truetype(font_name, rand_scale)

            # Background, foreground grayscale
            rand_bv = randint(0, 255)
            diff_bv = 30
            if rand_bv < diff_bv:
                flag = 1
            elif rand_bv > 255 - diff_bv:
                flag = -1
            else:
                rand_flag = randint(0, 1)
                if rand_flag == 0:
                    flag = 1
                else:
                    flag = -1
            if flag == 1:
                rand_fv = randint(rand_bv + diff_bv, 255)
            else:
                rand_fv = randint(0, rand_bv - diff_bv)

            img.paste(rand_bv, (i, j, i + text_w, j + text_h))
            draw.text((i, j), rand_text, fill=(rand_fv), font=rand_font)
    '''
    # save image
    #img.save(r'textGen_' + '{:0>4}'.format(str(t)) + '.png', 'PNG')
    print(text_num)
    img.save(r'text2images.png', 'PNG')
    break
print('**********End**********')
