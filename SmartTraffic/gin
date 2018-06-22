import math, cv2
import numpy as np
import qrcode
import re
from PIL import Image
import zbar

def cal_iou(bbox1, bbox2):
    if((abs(bbox1[0] - bbox2[0]) < ((bbox1[2] + bbox2[2]) / 2.0)) and (abs(bbox1[1] - bbox2[1]) < ((bbox1[3] + bbox2[3]) / 2.0))):  
        lu_x_inter = max((bbox1[0] - (bbox1[2] / 2.0)), (bbox2[0] - (bbox2[2] / 2.0)))  
        lu_y_inter = min((bbox1[1] + (bbox1[3] / 2.0)), (bbox2[1] + (bbox2[3] / 2.0)))  
  
        rd_x_inter = min((bbox1[0] + (bbox1[2] / 2.0)), (bbox2[0] + (bbox2[2] / 2.0)))  
        rd_y_inter = max((bbox1[1] - (bbox1[3] / 2.0)), (bbox2[1] - (bbox2[3] / 2.0)))  
  
        inter_w = abs(rd_x_inter - lu_x_inter)  
        inter_h = abs(lu_y_inter - rd_y_inter)  
  
        inter_square = inter_w * inter_h  
        union_square = (bbox1[2] * bbox1[3]) + (bbox2[2] * bbox2[3]) - inter_square  
  
        calcIOU = inter_square / union_square * 1.0   
    else:  
        calcIOU = 0.0
  
    return calcIOU  
    
def nms_bbox(bboxs, iou_thresh = 0.7):
    labels = [1 for i in range(len(bboxs))]

    for i in range(len(bboxs)):
        if labels[i] == -1:
            continue
        for j in range(i + 1, len(bboxs)):
            if cal_iou(bboxs[i], bboxs[j]) > iou_thresh:
                labels[j] = -1
                break
    if -1 in labels:
        bbox_new = []
        for i in range(len(bboxs)):
            if labels[i] == 1:
                bbox_new.append(bboxs[i])
        bboxs = bbox_new
    return bboxs

def get_bit_num(res):
    imgs = res.split(',')
    print len(imgs) - 1
    max_box_num = 0
    max_x = 0
    max_y = 0
    max_w = 0
    max_h = 0
    for img in imgs:
        bboxs = img.split(';')
        if max_box_num < (len(bboxs) - 1):
            max_box_num = len(bboxs) - 1
        for bbox in bboxs:
            if bbox == '':
                continue
            x,y,w,h = map(int, bbox.split('_'))
            if max_x < x:
                max_x = x
            if max_y < y:
                max_y = y
            if max_w < w:
                max_w = w
            if max_h < h:
                max_h = h
    print max_box_num, max_x, max_y, max_w, max_h
    bbox_bit_num = int(math.log(max_box_num,2)) + 1
    x_bit_num = int(math.log(max_x,2)) + 1
    y_bit_num = int(math.log(max_y,2)) + 1
    w_bit_num = int(math.log(max_w,2)) + 1
    h_bit_num = int(math.log(max_h,2)) + 1
    print 'bit_num:\t', bbox_bit_num, x_bit_num, y_bit_num, w_bit_num, h_bit_num
    return [bbox_bit_num, x_bit_num, y_bit_num, w_bit_num, h_bit_num]

def gen_binary(res,bit_num):
    codes = ''
    imgs = res.split(',')
    idx = 0
    for img in imgs:
        if img == '':
            codes += str(bin(0))[2:].zfill(bit_num[0])
            print idx
            continue
        bboxs = img.split(';')
        codes += str(bin(len(bboxs)))[2:].zfill(bit_num[0])

        for bbox in bboxs:
            if bbox == '':
                continue
            x,y,w,h = map(int, bbox.split('_'))
            codes += str(bin(x))[2:].zfill(bit_num[1])
            codes += str(bin(y))[2:].zfill(bit_num[2])
            codes += str(bin(w))[2:].zfill(bit_num[3])
            codes += str(bin(h))[2:].zfill(bit_num[4])
        idx += 1
    print len(codes)
    with open('bin_codes.txt', 'w') as f:
        f.write(codes)
    return codes

def RLE_codes(codes_all):
    bin_flag = False
    num = 0
    max_num = 0
    RLE_codes = []
    for code in codes_all:
        if int(code) == int(bin_flag):
            num += 1
        else:
            if max_num < num:
                max_num = num
            RLE_codes.append(num)
            num = 1
            bin_flag = not bin_flag
    if max_num < num:
        max_num = num
    RLE_codes.append(num)
    
    bit_num = int(math.log(max_num,2)) + 1
    print bit_num
    codes_str = ''
    for RLE_code in RLE_codes:
        codes_str += str(bin(RLE_code))[2:].zfill(bit_num)
    print max_num
    print len(codes_str)
    with open('bin_RLE_codes.txt', 'w') as f:
        f.write(codes_str)
    
def encode_chr(codes_all):
    chr_codes = ''
    codes = re.findall(r'.{32}',codes_all)
    remain_code = codes_all[-(len(codes_all) - 32*len(codes)):]
    print 'remain_code', remain_code
    for code in codes:
        chr_codes += str(int(code,2)) + ','
    chr_codes += str(int(remain_code,2)) + ','
    with open('int_codes.txt', 'w') as f:
        f.write(chr_codes)
    print len(chr_codes)
    return chr_codes,remain_code

def encode_chr_bitnum(codes_all, encode_bit_num, encode_table):
    chr_codes = ''
    codes = re.findall(r'.{6}',codes_all)
    print len(codes)
    if len(codes_all) == encode_bit_num*len(codes):
        remain_code = ''
    else:
        remain_code = codes_all[-(len(codes_all) - encode_bit_num*len(codes)):]
    # print 'remain_code', remain_code
    for code in codes:
        chr_codes += encode_table[int(code,2)]
    if remain_code != '':
        chr_codes += encode_table[int(remain_code,2)]
    with open('{}_codes.txt'.format(encode_bit_num), 'w') as f:
        f.write(chr_codes)
    print len(chr_codes)
    return chr_codes,remain_code

def gen_qr_imgs(chr_codes,im_folder):

    print len(chr_codes)
    qr_img_n = 0
    qr_char_len = 2953
    idx = 0
    while idx < len(chr_codes):
        if qr_char_len + idx < len(chr_codes):
            qr_codes = chr_codes[idx:qr_char_len + idx]
            idx += qr_char_len
        else:
            qr_codes = chr_codes[idx:]
            idx = len(chr_codes)
        qr_img_n += 1
        qr = qrcode.QRCode(version=20,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,  
                       box_size=4,
                       border=3)
        qr.add_data(qr_codes)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")     
        img.save(im_folder + str(qr_img_n) + ".png")

    
def image_cascade(imlist, shape):
    num_imgs = len(imlist) / shape[0] / shape[1]
    print len(imlist), shape, num_imgs
    im_num = 0
    while im_num < len(imlist):  
        if len(imlist) - im_num < shape[0] * shape[1]:
            print shape[0] * shape[1] - (len(imlist) - im_num)
            imlist[len(imlist) - 1] = cv2.copyMakeBorder(imlist[len(imlist) - 1], 0, imlist[0].shape[0] - imlist[len(imlist) - 1].shape[0], 0, imlist[0].shape[1] - imlist[len(imlist) - 1].shape[1], cv2.BORDER_CONSTANT, value=(255,255,255))
            print imlist[len(imlist) - 1].shape
            for i in range(shape[0] * shape[1] - (len(imlist) - im_num)):
                img = np.zeros((imlist[0].shape[0], imlist[0].shape[1], imlist[0].shape[2]), np.uint8)     
                #fill the image with white  
                img.fill(255)  
                print img.shape
                imlist.append(img)
        im_num += shape[0] * shape[1]
        print len(imlist)
        # print im_num
    for i in range(len(imlist)):
        imlist[i] = cv2.copyMakeBorder(imlist[i], 60, 60, 60, 60, cv2.BORDER_CONSTANT, value=(255,255,255))
    im_num = 0
    while im_num < len(imlist):
        im_stack = np.vstack(np.hstack((imlist[j * shape[0] + i + im_num] for i in range(shape[0]))) for j in range(shape[1]))
        cv2.imwrite('im_' + str(im_num) + '.png', im_stack)
        im_num += shape[0] * shape[1]

        
def scan_qr_code(imgPath):
    scanner = zbar.ImageScanner()

    scanner.parse_config('enable')

    img = Image.open(imgPath).convert('L')
    width, height = img.size

    qrCode = zbar.Image(width, height, 'Y800', img.tobytes())
    scanner.scan(qrCode)

    data = ''
    for s in qrCode:
        data += s.data

    del img
    print len(data)
    return data
    

def get_res_order(examplefile):
    im_names = []
    with open(examplefile) as f:
        for line in f.readlines():
            if line.split(',')[0][-4:] == '.jpg':
                im_names.append(line.split(',')[0])
    return im_names
    
def decode_bin_data(data, bit_num, encode_bit_num, im_names, remain_code, encode_table):
    bin_data = ''
    if encode_bit_num == 32:
        for num in data.split(','):
            if num == '':
                continue
            bin_data += str(bin(int(num)))[2:].zfill(encode_bit_num)
    else:
        for ch in data:
            bin_data += str(bin(encode_table.index(ch)))[2:].zfill(encode_bit_num)
    if remain_code != '':
        bin_data = bin_data[:-encode_bit_num] + remain_code
    with open('decode_bin.txt','w') as f:
        f.write(bin_data)
    res_str = ''
    im_id = 0
    idx = 0
    while idx < len(bin_data):
        idx_new = idx + bit_num[0]
        if idx_new >= len(bin_data):
            print('The index out of range [num]')
            break
        num_box = int(bin_data[idx:idx_new], 2)
        res_str += im_names[im_id] + ','

        idx = idx_new
        if num_box > 0:
            for i in range(num_box):
                # x
                idx_new = idx+bit_num[1]
                if idx_new >= len(bin_data):
                    print('The index out of range [x]')
                    break
                x = int(bin_data[idx:idx_new], 2)
                idx = idx_new
                # y
                idx_new = idx + bit_num[2]
                if idx_new >= len(bin_data):
                    print('The index out of range [y]')
                    break
                y = int(bin_data[idx:idx_new], 2)
                idx = idx_new
                # w
                idx_new = idx + bit_num[3]
                if idx_new >= len(bin_data):
                    print('The index out of range [w]')
                    break
                w = int(bin_data[idx:idx_new], 2)
                idx = idx_new
                # h
                idx_new = idx + bit_num[4]
                if idx_new >= len(bin_data):
                    print('The index out of range [h]')
                    break
                h = int(bin_data[idx:idx_new], 2)
                idx = idx_new
                res_str += '{}_{}_{}_{}'.format(x, y, w, h)
                if i != num_box - 1:
                    res_str += ';'.format(x, y, w, h)
            #print res_str
        else:
            print im_names[im_id]
        res_str += '\n'

        im_id += 1
    # print(res_str)
    with open('decode_res.txt', 'w') as f:
        f.write(res_str)
import os
if __name__ == '__main__':
    # with open('res_nms.csv', 'w') as fw:
    #     with open('res.csv') as f:
    #         for info in f.readlines():
    #             items = info.split(',')
    #             if items[1].strip() == '':
    #                 fw.write('{}\n'.format(info.strip()))
    #                 continue
    #             bboxs = []
    #             for box_info in items[1].split(';'):
    #                 x,y,w,h = map(int, box_info.split('_'))
    #                 bboxs.append([x,y,w,h])
    #             print items[0]
    #             bboxs = nms_bbox(bboxs)
    #             fw.write('{},'.format(items[0]))
    #             for bbox in bboxs:
    #                 fw.write('{}_{}_{}_{}'.format(bbox[0], bbox[1], bbox[2], bbox[3]))
    #                 if bbox != bboxs[-1]:
    #                     fw.write(';')
    #             fw.write('\n')

    # res = open('res_nms_example_order_ignorename.txt').read()
    # bit_num = get_bit_num(res)
    #
    # codes = gen_binary(res,bit_num)
    # # # chr_codes,remain_code = encode_chr(codes)
    encode_table = [chr(i) for i in range(ord('a'),ord('z') + 1)]\
                   + [chr(i) for i in range(ord('A'),ord('Z') + 1)]\
                   + [chr(i) for i in range(ord('0'),ord('9') + 1)] \
                   + [',','.']
    # chr_codes, remain_code = encode_chr_bitnum(codes, 6, encode_table)
    # im_folder = '6_qr_img/'
    # gen_qr_imgs(chr_codes, im_folder)
    # imlist = [cv2.imread('qrimgs/{}.png'.format(i)) for i in range(1, 1077)]
    # image_cascade(imlist, [5,5])
    # data = ''
    # # data = scan_qr_code('a.PNG')
    # for i in range(1, 1125):
    #     print i,
    #     data = scan_qr_code('qrimgs/{}.png'.format(i))
    #     with open('qr_data.txt','a') as f:
    #         f.write(data)
    with open('6_codes.txt') as f:
        data = f.read().strip()
    im_names = get_res_order('example_a.csv')
    remain_code = ''
    bit_num = [6,11,9,10,9]
    encode_bit_num = 6
    decode_bin_data(data, bit_num, encode_bit_num, im_names, remain_code, encode_table)
