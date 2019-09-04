import os, sys
import argparse
from PIL import Image
import json
from shutil import copyfile

bads = ['00013751.jpg', '00013865.jpg', '00013866.jpg', 
	    '00013869.jpg', '00013872.jpg', '00013873.jpg', 
	    '00013874.jpg', '00013876.jpg', '00100010.jpg', 
	    '00100011.jpg', '00100021.jpg', '00100027.jpg',
	    '00100037.jpg', '00100040.jpg', '00100050.jpg',
	    '00100057.jpg', '00100077.jpg', '00100080.jpg',
	    '00100093.jpg', '00100095.jpg', '00100234.jpg',
	    '00101504.jpg']


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Filter specific images for analysis')
    parser.add_argument('--img_dir', dest='img_dir',
                        help='images path',
                        default='/mnt/USBB/gx/DOTA/DOTA_clip/val/images/', type=str)
    parser.add_argument('--save_dir', dest='save_dir',
                        help='image format',
                        default='/mnt/USBB/gx', type=str)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

def rename(image_path):
	images_lists = os.listdir(image_path)
	for img_name in images_lists:
		img = Image.open(image_path + img_name)
		img = img.convert('RGB') # In case of converting png to jpg reports Alpha error
		new_name = img_name.split('.')[0].strip() + '.jpg'
		img.save(image_path + new_name)

def removeFileInDir(sourceDir):
    for file in os.listdir(sourceDir):
        file = os.path.join(sourceDir,file)
        if os.path.isfile(file) and file.find(".png")>0:
            os.remove(file)
            print (file + " remove succeeded")

def filterImgs(image_path, save_path):
	images_lists = os.listdir(image_path)
	for img_name in images_lists:
		img_name = img_name.split('.')[0].strip() + '.jpg'
		if img_name in bads:
			img = Image.open(image_path + img_name)
			img.save(save_path + img_name)

def select_imgs_from_json(json_file):
	with open(json_file, 'r') as f:
		instances = json.load(f)
		imgs = instances['images']
		img_names = [img['file_name'] for img in imgs]
		base_path = '/home/wsh/DOTAv1.5/coco'
		for img_name in img_names:
			img_path = os.path.join(base_path, 'coco_val2014', img_name)
			save_path = os.path.join(base_path, 'val_N8/imgs', img_name)
			copyfile(img_path, save_path)

def select_txts_from_json(json_file):
	with open(json_file, 'r') as f:
		instances = json.load(f)
		imgs = instances['images']
		img_names = [img['file_name'] for img in imgs]
		base_path = 'F:\\DOTAv1.5\\val_Split_800'
		for img_name in img_names:
			txt_name = img_name.split('.')[0] + '.txt'
			txt_path = os.path.join(base_path, 'labelTxt', txt_name)
			save_path = os.path.join(base_path, 'labelTxt_N8', txt_name)
			copyfile(txt_path, save_path)

if __name__ == '__main__':
	# args = parse_args()
	# filterImgs(args.img_dir, args.save_dir)
	# rename(args.img_dir)
	# removeFileInDir(args.img_dir)
	# select_imgs_from_json('/home/wsh/DOTAv1.5/coco/annotations_N8/instances_val2014.json')
	select_txts_from_json('F:\\DOTAv1.5\\val_Split_800\\Annotations\\DOTA_val_N8.json')
