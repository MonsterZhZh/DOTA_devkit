import os
import xml.etree.ElementTree as ET
import glob

# LabelTxtv1.5
# Old task 8 classes
wordname_old_8 = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court']
# New task 8 classes
wordname_new_8 = ['basketball-court', 'storage-tank',  'soccer-ball-field', 'turntable', 'harbor', 'swimming-pool', 'helicopter', 'container-crane']

def merge_to_single_cls(txt_path, save_path, class_name):
	image_name_lists = os.listdir(txt_path)
	with open(txt_path + save_path, 'w') as w:
		for image_name in image_name_lists:
			with open(txt_path + image_name, 'r') as r:
				lines = r.readlines()
				splitlines = [x.strip().replace(' ','').split(',') for x in lines]
				for splitline in splitlines:
					if splitline[4] == class_name:
						w.write('{:s} {:.3f} {:.0f} {:.0f} {:.0f} {:.0f}\n'.format(image_name.split('.')[0], float(splitline[5]), float(splitline[0]), float(splitline[1]), float(splitline[2]), float(splitline[3])))
					elif splitline[5] == class_name:
						w.write('{:s} {:.3f} {:.0f} {:.0f} {:.0f} {:.0f}\n'.format(image_name.split('.')[0], float(splitline[4]), float(splitline[0]), float(splitline[1]), float(splitline[2]), float(splitline[3])))
					else:
						print('No matching class found in the:', image_name)

def merge_to_multiple_cls(txt_path, save_path, class_names):
	image_name_lists = os.listdir(txt_path)
	for class_name in class_names:
		save_path = '/home/wsh/DOTAv1.5/coco/dets/' + class_name + '.txt'
		with open(save_path, 'w') as w:
			for image_name in image_name_lists:
				with open(txt_path + image_name, 'r') as r:
					lines = r.readlines()
					splitlines = [x.strip().replace(' ','').split(',') for x in lines]
					for splitline in splitlines:
						if splitline[4] == class_name:
							w.write('{:s} {:.3f} {:.0f} {:.0f} {:.0f} {:.0f}\n'.format(image_name.split('.')[0], float(splitline[5]), float(splitline[0]), float(splitline[1]), float(splitline[2]), float(splitline[3])))
						elif splitline[5] == class_name:
							w.write('{:s} {:.3f} {:.0f} {:.0f} {:.0f} {:.0f}\n'.format(image_name.split('.')[0], float(splitline[4]), float(splitline[0]), float(splitline[1]), float(splitline[2]), float(splitline[3])))
						else:
							print('No matching class found in the:', image_name)


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars

def covert_gt_xml_to_txt(xml_path, save_path):
	xml_lists = glob.glob(xml_path + '/*.xml')
	for xml in xml_lists:
		tree = ET.parse(xml)
		root = tree.getroot()
		Objects = root.findall('object')
		txt_name = os.path.basename(xml).split('.')[0] + '.txt'
		with open(save_path + txt_name, 'w') as w:
			for Obj in Objects:
				bndbox = get_and_check(Obj, 'bndbox', 1)
				xmin = float(get_and_check(bndbox, 'xmin', 1).text)
				ymin = float(get_and_check(bndbox, 'ymin', 1).text)
				xmax = float(get_and_check(bndbox, 'xmax', 1).text)
				ymax = float(get_and_check(bndbox, 'ymax', 1).text)
				name = Obj.findall('name')[0].text
				w.write('{:.0f} {:.0f} {:.0f} {:.0f} {:s}\n'.format(xmin, ymin, xmax, ymax, name))


def record_imagesetfile(image_path, save_path):
	image_name_lists = os.listdir(image_path)
	with open(save_path + 'imagesetfile.txt', 'w') as w:
		for image_name in image_name_lists:
			w.write('{:s}\n'.format(image_name.split('.')[0]))


if __name__ == '__main__':
	# merge_to_single_cls('F:\\DOTA_devkit-master\\detection_results\\FPN\\', 'Vehicle.txt', 'Vehicle')
	# merge_to_single_cls('ensamble/', 'Vehicle.txt', 'Vehicle')
	# merge_to_single_cls('F:\\DOTA_devkit-master\\detection_results\\cascade_rcnn\\', 'Vehicle.txt', 'Vehicle')
	merge_to_multiple_cls('/home/wsh/DOTAv1.5/coco/dets/txts/', '/home/wsh/DOTAv1.5/coco/dets/', wordname_old_8)
	# covert_gt_xml_to_txt('F:\\UAV\\all\\Annotations\\', 'GT\\')
	# record_imagesetfile('/home/wsh/DOTAv1.5/coco/val_N8', '/home/wsh/DOTAv1.5/coco/GT/')