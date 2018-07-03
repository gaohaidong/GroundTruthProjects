import cv2
import json
def read_csv(anno_file):
    annos = dict()
    with open(anno_file) as f:
        for line in f.readlines():
            items = line.split(',')
            if items[0][-3:] == 'jpg':
                annos[items[0]] = items[1].strip()
    return annos

def gen_json(csv_infos, json_file, img_dir = 'train_b/'):
    images = []
    annotations = []
    im_id  = 0
    bbox_id = 0
    for csv_info in csv_infos.keys():
        img_info = dict()
        img_info["file_name"] = csv_info
        im = cv2.imread(img_dir + csv_info)
        img_info["width"] = im.shape[1]
        img_info["height"] = im.shape[0]
        img_info["id"] = im_id
        images.append(img_info)
        for bbox in csv_infos[csv_info].split(';'):
            if bbox == '':
                continue
            anno_info = dict()
            anno_info["bbox"] = map(float, bbox.split('_'))
            anno_info["image_id"] = im_id
            anno_info["id"] = bbox_id
            anno_info["category_id"] = 1
            annotations.append(anno_info)
            bbox_id += 1
        im_id += 1
    anno = dict()

    info = dict()
    info["description"] = "annos for {}".format(json_file[:-5])
    anno["info"] = info
    anno["images"] = images
    anno["annotations"] = annotations
    anno["categories"] = [{"name":"car", "id": 1}]

    json.dump(anno, open(json_file, 'w'))


anno_file = 'train_b.csv'
annos_info = read_csv(anno_file)
gen_json(annos_info, 'train_b.json')
