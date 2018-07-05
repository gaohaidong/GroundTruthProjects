import numpy as np
def read_csv(anno_file):
    annos = dict()
    num = 0
    with open(anno_file) as f:
        for line in f.readlines():
            items = line.split(',')
            if items[0][-3:] == 'jpg':
                bboxes = []
                for bbox_item in items[1].strip().split(';'):
                    bbox = []
                    if bbox_item == '':
                        continue
                    info = bbox_item.split('_')
                    if len(info) == 5:
                        if float(info[-1]) < 0.999:
                            continue
                    for i in range(4):
                        bbox.append(float(info[i]))
                    bboxes.append(bbox)
                    num += 1
                annos[items[0]] = bboxes
    return annos, num


def cal_iou(bbox1, bbox2): # x,y,w,h
    if ((abs(bbox1[0] - bbox2[0]) < ((bbox1[2] + bbox2[2]) / 2.0)) and (
            abs(bbox1[1] - bbox2[1]) < ((bbox1[3] + bbox2[3]) / 2.0))):
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

def eval_det(gt_info, det_info, iou_thresh = 0.7, if_write_res = False):
    wrong_dets = dict()
    missing_dets = dict()
    right_num = 0
    for img in det_info.keys():
        assert img in gt_info.keys(), '{} is not annotated'.format(img)
        for det_bbox in det_info[img]:
            flag_wrong = True
            for gt_bbox in gt_info[img]:
                if cal_iou(gt_bbox, det_bbox) >= iou_thresh:
                    flag_wrong = False
                    right_num += 1
                    break
            if flag_wrong:
                if img not in wrong_dets.keys():
                    wrong_dets[img] = [det_bbox]
                else:
                    wrong_dets[img].append(det_bbox)
    if if_write_res:
        for gt_bbox in gt_info[img]:
            flag_missing = True
            for det_bbox in det_info[img]:
                if cal_iou(gt_bbox, det_bbox) >= iou_thresh:
                    flag_missing = False
                    break
            if flag_missing:
                if img not in missing_dets.keys():
                    missing_dets[img] = [gt_bbox]
                else:
                    missing_dets[img].append(gt_bbox)
        with open('wrong_dets.csv', 'w') as f:
            for img in wrong_dets.keys():
                f.write('\n{},'.format(img))
                for bbox in wrong_dets[img]:
                    f.write('{}_{}_{}_{};'.format(bbox[0], bbox[1], bbox[2], bbox[3]))
        with open('missing_dets.csv', 'w') as f:
            for img in missing_dets.keys():
                f.write('\n{},'.format(img))
                for bbox in missing_dets[img]:
                    f.write('{}_{}_{}_{};'.format(bbox[0], bbox[1], bbox[2], bbox[3]))
    return right_num

anno_file = 'train_b.csv'
annos_info, gt_num = read_csv(anno_file)
res_file = 'gtai_res_X101_64x4d_roi14_aug.csv'
res_info, det_num = read_csv(res_file)
sum = 0.0
print 'gt_num\t', gt_num, 'det_num', det_num
for iou_thresh in np.arange(0.5, 0.95, 0.05):
    a = eval_det(annos_info, res_info, iou_thresh)
    s = 2.0 * a / (gt_num + det_num)
    print iou_thresh, a, s
    sum += s
print 'average res\t', sum / 9
