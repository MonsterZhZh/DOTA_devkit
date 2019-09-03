import os, sys
import argparse
from PIL import Image

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

if __name__ == '__main__':
	args = parse_args()
	# filterImgs(args.img_dir, args.save_dir)
	rename(args.img_dir)
	removeFileInDir(args.img_dir)