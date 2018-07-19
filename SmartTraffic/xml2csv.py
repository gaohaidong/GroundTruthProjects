import xml.etree.ElementTree as ET
import os
from read_csv import read_csv
ANNO_DIR = 'test_anno_xml/'
def xml2anno(file):
    tree = ET.parse(os.path.join(ANNO_DIR, file.replace('jpg', 'xml')))
    objs = tree.findall('object')
    boxes = []
    for ix, obj in enumerate(objs):
        bbox = obj.find('bndbox')
        # print unicode(cls_name, encoding="utf-8")
        x1 = int(bbox.find('xmin').text)
        y1 = int(bbox.find('ymin').text)
        x2 = int(bbox.find('xmax').text)
        y2 = int(bbox.find('ymax').text)
        boxes.append([x1, y1, x2 -x1, y2 - y1])
    return boxes

def annos2csv(annos, csv_file):
    with open(csv_file, 'w') as f:
        f.write('name,coordinate')
        for im in annos.keys():
            f.write('\n{},'.format(im))
            for box in annos[im]:
                f.write('{}_{}_{}_{};'.format(box[0], box[1], box[2], box[3]))


if __name__ == '__main__':
    annos, num = read_csv('gtai_res_101_fc_0705.csv')
    for file in os.listdir(ANNO_DIR):
        file = file.replace('xml', 'jpg')
        if file in annos.keys():
            annos[file] = xml2anno(file)
        else:
            print('{} not in csv\n'.format(file))
    annos2csv(annos, 'test_anno.csv')
