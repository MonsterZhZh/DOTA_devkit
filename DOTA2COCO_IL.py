import dota_utils as util
import os
import cv2
import json

## DOTA
# LabelTxtv1.0
# Old task 8 classes
# wordname_old_8 = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court']
# New task 7 classes
# wordname_new_7 = ['basketball-court', 'storage-tank',  'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool', 'helicopter']

# LabelTxtv1.5
# Old task 8 classes
# wordname_old_8 = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court']
# New task 8 classes
# wordname_new_8 = ['basketball-court', 'storage-tank',  'soccer-ball-field', 'turntable', 'harbor', 'swimming-pool', 'helicopter', 'container-crane']
# All 16 classes
wordname_all_16 = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court',
                   'basketball-court', 'storage-tank',  'soccer-ball-field', 'turntable', 'harbor', 'swimming-pool', 'helicopter', 'container-crane']

## DIOR
# Old task 10 classes
# wordname_old_10 = ['airplane', 'baseballfield', 'bridge', 'groundtrackfield', 'vehicle', 'ship', 'tenniscourt', 'airport', 'chimney', 'dam']
# New task 10 classes
# wordname_new_10 = ['basketballcourt', 'storagetank', 'harbor', 'Expressway-toll-station', 'Expressway-Service-area', 'golffield', 'overpass', 'stadium', 'trainstation', 'windmill']
# All 20 classes
wordname_all_20 = ['airplane', 'baseballfield', 'bridge', 'groundtrackfield', 'vehicle', 'ship', 'tenniscourt', 'airport', 'chimney', 'dam',
                   'basketballcourt', 'storagetank', 'harbor', 'Expressway-toll-station', 'Expressway-Service-area', 'golffield', 'overpass', 'stadium', 'trainstation', 'windmill']

def DOTA2COCO(srcpath, destfile, wordname):
    imageparent = os.path.join(srcpath, 'images')
    labelparent = os.path.join(srcpath, 'labelTxt')

    data_dict = {}
    info = {'contributor': 'captain group',
           'data_created': '2018',
           'description': 'This is 1.0 version of DOTA dataset.',
           'url': 'http://captain.whu.edu.cn/DOTAweb/',
           'version': '1.0',
           'year': 2018}
    data_dict['info'] = info
    data_dict['images'] = []
    data_dict['categories'] = []
    data_dict['annotations'] = []
    for idex, name in enumerate(wordname):
        single_cat = {'id': idex + 1, 'name': name, 'supercategory': name}
        data_dict['categories'].append(single_cat)

    inst_count = 1
    image_id = 1
    with open(destfile, 'w') as f_out:
        filenames = util.GetFileFromThisRootDir(labelparent)
        for file in filenames:
            CONTAIN_CLS = False # contain or not corresponding classes in the given image
            # annotations
            # 8 coordinates
            objects = util.parse_dota_poly2(file)
            # 4 coordinates
            # objects = util.parse_dota_poly3(file)
            for obj in objects:
                if obj['name'] in wordname:
                    single_obj = {}
                    single_obj['area'] = obj['area']
                    single_obj['category_id'] = wordname.index(obj['name']) + 1
                    single_obj['segmentation'] = []
                    single_obj['segmentation'].append(obj['poly'])
                    single_obj['iscrowd'] = 0
                    xmin, ymin, xmax, ymax = min(obj['poly'][0::2]), min(obj['poly'][1::2]), \
                                             max(obj['poly'][0::2]), max(obj['poly'][1::2])
    
                    width, height = xmax - xmin, ymax - ymin
                    single_obj['bbox'] = xmin, ymin, width, height
                    single_obj['image_id'] = image_id
                    data_dict['annotations'].append(single_obj)
                    single_obj['id'] = inst_count
                    inst_count = inst_count + 1
                    CONTAIN_CLS = True

            # Corresponding image
            if CONTAIN_CLS:
                basename = util.custombasename(file)
                imagepath = os.path.join(imageparent, basename + '.jpg')
                img = cv2.imread(imagepath)
                height, width, c = img.shape
    
                single_image = {}
                single_image['file_name'] = basename + '.jpg'
                single_image['id'] = image_id
                single_image['width'] = width
                single_image['height'] = height
                data_dict['images'].append(single_image)
                image_id = image_id + 1
        json.dump(data_dict, f_out)

if __name__ == '__main__':
    # Train hbb of old task
    # DOTA2COCO('F:\\DIOR\\test', 'F:\\DIOR\\test\\Annotations\\DIOR_test_all.json', wordname_all_20)
    # Val hbb of old task
    DOTA2COCO('F:\DOTAv1.5\\train_Split_800', 'F:\DOTAv1.5\\train_Split_800\Annotations\DOTA_train_all.json', wordname_all_16)
    # Test hbb of old task without annotations
    # DOTA2COCO('F:\workspace\DOTAv1.5\\train', 'F:\workspace\DOTAv1.5\\train\Annotations\DOTA_test_O8.json', wordname_old_8)
    # Train hbb of new task
    # DOTA2COCO('F:\\DIOR\\trainval', 'F:\\DIOR\\trainval\\Annotations\\DIOR_train_N10.json', wordname_new_10)
    # Val hbb of new task
    # DOTA2COCO('F:\DOTAv1.5\\val_Split_800', 'F:\DOTAv1.5\\val_Split_800\Annotations\DOTA_val_N7.json', wordname_new_8)
    # Test hbb of new task without annotations
    # DOTA2COCO('F:\workspace\DOTAv1.5\\train', 'F:\workspace\DOTAv1.5\\train\Annotations\DOTA_test_N7.json', wordname_new_7)
