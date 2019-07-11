import dota_utils as util
import os
import cv2
import json

# Old task 8 classes
wordname_old_8 = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court']
# New task 7 classes
wordname_new_7 = ['basketball-court', 'storage-tank',  'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool', 'helicopter']

def DOTA2COCO(srcpath, destfile, wordname):
    imageparent = os.path.join(srcpath, 'images', 'images')
    labelparent = os.path.join(srcpath, 'labelTxt-v1.0', 'Val_Task2_gt')

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
            objects = util.parse_dota_poly2(file)
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
    # DOTA2COCO('F:\workspace\DOTAv1.5\\train', 'F:\workspace\DOTAv1.5\\train\Annotations\DOTA_train_O8.json', wordname_old_8)
    # Val hbb of old task
    DOTA2COCO('F:\workspace\DOTAv1.5\\val', 'F:\workspace\DOTAv1.5\\val\Annotations\DOTA_val_O8.json', wordname_old_8)
    # Test hbb of old task without annotations
    # DOTA2COCO('F:\workspace\DOTAv1.5\\train', 'F:\workspace\DOTAv1.5\\train\Annotations\DOTA_test_O8.json', wordname_old_8)
    # Train hbb of new task
    # DOTA2COCO('F:\workspace\DOTAv1.5\\train', 'F:\workspace\DOTAv1.5\\train\Annotations\DOTA_train_N7.json', wordname_new_7)
    # Val hbb of new task
    DOTA2COCO('F:\workspace\DOTAv1.5\\val', 'F:\workspace\DOTAv1.5\\val\Annotations\DOTA_val_N7.json', wordname_new_7)
    # Test hbb of new task without annotations
    # DOTA2COCO('F:\workspace\DOTAv1.5\\train', 'F:\workspace\DOTAv1.5\\train\Annotations\DOTA_test_N7.json', wordname_new_7)
