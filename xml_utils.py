import os  
import xml.etree.ElementTree as ET
import random
# from lxml.etree import Element, SubElement, tostring
from xml.etree.ElementTree import ElementTree, Element
from xml.dom.minidom import parseString
import glob
from shutil import copyfile

from operator import itemgetter

def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars

def calculate(annotations, images):
	'''
	Summarize total number of categories, images, and instances for each category

	Input: 
		annotations file path
		images file path
	Output: 
		list of categories
		list of the number of images corresponding to categories
		list of the number of instances corresponding to categories
	'''

	categories = []
	num_imgs = []
	num_ins = []
	ratios = []

	xml_lists = glob.glob(annotations + '/*.xml')

	# Check if there is no corresponding images
	xml_basenames = []
	for item in xml_lists:
		xml_basenames.append(os.path.basename(item))
	xml_names = []
	for item in xml_basenames:
		temp1, temp2 = os.path.splitext(item)
		img_path = images + temp1 + '.jpg'
		if os.path.exists(img_path):
			xml_names.append(temp1)
		else:
			print('Without corresponding image:' + temp1 + '.xml')

	# calculate statics
	for it in xml_names:
		tree = ET.parse(os.path.join(annotations, str(it) + '.xml'))
		root = tree.getroot()
		node_root = Element('annotation')
		# node_folder = SubElement(node_root, 'folder')
		# node_folder.text = ''
		# node_filename = SubElement(node_root, 'filename')
		# node_filename.text = str(it)+'.jpg'
		# Calculate the number of images and instances
		Objects = root.findall('object')
		if len(Objects) == 0:
			print('No instance in such image:' + str(it) + '.jpg')
		else:
			names = []
			for Object in Objects:
				name = Object.find('name').text
				if name not in categories:
					categories.append(name)
					num_ins.append(1)
					num_imgs.append(1)
				else:
					i = categories.index(name)
					num_ins[i] += 1
					if name not in names:
						num_imgs[i] += 1
				if name not in names:
					names.append(name)
		# Calculate the width and height of images
		size = root.find('size') # return an Element
		width = int(size.findall('width')[0].text) # return a list of Element
		height = int(size.findall('height')[0].text)
		if (width, height) not in ratios:
			ratios.append((width, height))



	return categories, num_imgs, num_ins, ratios


def split(annotations, images):
	'''
	Split total annotations and images into train and validation sets. 

	Input:
		annotations file path
		images file path
	'''
	xml_lists = glob.glob(annotations + '/*.xml')
	random.seed(len(xml_lists))
	# Randomly choose 355 images as validation set
	val_xml_lists = random.sample(xml_lists, 355)
	for val in val_xml_lists:
		item = os.path.basename(val)
		basename, tmp = os.path.splitext(item)
		copyfile(val, 'F:\\UAV\\val\\Annotations\\' + basename  + '.xml')
		img_name = basename + '.jpg'
		copyfile(images + img_name, 'F:\\UAV\\val\\JPEGImages\\' + img_name)
	for xml in xml_lists:
		if xml not in val_xml_lists:
			item = os.path.basename(xml)
			basename, tmp = os.path.splitext(item)
			copyfile(xml, 'F:\\UAV\\train\\Annotations\\' + basename + '.xml')
			img_name = basename + '.jpg'
			copyfile(images + img_name, 'F:\\UAV\\train\\JPEGImages\\' + img_name)

def modify_xml(annotations):
	'''
	Modify some node or values in xml annotation file

	Input: annotations file path
	'''
	xml_lists = glob.glob(annotations + '/*.xml')
	for xml in xml_lists:
		updateTree = ET.parse(xml)
		root = updateTree.getroot()

		# Inconsistent image folder
		# folder = root.find('folder')
		# folder.text = 'JPEGImages'

		# Convert coordinates of bounding box [xmin, ymin, xmax, ymax] into [x1,y1,x2,y2,x3,y3,x4,y4]
		Objects = root.findall('object')
		if len(Objects) == 0:
			print('No instances in such image:' + str(xml) + '.jpg')
		else:
			for Obj in Objects:
				bndbox = get_and_check(Obj, 'bndbox', 1)
				xmin = get_and_check(bndbox, 'xmin', 1) # x1
				x1 = xmin.text
				bndbox.remove(xmin)
				ymin = get_and_check(bndbox, 'ymin', 1) # y1
				y1 = ymin.text
				bndbox.remove(ymin)
				xmax = get_and_check(bndbox, 'xmax', 1) # x3
				x3 = xmax.text
				bndbox.remove(xmax)
				ymax = get_and_check(bndbox, 'ymax', 1) # y3
				y3 = ymax.text
				bndbox.remove(ymax)

				x1_node = Element('x0')
				x1_node.text = x1
				bndbox.append(x1_node)
				y1_node = Element('y0')
				y1_node.text = y1
				bndbox.append(y1_node)

				x2_node = Element('x1')
				x2_node.text = x3
				bndbox.append(x2_node)
				y2_node = Element('y1')
				y2_node.text = y1
				bndbox.append(y2_node)

				x3_node = Element('x2')
				x3_node.text = x3
				bndbox.append(x3_node)
				y3_node = Element('y2')
				y3_node.text = y3
				bndbox.append(y3_node)

				x4_node = Element('x3')
				x4_node.text = x1
				bndbox.append(x4_node)
				y4_node = Element('y3')
				y4_node.text = y3
				bndbox.append(y4_node)

		updateTree.write(xml)



if __name__ == '__main__':
	origin_ann_dir = 'F:\\DIOR\\Annotations\\'
	img_dir = 'F:\\DIOR\\JPEGImages-test\\'

	categories, num_imgs, num_ins, ratios = calculate(origin_ann_dir, img_dir)
	print('categories:', categories)
	print('number of imaegs:', num_imgs)
	print('number of instances:', num_ins)
	print('types of ratios:', ratios)
	print(sorted(ratios, key=itemgetter(1)))

	# split(origin_ann_dir, img_dir)
	# modify_xml('/home/jzchen/data/UAV/val/Annotations/')
	# modify_xml('/home/jzchen/data/UAV/train/Annotations/')
	# modify_xml('F:\\UAV\\Annotations\\')

	
		