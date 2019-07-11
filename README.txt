数据库介绍
DOTAv1.5数据集, 包含plane, large ship, small ship, storage tank, baseball diamond, tennis court, basketball court, ground track field, harbor, bridge, small vehicle, helicopter, roundabout, soccer ball field, basketball court and container crane十六类目标, 共2806张图像, DOTAv1.0共标注了188282个实例, DOTAv1.5在此基础上新标记了部分小目标, 并新增了container crane类. 其中ship instances约80000左右.

数据来源
Google Earth, satellite JL-1, and satellite GF-2

数据格式
RGB

分辨率范围
多分辨率, 具体不详

图片尺寸(Height x Width)
800×800 ~ 4000×4000

图片数量
2806

标注类型
Oriented bounding boxes, and Horizontal Bounding Box

标注格式
bbox, category label, difficult label(是否容易识别)
['imagesource': imagesource
'gsd':gsd
x1, y1, x2, y2, x3, y3, x4, y4, category, difficult
x1, y1, x2, y2, x3, y3, x4, y4, category, difficult
...]

检测场景(针对ship)
大部分是近海场景

背景环境
分辨率高，云层干扰少(几乎没有)

文件介绍
train:训练集, 包含图片及图片中实例的标注(斜框和水平框)
val:验证集, 包含图片及图片中实例的标注(斜框和水平框)
test:测试集, 包含测试图片

更多
https://captain-whu.github.io/DOAI2019/dataset.html
https://captain-whu.github.io/DOTA/dataset.html
