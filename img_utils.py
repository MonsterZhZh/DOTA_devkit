from PIL import Image
import os, sys
import cv2
import numpy as np

def convert_img_format(img_dir, save_dir, img_format):
	'''
	img_dir (str): the directory of images needed to be converted
	save_dir (str): the directory of images to be saved after conversion
	format (str): the format of images to be converted
	'''
	file_list = os.listdir(img_dir) 
	for file_name in file_list:
		path = img_dir + file_name
		img = Image.open(path)
		rgb_img = img.convert('RGB')
		rgb_img.save(save_dir+file_name[:-4]+img_format) # default appendix of images is '.png'

def show_boxes_in_img(img_dir, anno_dir, save_dir):
	img_list = os.listdir(img_dir)
	for img_name in img_list:
		img = Image.open(img_dir + img_name)
		txt = open(anno_dir + img_name[:-4] + '.txt', "r")
		coordinates = []
		labels = []
		for line in txt.readlines():
			line_list = line.split()
			if len(line_list) > 1:
				coordinates.append(line_list[:-2])
				labels.append(line_list[-2])
		coordinates = np.array(coordinates, np.float32)
		coordinates = back_forward_convert(coordinates, False)
		img_show_gt = draw_rotate_box_cv(img, coordinates, labels, None)
		cv2.imwrite(save_dir+img_name, img_show_gt)




def forward_convert(coordinate, with_label=True):
    """
    :param coordinate: format [x_c, y_c, w, h, theta]
    :return: format [x1, y1, x2, y2, x3, y3, x4, y4]
    """
    boxes = []
    if with_label:
        for rect in coordinate:
            box = cv2.boxPoints(((rect[0], rect[1]), (rect[2], rect[3]), rect[4]))
            box = np.reshape(box, [-1, ])
            boxes.append([box[0], box[1], box[2], box[3], box[4], box[5], box[6], box[7], rect[5]])
    else:
        for rect in coordinate:
            box = cv2.boxPoints(((rect[0], rect[1]), (rect[2], rect[3]), rect[4]))
            box = np.reshape(box, [-1, ])
            boxes.append([box[0], box[1], box[2], box[3], box[4], box[5], box[6], box[7], box[6]])

    return np.array(boxes, dtype=np.float32)


def back_forward_convert(coordinate, with_label=True):
    """
    :param coordinate: format [x1, y1, x2, y2, x3, y3, x4, y4, (label)] 
    :param with_label: default True
    :return: format [x_c, y_c, w, h, theta, (label)]
    """

    boxes = []
    if with_label:
        for rect in coordinate:
            box = np.int0(rect[:-1])
            box = box.reshape([4, 2])
            rect1 = cv2.minAreaRect(box)

            x, y, w, h, theta = rect1[0][0], rect1[0][1], rect1[1][0], rect1[1][1], rect1[2]
            boxes.append([x, y, w, h, theta, rect[-1]])

    else:
        for rect in coordinate:
            box = np.int0(rect)
            box = box.reshape([4, 2])
            rect1 = cv2.minAreaRect(box)

            x, y, w, h, theta = rect1[0][0], rect1[0][1], rect1[1][0], rect1[1][1], rect1[2]
            boxes.append([x, y, w, h, theta])

    return np.array(boxes, dtype=np.float32)

def draw_rotate_box_cv(img, boxes, labels, scores):
    boxes = boxes.astype(np.int64)
    img = np.array(img, np.float32)
    img = np.array(img*255/np.max(img), np.uint8)

    num_of_object = 0
    for i, box in enumerate(boxes):
        x_c, y_c, w, h, theta = box[0], box[1], box[2], box[3], box[4]

        category = labels[i]
        if category != '':
            num_of_object += 1
            # color = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
            color = (0, 255, 0)
            rect = ((x_c, y_c), (w, h), theta)
            rect = cv2.boxPoints(rect)
            rect = np.int0(rect)
            cv2.drawContours(img, [rect], -1, color, 2)

            if scores is not None:
                # cv2.rectangle(img,
                #               pt1=(x_c, y_c),
                #               pt2=(x_c + 120, y_c + 15),
                #               color=color,
                #               thickness=-1)
                cv2.putText(img,
                            text=category+": "+str(scores[i]),
                            org=(x_c, y_c+10),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
                cv2.putText(img,
                            text="angle:{}".format(theta),
                            org=(x_c, y_c + 30),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
            else:
                # cv2.rectangle(img,
                #               pt1=(x_c, y_c),
                #               pt2=(x_c + 40, y_c + 15),
                #               color=color,
                #               thickness=-1)
                # cv2.putText(img,
                #             text=category,
                #             org=(x_c, y_c + 10),
                #             fontFace=1,
                #             fontScale=1,
                #             thickness=2,
                #             color=(color[1], color[2], color[0]))
                cv2.putText(img,
                            text="angle{}".format(theta),
                            org=(x_c, y_c + 30),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))

    cv2.putText(img,
                text=str(num_of_object),
                org=((img.shape[1]) // 2, (img.shape[0]) // 2),
                fontFace=3,
                fontScale=1,
                color=(255, 0, 0))
    return img

if __name__ == '__main__':
	img_dir = input('Please input the directory of images needed to converted:')
	save_dir = input('Please input the directory of images to be saved：')
	img_format = input('Please input the format of images to be converted:')
	convert_img_format(img_dir, save_dir, img_format)
	# show_boxes_in_img('F:\workspace\DOTAv1.5\\train\images\images_jpg\\', 'F:\workspace\DOTAv1.5\\train\labelTxt-v1.0\labelTxt\\', 'F:\workspace\DOTAv1.5\\train\images\images_show_gt\\')
	# show_boxes_in_img('F:\workspace\DOTAv1.5\\train\images\images_jpg\\', 'F:\workspace\DOTAv1.5\\train\labelTxt-v1.0\Train_Task2_gt\\', 'F:\workspace\DOTAv1.5\\train\images\images_show_gt\\')