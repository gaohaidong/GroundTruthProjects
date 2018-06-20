import math, cv2
import numpy as np
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
    for img in imgs:
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
    import re
    chr_codes = ''
    codes = re.findall(r'.{32}',codes_all) 
    remain_code = codes_all[-(len(codes_all) - 32*len(codes)):]
    print remain_code
    for code in codes:
        chr_codes += str(int(code,2)) + ','
    chr_codes += str(int(remain_code,2)) + ','
    with open('int_codes.txt', 'w') as f:
        f.write(chr_codes)
    print len(chr_codes)
    return chr_codes

def gen_qr_imgs(chr_codes):
    import qrcode  
    print len(chr_codes)
    qr_img_n = 0
    while chr_codes != '':
        if len(chr_codes) > 2953:
            qr_codes = chr_codes[:2953]
            chr_codes = chr_codes[2953:]
        else:
            qr_codes = chr_codes
            chr_codes = ''
        print len(chr_codes)
        qr_img_n += 1
        qr = qrcode.QRCode(version=20,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,  
                       box_size=3,
                       border=3)
        qr.add_data(qr_codes)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")     
        img.save('qrimgs/' + str(qr_img_n) + ".png")

    
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
        print len(imlist)
        # print im_num
        # for i in range(im_num, im_num + shape[0] * shape[1]):
            # imlist[i] = cv2.copyMakeBorder(imlist[i], 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255,255,255))
        im_stack = np.vstack(np.hstack((imlist[j * shape[0] + i + im_num] for i in range(shape[0]))) for j in range(shape[1]))
        cv2.imwrite('im_' + str(im_num) + '.png', im_stack)
        im_num += shape[0] * shape[1]

        
def scan_qr_code(imgPath):
    from PIL import Image
    import zbar
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
    bin_data = ''
    for num in data.split(','):
        bin_data += str(bin(int(num)))[2:].zfill(32)
    return bin_data

def get_res_order(examplefile):
    im_names = []
    with open(examplefile) as f:
        for line in f.readlines():
            if line.split(',')[0][-4:] == '.jpg':
                im_names.append(line.split(',')[0])
    return im_names
    
def decode_bin_data(bin_data, bit_num, im_names):
    str = ''
    id = 0
    while bin_data != '':
        print int(bin_data[:bit_num[0]], 2)
        if int(bin_data[:bit_num[0]], 2) > 0:
            str += im_names[id] + ','
            box_num = int(bin_data[:bit_num[0]], 2)
            bin_data = bin_data[bit_num[0]:]
            for i in range(box_num):
                x = int(bin_data[:bit_num[1]], 2)
                bin_data = bin_data[bit_num[1]:]
                y = int(bin_data[:bit_num[2]], 2)
                bin_data = bin_data[bit_num[2]:]
                w = int(bin_data[:bit_num[3]], 2)
                bin_data = bin_data[bit_num[3]:]
                h = int(bin_data[:bit_num[4]], 2)
                bin_data = bin_data[bit_num[4]:]
                str += '{}_{}_{}_{};'.format(x,y,w,h)
            str = str[:-1] + '\n'
            print str
        else:
            print im_names[id]
        id += 1
    with open('decode_res.txt', 'w') as f:
        f.write(str)

if __name__ == '__main__':
    # res = open('res_example_order.txt').read()
    # bit_num = get_bit_num(res)
    bit_num = [6,11,9,10,9]
    # codes = gen_binary(res,bit_num)
    # chr_codes = encode_chr(codes)
    # gen_qr_imgs(chr_codes)
    # imlist = [cv2.imread('qrimgs/{}.png'.format(i)) for i in range(1, 1125)]
    # image_cascade(imlist, [7,7])
    bin_data = scan_qr_code('a.PNG')
    im_names = get_res_order('example_a.csv')
    decode_bin_data(bin_data, bit_num, im_names)
    
