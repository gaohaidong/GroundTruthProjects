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
    round2_csv = os.path.join(os.path.dirname(args.res_csv), 'ori.csv')
    defect_codes = {'zhadong':1, 'bianzhadong':1, 'maoban':2, 'cadong':3, 'maodong':4, 'zhixi':5, 'diaojing':6,'quejing':7, 'bianquejing':7, 'tiaohua':8, 'jingtiaohua':8, 'youzi':9, 'wuzi':9, 'huangzi':9, 'youwu':9}
    defect_codes_imgs = [dict() for i in range(11)]
    labels = ['norm'] + ['defect_{}'.format(i) for i in range(1,11)]
    imgs = []
    with open(res_csv) as f:
        for line in f.readlines():
            items = line.strip().split(',')
            if items[0][-4:] == '.jpg':
                imgs.append(items[0])
                boxes = items[1].split(';')
                max_thresh = [0.0 for i in range(11)]
                for box in boxes:
                    if box == '':
                        continue
                    thresh = float(box.split('_')[-1])
                    if thresh > conf_thresh:
                        defect_code = box.split('_')[-2]
                        if defect_code in defect_codes.keys():
                            if thresh > max_thresh[defect_codes[defect_code]]:
                                max_thresh[defect_codes[defect_code]] = thresh
                        else:
                            if thresh > max_thresh[10]:
                                max_thresh[10] = thresh
                max_thresh[0] = 1.0
                for i in range(1,11):
                    max_thresh[0] *= 1 - max_thresh[i]
                for i in range(11):
                    defect_codes_imgs[i][items[0]] = max_thresh[i]

    with open(round2_csv, 'w') as f:
        f.write('filename|defect,probability\n')
        for i in range(11):
            for img in defect_codes_imgs[i].keys():
                f.write('{}|{}, {}\n'.format(img, labels[i], round(defect_codes_imgs[i][img], 6)))