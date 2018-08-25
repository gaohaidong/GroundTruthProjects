import numpy as np
import argparse, sys, os


defect_codes_imgs = dict()
merged_codes_imgs = dict()
labels = ['norm'] + ['defect_{}'.format(i) for i in range(1,11)]

def parse_args():
    parser = argparse.ArgumentParser(description='End-to-end inference')
    parser.add_argument(
        '--res_dir',
        dest='res_dir',
        help='csv file dir to val',
        default=None,
        type=str
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    res_csvs = [os.path.join(args.res_dir, 'crop_2.csv'), os.path.join(args.res_dir, 'ori.csv')]

    for res_csv in res_csvs:
        with open(res_csv) as f:
            for line in f.readlines():
                infos = line.strip().split(',')
                items = infos[0].split('|')
                if items[0][-4:] == '.jpg':
                    print items[0]
                    if items[0] not in defect_codes_imgs.keys():
                        defect_codes_imgs[items[0]] = [[] for i in range(11)]
                    thresh = float(infos[1])
                    defect_codes_imgs[items[0]][labels.index(items[1])].append(thresh)
    for img in defect_codes_imgs.keys():
        merged_codes_imgs[img] = [[] for i in range(11)]
        for i in range(1,11):
            merged_codes_imgs[img][i] = np.mean(defect_codes_imgs[img][i])
        # merged_codes_imgs[img][0] = 1 - max([merged_codes_imgs[img][i] for i in range(1,11)])
        merged_codes_imgs[img][0] = 1.0
        for i in range(1, 11):
            merged_codes_imgs[img][0] *= 1 - merged_codes_imgs[img][i]
    merged_csv = os.path.join(args.res_dir, 'merged.csv')
    # merged_csv = '{}_{}.csv'.format(res_csvs[0], res_csvs[1])

    with open(merged_csv, 'w') as f:
        f.write('filename|defect,probability\n')

        for img in merged_codes_imgs.keys():
            for i in range(11):
                f.write('{}|{}, {}\n'.format(img, labels[i], round(merged_codes_imgs[img][i], 6)))