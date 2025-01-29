用于构建蛇年拜年动图，灵感来自小红书（http://xhslink.com/a/CYi73XPYWIM4 ）。效果如下图所示：

Creating a New Year greeting animation, which is inspired by rednote (http://xhslink.com/a/CYi73XPYWIM4 ), as shown in the GIF below

![demo](https://github.com/user-attachments/assets/70171e69-cb9d-4ebb-8295-6bcc71fda045)

主要流程是加载一个逐个笔画拆开的图片数据文件（来自https://github.com/Lex-voda/Chinese-Character-Stroke-Sequence-Dataset ），找到最粗的笔画，由此定义一条进入的路径，然后让一条蛇在这条路径上运动。蛇通过蛇头和蛇身组成，蛇头用的网络图片（https://pic.616pic.com/ys_bnew_img/00/50/82/CmwMozANM7.jpg ），蛇身本质是散点图，末尾的蛇身散点逐渐变小，形成蛇尾的形状。

The main process involves loading an image data file that is broken down into individual strokes (from https://github.com/Lex-voda/Chinese-Character-Stroke-Sequence-Dataset). The thickest stroke is identified to define a path for movement. A snake will then move along this path. The snake is composed of a head and a body, with the head using a network image (https://pic.616pic.com/ys_bnew_img/00/50/82/CmwMozANM7.jpg). The body of the snake is essentially a scatter plot, with the points at the end of the snake's body gradually decreasing in size to form the shape of the tail.

笔画数据文件需要clone https://github.com/Lex-voda/Chinese-Character-Stroke-Sequence-Dataset ，运行run.py来获得。如果您有百度网盘，也可以直接下载，然后解压在本项目的文件夹下。链接：https://pan.baidu.com/s/1oye4fGHLLi5sgblYl7MYTA?pwd=wklz  提取码：wklz 

The stroke data file needs to be cloned from https://github.com/Lex-voda/Chinese-Character-Stroke-Sequence-Dataset and run run.py to obtain it. If you have Baidu Cloud, you can also download it directly and then extract it into the folder of this project. Link: https://pan.baidu.com/s/1oye4fGHLLi5sgblYl7MYTA?pwd=wklz Extraction code: wklz.


运行环境：

Environment:

python==3.9

numpy==1.23.0

scipy==1.13.1

matplotlib==3.9.3


欢迎魔改

Feel free to modify as you wish!
