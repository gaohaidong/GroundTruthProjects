# -*- coding: UTF-8 -*-
import os
import pdb
import numpy as np
# from PIL import Image
# from skimage import io, color, filters
from cv2 import *
from matplotlib import pyplot as plt
import xml.dom.minidom as xmldom
from metrics import calc_rate, calc_auc
from utils_xml import get_bbox_xml

def get_r1_csv(res_pth):
    res_dct = {}
    with open(res_pth, 'r') as f:
        lines = f.readlines()
        for i in range(1, len(lines)):
            items = lines[i].strip().split('\t')
            res_dct[items[0]] = float(items[1])
    return res_dct


def get_r1_ans(xml_dir):
    xml_dct = {}
    for item in os.listdir(xml_dir):
        sub_dir = os.path.join(xml_dir, item)
        if os.path.isdir(sub_dir):
            for temp in os.listdir(sub_dir):
                xml_pth = os.path.join(sub_dir, temp)
                if temp[-3:] == 'xml':
                    jpg_pth = temp[0:-3] + 'jpg'
                    if jpg_pth not in xml_dct:
                        xml_dct[jpg_pth] = 1
    return xml_dct


def get_r2_csv(res_pth):
    res_dct = {}
    with open(res_pth, 'r') as f:
        lines = f.readlines()
        for i in range(1, len(lines)):
            items = lines[i].strip().split(',')
            parts = items[0].split('|')
            if parts[1] not in res_dct:
                res_dct[parts[1]] = {}
            # [defect_class][image_name] = probability
            res_dct[parts[1]][parts[0]] = float(items[1].strip())
    return res_dct


def get_r2_ans(xml_dir, cls_dct):
    xml_dct = {}
    for item in os.listdir(xml_dir):
        sub_dir = os.path.join(xml_dir, item)
        if os.path.isdir(sub_dir):
            def_cls = cls_dct[item]
            if def_cls not in xml_dct:
                xml_dct[def_cls] = {}
            for temp in os.listdir(sub_dir):
                xml_pth = os.path.join(sub_dir, temp)
                if temp[-3:] == 'xml':
                    jpg_pth = temp[0:-3] + 'jpg'
                    if jpg_pth not in xml_dct:
                        xml_dct[def_cls][jpg_pth] = 1
    return xml_dct


if __name__ == '__main__':
    ############################round 1############################
    # step 1: get the algorithm result
    res_pth = '/data/ghd/08GUN_Data/cloth-x101-crop-tc-tx.csv'
    res_dct = get_r1_csv(res_pth)

    # step 2: get the provided result
    # xml_pth = '/data/ghd/08GUN_Data/r1ansb/薄段/J01_2018.06.20 08_44_57.xml'
    # xml_res = get_bbox_xml(xml_pth)
    # for key in xml_res.keys():
    #	print(key.decode('utf-8'))
    xml_dir = '/data/ghd/08GUN_Data/r1ansb/'
    xml_dct = get_r1_ans(xml_dir)

    # step 3: get the probs and labels
    probs, labels = [], []
    for key in res_dct.keys():
        probs.append(res_dct[key])
        labels.append(1 if key in xml_dct else -1)
    tpr, fpr, pre = calc_rate(probs, labels)
    auc = calc_auc(fpr, tpr)
    ap = calc_auc(tpr, pre)

    ############################round 2############################
    # step 1: get the algorithm result
    res_pth = '/data/ghd/08GUN_Data/r1teb_r2_det_prob.csv'
    res_dct = get_r2_csv(res_pth)

    # step 2: get the provided result
    '''
    cls_dct['norm'] = set(['正常'])
    cls_dct['defect_1'] = set(['扎洞'])
    cls_dct['defect_2'] = set(['毛斑'])
    cls_dct['defect_3'] = set(['擦洞'])
    cls_dct['defect_4'] = set(['毛洞'])
    cls_dct['defect_5'] = set(['织稀'])
    cls_dct['defect_6'] = set(['吊经'])
    cls_dct['defect_7'] = set(['缺经'])
    cls_dct['defect_8'] = set(['跳花'])
    cls_dct['defect_9'] = set(['黄渍', '污渍', '油渍'])
    others = ['剪洞', '吊弓', '薄段', '扎梳', '缺纬', '错纱', '弓纱']
    others += ['回边', '破洞', '楞断', '织入', '粗纱', '错经', '夹纱']
    others += ['擦伤', '线印', '厚段', '破边', '边扎洞', '换纱印', '纬粗纱']
    cls_dct['defect_10'] = set(others)
    '''
    cn_dct = {}
    cn_dct['正常'] = 'norm'
    cn_dct['夹码'] = 'defect_10'
    cn_dct['织入'] = 'defect_10'
    cn_dct['双纱'] = 'defect_10'
    cn_dct['薄段'] = 'defect_10'
    cn_dct['夹纱'] = 'defect_10'
    cn_dct['擦伤'] = 'defect_10'
    cn_dct['蛛网'] = 'defect_10'
    cn_dct['嵌结'] = 'defect_10'
    cn_dct['织稀'] = 'defect_5'
    cn_dct['擦毛'] = 'defect_10'
    cn_dct['剪洞'] = 'defect_10'
    cn_dct['跳花'] = 'defect_8'
    cn_dct['油污'] = 'defect_9'
    cn_dct['线印'] = 'defect_10'
    cn_dct['扎纱'] = 'defect_10'
    cn_dct['扎梳'] = 'defect_10'
    cn_dct['粗结'] = 'defect_10'
    cn_dct['修印'] = 'defect_10'
    cn_dct['吊纬'] = 'defect_10'
    cn_dct['错纱'] = 'defect_10'
    cn_dct['错经'] = 'defect_10'
    cn_dct['回边'] = 'defect_10'
    cn_dct['吊弓'] = 'defect_10'
    cn_dct['缺纬'] = 'defect_10'
    cn_dct['毛洞'] = 'defect_4'
    cn_dct['破边'] = 'defect_10'
    cn_dct['油渍'] = 'defect_9'
    cn_dct['耳朵'] = 'defect_10'
    cn_dct['黄渍'] = 'defect_9'
    cn_dct['边洞'] = 'defect_10'
    cn_dct['结洞'] = 'defect_10'
    cn_dct['弓纱'] = 'defect_10'
    cn_dct['毛粒'] = 'defect_10'
    cn_dct['紧纱'] = 'defect_10'
    cn_dct['毛斑'] = 'defect_2'
    cn_dct['厚段'] = 'defect_10'
    cn_dct['污渍'] = 'defect_9'
    cn_dct['缺经'] = 'defect_7'
    cn_dct['楞断'] = 'defect_10'
    cn_dct['擦洞'] = 'defect_3'
    cn_dct['扎洞'] = 'defect_1'
    cn_dct['破洞'] = 'defect_10'
    cn_dct['粗纱'] = 'defect_10'
    cn_dct['吊经'] = 'defect_6'
    cn_dct['边白印'] = 'defect_10'
    cn_dct['厚薄段'] = 'defect_10'
    cn_dct['蒸呢印'] = 'defect_10'
    cn_dct['明嵌线'] = 'defect_10'
    cn_dct['纬粗纱'] = 'defect_10'
    cn_dct['换纱印'] = 'defect_10'
    cn_dct['经粗纱'] = 'defect_10'
    cn_dct['边缺经'] = 'defect_10'
    cn_dct['烧毛痕'] = 'defect_10'
    cn_dct['边针眼'] = 'defect_10'
    cn_dct['纬粗节'] = 'defect_10'
    cn_dct['边扎洞'] = 'defect_10'
    cn_dct['经跳花'] = 'defect_10'
    cn_dct['边缺纬'] = 'defect_10'
    cn_dct['圆珠笔印'] = 'defect_10'
    xml_dct = get_r2_ans(xml_dir, cn_dct)
    ook_lst = []
    for i in range(1, 11):
        ook_lst += xml_dct['defect_{0}'.format(i)].keys()
    ook_set = set(ook_lst)
    for jpg in res_dct['norm'].keys():
        if jpg not in set(ook_set):
            xml_dct['norm'][jpg] = 1

    # step 3: get the probs and labels
    score = 0.0
    for def_cls in res_dct.keys():
        probs, labels = [], []
        tmp_res_dct = res_dct[def_cls]
        tmp_xml_dct = xml_dct[def_cls]
        for key in tmp_res_dct.keys():
            probs.append(tmp_res_dct[key])
            labels.append(1 if key in tmp_xml_dct else -1)
        tpr, fpr, pre = calc_rate(probs, labels)
        if def_cls == 'norm':
            val = calc_auc(fpr, tpr)
            print('auc_{0}={1}'.format(def_cls, val))
            score += 0.7 * val
            plt.subplot(3, 4, 1)
            plt.plot(fpr, tpr)
        else:
            val = calc_auc(tpr, pre)
            print('ap_{0}={1}'.format(def_cls, val))
            score += 0.3 * 0.1 * val
            plt.subplot(3, 4, int(def_cls[7:]) + 1)
            plt.plot(tpr, pre)
        plt.title(def_cls)
    plt.show()
    print(score)
    pdb.set_trace()
    dir_src = '/data/ghd/08GUN_Data/xuelang_round2_test_a_20180809_bg/'
    pth_lst = os.listdir(dir_src)
    for item in pth_lst:
        # if item != 'J01_2018.07.20 08_17_44.jpg':
        #	continue
        # if item != 'J01_2018.07.20 08_48_46.jpg':
        #	continue
        img_pth = os.path.join(dir_src, item.strip())
        '''
        img_rgb = io.imread(img_pth)
        img_src = img_rgb
        img_hsv = color.rgb2hsv(img_rgb)
        img_h, img_s, img_v = img_hsv[:,:,0], img_hsv[:,:,1], img_hsv[:,:,2]
        val_thr = filters.threshold_otsu(img_hsv[:,:,2])
        img_bin = (img_hsv[:,:,2] <= val_thr) * 1.0
        '''
        img_bgr = imread(img_pth)
        img_src = img_bgr
        img_hsv = cvtColor(img_bgr, COLOR_BGR2HSV)
        img_h, img_s, img_v = split(img_hsv)
        blr_val = 11  # 7
        blr_str = '_blur=' + str(blr_val)
        img4seg = 255 - GaussianBlur(img_v, (blr_val, blr_val), 0)
        #### 1. draw image for segmentation
        imwrite(item + '_SAVE1' + '_in' + blr_str + '.jpg', img4seg)

        #### 2. draw segmentation result
        for j in range(3):
            # if j != 1:
            #	continue
            if j == 0:
                tmp_val, img_dst = threshold(img4seg, 0, 255, THRESH_BINARY + THRESH_OTSU)
                name = '_SAVE2' + blr_str + '_segOTSU.jpg'
            elif j == 1:
                set_val = 100  # 80
                ret_val, img_dst = threshold(img4seg, set_val, 255, THRESH_BINARY)
                name = '_SAVE2' + blr_str + '_seg' + str(set_val) + '.jpg'
            else:
                set_val = 50
                tmp_val, img_dst = threshold(img4seg, set_val, 255, THRESH_OTSU)
                name = '_SAVE2' + blr_str + '_segOTSU' + str(set_val) + '.jpg'
            kernel = getStructuringElement(MORPH_RECT, (5, 5))
            img_bin = morphologyEx(img_dst, MORPH_CLOSE, kernel)
            imwrite(item + name, img_bin)

            #### 3. draw various result
            if j == 0:
                plt.subplot(231)
                plt.imshow(img_src)
                plt.title('img_src')
                plt.subplot(232)
                plt.imshow(img4seg, cmap='gray')
                plt.title('img4seg')
                plt.subplot(233)
                plt.imshow(img_bin, cmap='gray')
                plt.title('img_bin')
                plt.subplot(234)
                plt.imshow(img_h, cmap='gray')
                plt.title('img_h')
                plt.subplot(235)
                plt.imshow(img_s, cmap='gray')
                plt.title('img_s')
                plt.subplot(236)
                plt.imshow(img_v, cmap='gray')
                plt.title('img_v')
                plt.savefig(item + '_SAVE3' + '_plot.jpg')
            # plt.show()

            #### 4. draw image hist
            if j == 0:
                plt.subplot(111)
                nbins = [64, 128, 256]
                color = ['r', 'g', 'b']
                for i in range(len(nbins)):
                    plt.cla()
                    nbin = nbins[i]
                    img_hist = calcHist([img4seg], [0], None, [nbin], [0, 256])
                    plt.plot(img_hist, color=color[i])
                    plt.xlim([0, nbin])
                    val = tmp_val / (256 / nbin)
                    num = np.max(img_hist)
                    plt.plot([val for i in range(num)], [i for i in range(num)])
                    plt.savefig(item + '_SAVE4' + '_hist' + str(nbin) + '.jpg')

        # pdb.set_trace()