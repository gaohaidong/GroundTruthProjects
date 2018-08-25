import numpy as np
import argparse, sys, os

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def softmax_notzero(x):
    """Compute not_zero softmax values for each sets of scores in x."""
    notzero = [item for item in x if item != 0]
    softmax_notzero = softmax(notzero)
    res = []
    j = 0
    for i in range(len(x)):
        if x[i] == 0:
            res.append(0)
        else:
            res.append(softmax_notzero[j])
            j += 1
    return res

def parse_args():
    parser = argparse.ArgumentParser(description='End-to-end inference')
    parser.add_argument(
        '--csv_file',
        dest='res_csv',
        help='csv file to convert',
        default=None,
        type=str
    )
    parser.add_argument(
        '--thresh',
        dest='thresh',
        help='thresh for result',
        default=0.000001,
        type=float
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    res_csv = args.res_csv
    conf_thresh = args.thresh
    round2_csv = os.path.join(os.path.dirname(args.res_csv), 'crop_2.csv')
    defect_codes = {'zhadong':1, 'bianzhadong':1, 'maoban':2, 'cadong':3, 'maodong':4, 'zhixi':5, 'diaojing':6,'quejing':7, 'bianquejing':7, 'tiaohua':8, 'jingtiaohua':8, 'youzi':9, 'wuzi':9, 'huangzi':9, 'youwu':9}
    defect_codes_imgs = [dict() for i in range(11)]
    labels = ['norm'] + ['defect_{}'.format(i) for i in range(1,11)]
    imgs = []
    max_thresh = []
    with open(res_csv) as f:
        for line in f.readlines():
            items = line.strip().split(',')
            if items[0][-4:] == '.jpg':
                patch_id = int(items[0][items[0].rfind('_') + 1: items[0].rfind('.')])
                im_name = items[0][:items[0].rfind('_')]
                if im_name not in imgs:
                    imgs.append(im_name)
                    max_thresh.append([0.0 for i in range(11)])
                ind = imgs.index(im_name)
                boxes = items[1].split(';')

                for box in boxes:
                    if box == '':
                        continue
                    bbox = box.split('_')
                    if patch_id % 3 != 0 and int(bbox[1]) + int(bbox[3]) < 160:
                        continue
                    if patch_id >= 3 and int(bbox[0]) + int(bbox[2]) < 213:
                        continue
                    if patch_id % 3 != 2 and int(bbox[1]) > 800:
                        continue
                    if patch_id < 6 and int(bbox[0]) > 1067:
                        continue
                    thresh = float(box.split('_')[-1])
                    if thresh > conf_thresh:
                        defect_code = box.split('_')[-2]
                        if defect_code in defect_codes.keys():
                            if thresh > max_thresh[ind][defect_codes[defect_code]]:
                                max_thresh[ind][defect_codes[defect_code]] = thresh
                        else:
                            if thresh > max_thresh[ind][10]:
                                max_thresh[ind][10] = thresh
    for ind in range(len(imgs)):
        max_thresh[ind][0] = 1.0
        for i in range(1,11):
            max_thresh[ind][0] *= 1 - max_thresh[ind][i]
        for i in range(11):
            defect_codes_imgs[i][imgs[ind]] = max_thresh[ind][i]

    with open(round2_csv, 'w') as f:
        f.write('filename|defect,probability\n')
        for i in range(11):
            for img in defect_codes_imgs[i].keys():
                f.write('{}.jpg|{}, {}\n'.format(img, labels[i], round(defect_codes_imgs[i][img], 6)))