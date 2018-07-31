import cv2, os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from read_csv import read_csv

def gen_xml(annos, im, filefolder):
    root = ET.Element('annotation')
    folder = ET.SubElement(root, 'folder')
    folder.text = filefolder
    filename = ET.SubElement(root, 'filename')
    filename.text = im
    size = ET.SubElement(root, 'size')
    im_shape = cv2.imread(os.path.join(filefolder, im)).shape
    width = ET.SubElement(size, 'width')
    width.text = str(im_shape[1])
    height = ET.SubElement(size, 'height')
    height.text = str(im_shape[0])
    depth = ET.SubElement(size, 'depth')
    depth.text = str(im_shape[2])
    for bbox in annos[im]:
        obj = ET.SubElement(root, 'object')
        name = ET.SubElement(obj, 'name')
        name.text = 'car'
        bndbox = ET.SubElement(obj, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(int(bbox[0]))
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(int(bbox[1]))
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(int(bbox[0] + bbox[2]))
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(int(bbox[1] + bbox[3]))
    tree = minidom.parseString(ET.tostring(root))
    xml_str = tree.toprettyxml()
    dom_string = '\n'.join([s for s in xml_str.splitlines() if s.strip()])
    with open(os.path.join(filefolder, im.replace('jpg', 'xml')), 'w') as f:
        f.write(dom_string)
        
if __name__ == '__main__':
    annos, num = read_csv('train_1w.csv')
    wrong_im = []
    with open('wrong_dets.csv') as f:
        for line in f.readlines():
            items = line.strip().split(',')
            if items[0].endswith('.jpg'):
                wrong_im.append(items[0])
    for im in wrong_im:
        print(im)
        gen_xml(annos, im, 'train_1w')
    
    
    
    
    
    
    
    
