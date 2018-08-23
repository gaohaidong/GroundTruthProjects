import os

# get the results in round 1 with csv format
def get_r1_csv(res_pth):
    res_dct = {}
    with open(res_pth, 'r') as f:
        lines = f.readlines()
        for i in range(1, len(lines)):
            items = lines[i].strip().split('\t')
            res_dct[items[0]] = float(items[1])
    return res_dct

# get the answers in round 1 with xml format
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
                        xml_dct[jpg_pth] = [[item, xml_pth]]
                    else:
                        xml_dct[jpg_pth].append([item, xml_pth])
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