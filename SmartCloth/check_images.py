import cv2, os, pdb
import glob
from utils_files import get_r1_ans
from utils_xml import get_bbox_xml

def get_img_xml_lst(img_dir, xml_dct):
    name_lst, cls_lst, img_lst, xml_lst = [], [], [], []
    for name in os.listdir(img_dir):
        if name[-3:] != 'jpg':
            continue
        #print name
        img_pth = os.path.join(img_dir, name)
        name_lst.append(name)
        img_lst.append(img_pth)
        cls_lst.append(xml_dct[name][0][0] if name in xml_dct else 'norm')
        xml_lst.append(xml_dct[name][0][1] if name in xml_dct else '')
    return zip(name_lst, cls_lst, img_lst, xml_lst)


if __name__ == '__main__':
    r1tea_imgdir = '/media/gait/DATA/04data/01competitions/11tianchi_bupi/round1/r1tea_img/'
    r1teb_imgdir = '/media/gait/DATA/04data/01competitions/11tianchi_bupi/round1/r1teb_img/'
    r1tea_xmldir = '/media/gait/DATA/04data/01competitions/11tianchi_bupi/round1/r1tea_xml/'
    r1teb_xmldir = '/media/gait/DATA/04data/01competitions/11tianchi_bupi/round1/r1teb_xml/'
    #r1tea_lst = glob.glob(r1tea_dir + '*.jpg')
    #r1teb_lst = glob.glob(r1teb_dir + '*.jpg')
    r1tea_xmldct = get_r1_ans(r1tea_xmldir)
    r1teb_xmldct = get_r1_ans(r1teb_xmldir)
    r1tea_zip = get_img_xml_lst(r1tea_imgdir, r1tea_xmldct)
    r1teb_zip = get_img_xml_lst(r1teb_imgdir, r1teb_xmldct)

    # resize the images to 800x600
    len_xmldir = len(r1tea_xmldir)
    len_imgdir = len_xmldir
    r1te_imgdir = '/media/gait/DATA/04data/01competitions/11tianchi_bupi/round2/r1te_imgxml_800x600/'
    r1te_prtdir = '/media/gait/DATA/04data/01competitions/11tianchi_bupi/round2/r1te_imgxml_patches/'
    dst_w, dst_h = 800, 600
    src_w, src_h = 2560, 1920
    for i in range(2):
        for name, cls, img_pth, xml_pth in (r1tea_zip if i == 0 else r1teb_zip):
            if xml_pth == '':
                continue
            img_src = cv2.imread(img_pth)
            img_dst = cv2.resize(img_src, (dst_w, dst_h), interpolation=cv2.INTER_LINEAR)
            dir_dst = r1te_imgdir + cls + '/'
            if not os.path.exists(dir_dst):
                os.mkdir(dir_dst)
            pth_dst = dir_dst + img_pth[len_imgdir:-3] + 'png'
            obj_dct = get_bbox_xml(xml_pth)
            for def_name in obj_dct.keys():
                for bbox in obj_dct[def_name]:
                    xmin = bbox[0] * dst_w / src_w
                    xmax = bbox[2] * dst_w / src_w
                    ymin = bbox[1] * dst_h / src_h
                    ymax = bbox[3] * dst_h / src_h
                    cv2.rectangle(img_dst, (xmin, ymin), (xmax, ymax), (0, 0, 255))
            cv2.imwrite(pth_dst, img_dst)

            for def_name in obj_dct.keys():
                dir_dst = r1te_prtdir + def_name + '/'
                if not os.path.exists(dir_dst):
                    os.mkdir(dir_dst)
                for j in range(len(obj_dct[def_name])):
                    bbox = obj_dct[def_name][j]
                    pth_dst = dir_dst + '{0}_{1}_{2}.png'.format(img_pth[len_imgdir:-4], def_name, j)
                    cv2.imwrite(pth_dst, img_src[bbox[1]:bbox[3], bbox[0]:bbox[2], :])
            #pdb.set_trace()