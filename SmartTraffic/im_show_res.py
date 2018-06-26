import cv2, os

def show_im_bbox(info, affix):
    items = info.split(',')
    if items[0] not in os.listdir('/data/01competitions/10traffic/jiaotong/test_a/'):
        return
    if items[1].strip() == '':
        return
    im = cv2.imread('/data/01competitions/10traffic/jiaotong/test_a/' + items[0])
    for box in items[1].split(';'):
        if box == '':
            continue
        x,y,w,h = map(int, box.split('_'))
        cv2.rectangle(im, (x,y), (x + w, y + h), (255,0,0))
    cv2.imwrite(affix + items[0], im)
if __name__ == '__main__':
    name = 'gtai_res.csv'
    with open(name) as f:
        infos = f.readlines()
        for index in range(len(infos)):
            affix = str(index) + '_'
            show_im_bbox(infos[index].strip(), affix)
