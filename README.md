用于构建蛇年拜年动图，效果如下图所示：
Creating a New Year greeting animation, as shown in the GIF below

主要流程是加载一个逐个笔画拆开的图片数据文件（来自https://github.com/Lex-voda/Chinese-Character-Stroke-Sequence-Dataset），找到最粗的笔画，由此定义一条进入的路径，然后让一条蛇在这条路径上运动。蛇通过蛇头和蛇身组成，蛇头用的网络图片（https://pic.616pic.com/ys_bnew_img/00/50/82/CmwMozANM7.jpg），蛇身本质是散点图，末尾的蛇身散点逐渐变小，形成蛇尾的形状。
The main process involves loading an image data file that is broken down into individual strokes (from https://github.com/Lex-voda/Chinese-Character-Stroke-Sequence-Dataset). The thickest stroke is identified to define a path for movement. A snake will then move along this path. The snake is composed of a head and a body, with the head using a network image (https://pic.616pic.com/ys_bnew_img/00/50/82/CmwMozANM7.jpg). The body of the snake is essentially a scatter plot, with the points at the end of the snake's body gradually decreasing in size to form the shape of the tail.

欢迎魔改
Feel free to modify as you wish!
