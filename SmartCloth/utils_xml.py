import xml.dom.minidom as xmldom

def get_bbox_xml(xml_pth):
    obj_dict = {}
    domobj = xmldom.parse(xml_pth)
    node_objs = domobj.documentElement.getElementsByTagName("object")
    for i in range(len(node_objs)):
        # print node_objs[i].nodeName
        node_name = node_objs[i].getElementsByTagName("name")
        node_bbox = node_objs[i].getElementsByTagName("bndbox")
        node_xmin = node_bbox[0].getElementsByTagName("xmin")
        node_ymin = node_bbox[0].getElementsByTagName("ymin")
        node_xmax = node_bbox[0].getElementsByTagName("xmax")
        node_ymax = node_bbox[0].getElementsByTagName("ymax")
        name = node_name[0].firstChild.data.encode("utf-8")  # unicode->utf8
        xmin = int(node_xmin[0].firstChild.data)
        ymin = int(node_ymin[0].firstChild.data)
        xmax = int(node_xmax[0].firstChild.data)
        ymax = int(node_ymax[0].firstChild.data)
        if name not in obj_dict:
            obj_dict[name] = [[xmin, ymin, xmax, ymax]]
        else:
            obj_dict[name].append([xmin, ymin, xmax, ymax])
    return obj_dict