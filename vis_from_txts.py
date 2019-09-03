import numpy as np
import cv2
import os

LABEl_NAME_MAP = ['background', 'plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court']
categories = []

def draw_box_cv(img, boxes, labels, scores=None):
    boxes = boxes.astype(np.int64)
    labels = labels.astype(np.int32)
    img = np.array(img, np.float32)
    img = np.array(img*255/np.max(img), np.uint8)

    num_of_object = 0
    for i, box in enumerate(boxes):
        xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]

        label = labels[i]
        if label != 0:
            num_of_object += 1
            # color = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
            color = (0, 255, 0)
            cv2.rectangle(img,
                          pt1=(xmin, ymin),
                          pt2=(xmax, ymax),
                          color=color,
                          thickness=2)
            category = LABEl_NAME_MAP[label]

            if scores is not None:
                cv2.rectangle(img,
                              pt1=(xmin, ymin),
                              pt2=(xmin + 120, ymin + 15),
                              color=color,
                              thickness=-1)
                cv2.putText(img,
                            text=category+": "+str(scores[i]),
                            org=(xmin, ymin+10),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
            else:
                cv2.rectangle(img,
                              pt1=(xmin, ymin),
                              pt2=(xmin + 40, ymin + 15),
                              color=color,
                              thickness=-1)
                cv2.putText(img,
                            text=category,
                            org=(xmin, ymin + 10),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
    cv2.putText(img,
                text=str(num_of_object),
                org=((img.shape[1]) // 2, (img.shape[0]) // 2),
                fontFace=3,
                fontScale=3,
                color=(0, 0, 255))
    return img

def display_imgs(anno_file_path, img_file_path, display_path):
    txt_names = os.listdir(anno_file_path)
    for txt_name in txt_names:
        boxes = []
        labels = []
        with open(os.path.join(anno_file_path, txt_name), 'r') as f:
            lines = f.readlines()
            for line in lines:
                splitline = line.strip().split(' ')
                if (len(splitline) < 9):
                    continue
                if (len(splitline) >= 9):
                    cls_name = splitline[8]
                    coordinates = [float(splitline[i]) for i in range(0, 8)]
                    if cls_name in LABEl_NAME_MAP:
                        xmin, ymin, xmax, ymax = min(coordinates[0::2]), min(coordinates[1::2]), max(coordinates[0::2]), max(coordinates[1::2])
                        boxes.append([xmin, ymin, xmax, ymax])
                        labels.append(LABEl_NAME_MAP.index(cls_name))
        boxes = np.array(boxes, dtype=np.int64)
        labels = np.array(labels, dtype=np.int32)
        if len(boxes) != 0:
            img_name = txt_name.strip().split('.')[0] + '.jpg'
            img = cv2.imread(os.path.join(img_file_path, img_name))
            displayed_img = draw_box_cv(img, boxes, labels)
            cv2.imwrite(os.path.join(display_path, img_name), displayed_img)

def display_all_categories(anno_file_path):
    txt_names = os.listdir(anno_file_path)
    for txt_name in txt_names:
        with open(os.path.join(anno_file_path, txt_name), 'r') as f:
            lines = f.readlines()
            for line in lines:
                splitline = line.strip().split(' ')
                if (len(splitline) < 9):
                    continue
                if (len(splitline) >= 9):
                    cls_name = splitline[8]
                    if cls_name not in categories:
                        categories.append(cls_name)
    print('All categories:\n',categories)


if __name__ == "__main__":
    # display_imgs('F:\\DOTAv1.5\\val_Split_800\\labelTxt\\', 'F:\\DOTAv1.5\\val_Split_800\\images\\', 'F:\\DOTAv1.5\\val_Split_800\\vis_val_Split\\')
    display_imgs('F:\\DOTAv1.5\\train_Split_800\\labelTxt\\', 'F:\\DOTAv1.5\\train_Split_800\\images\\', 'F:\\DOTAv1.5\\train_Split_800\\vis_train_Split\\')
    # display_all_categories('F:\\labelTxt-v1.0\\Val_Task2_gt\\valset_reclabelTxt\\')