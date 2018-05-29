def read_csvfile(filename, interested_id):
    import csv

    csvFile = open(filename, "r")
    reader = csv.reader(csvFile)

    result = {}
    for item in reader:
        if reader.line_num == 1:
            continue
        if item[interested_id] != "":
            result[item[0]] = item[interested_id]
    csvFile.close()
    return result

def dict_img_dir(root):
    import os
    img_dir_dict = {}
    for par, dirs, files in os.walk(root):
        for file in files:
            item = file[:-4].split('.')
            img_dir_dict[item[0] + '-' + item[1]] = os.path.join(par,file)
    return img_dir_dict
    
def move_img(attr_dict, img_dir_dict, root_dir):
    import shutil,os
    attrs = set()
    multi_attr_dict = {}
    for key in attr_dict.keys():
        if 1:#len(attr_dict[key].split(';')) == 1:
            if attr_dict[key] not in attrs:
                attrs.add(attr_dict[key])
                new_path = os.path.join(root_dir, attr_dict[key])
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
            new_path = os.path.join(root_dir, attr_dict[key])
            shutil.copy(img_dir_dict[key], os.path.join(new_path, key + '.jpg'))
        else:
            multi_attr_dict[key] = attr_dict[key]
    with open("shoes_material.txt", "w") as f:
        for attr in attrs:
            f.write(attr + "\t" + str(len(os.listdir(os.path.join(root_dir, attr)))) + "\n")
            
def move_selected_materials(attr, old_dir, new_dir):
    import os,shutil
    new_path = os.path.join(new_dir, attr)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    for dir in os.listdir(old_dir):
        if attr in dir:
            for file in os.listdir(os.path.join(old_dir, dir)):
                shutil.copy(os.path.join(os.path.join(old_dir, dir), file), os.path.join(new_path, file))

if __name__ == '__main__':
    img_dir_dict = dict_img_dir("ut-zap50k-images-square")
    attr_dict = read_csvfile("ut-zap50k-data/meta-data.csv", 7)
    move_img(attr_dict, img_dir_dict, "shoes_material")
    move_selected_materials("Rubber", "shoes_material", "shoes_selected_material")
