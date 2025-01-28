# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 18:15:50 2025

@author: Jinyin Zha
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.image as mpimg
from scipy import ndimage
import sys,os
import time

def in_path(mx,my,step=2):
    path_xs = []
    path_ys = []
    l = 0
    mx = mx.tolist()
    my = my.tolist()
    #fit ini path
    if mx[1]-mx[0] == 0:
        k_ini = (my[1]-my[0]) / (mx[1]-mx[0]+0.1)
    else:
        k_ini = (my[1]-my[0]) / (mx[1]-mx[0])
    b_ini = my[1] - k_ini * mx[1]
    if abs(k_ini) < 0.1:
        if mx[0] > mx[1]:
            mx = [max_length*1024] + my
            my = [k_ini*max_length*1024+b_ini] + mx
        else:
            mx = [0] + mx
            my = [b_ini] + my
    else:
        if my[0] > my[1]:
            my = [1024+y_margin] + my
            mx = [(1024+y_margin-b_ini)/k_ini] + mx
        else:
            my = [-y_margin] + my
            mx = [(-y_margin-b_ini)/k_ini] + mx
    #inteporlate between each crucial point
    for i in range(len(mx)-1):
        d = ((my[i]-my[i+1])**2 + (mx[i]-mx[i+1])**2)**0.5
        n_dot = int(d/step) + 1
        path_xs += np.linspace(mx[i],mx[i+1],n_dot)[:-1].tolist()
        path_ys += np.linspace(my[i],my[i+1],n_dot)[:-1].tolist()
        if i > 0:
            l += n_dot
    path_xs.append(mx[-1])
    path_ys.append(my[-1])   
    return path_xs,path_ys,l

def rotate(img,angle):    
    rotated_img = ndimage.rotate(img,angle , reshape=False)
    height, width = rotated_img.shape[0:2]
    rgba_img = np.zeros((height, width, 4), dtype=np.uint8)
    rgba_img[..., :3] = rotated_img[..., :3]  
    threshold_black = 10  
    threshold_white = 245  
    alpha_channel = np.ones((height, width), dtype=np.uint8) * 255  # 默认完全不透明
    for i in range(height):
        for j in range(width):
            if rotated_img[i,j,0] < threshold_black and rotated_img[i,j,1] < threshold_black and rotated_img[i,j,2] < threshold_black:
                alpha_channel[i,j] = 0
            if rotated_img[i,j,0] > threshold_white and rotated_img[i,j,1] > threshold_white and rotated_img[i,j,2] > threshold_white:
                alpha_channel[i,j] = 0
            if i == 0 or i == height-1 or j == 0 or j == width-1:
                alpha_channel[i,j] = 0
    rgba_img[..., 3] = alpha_channel
    return rgba_img

def animate(gf):
    #1,get which character to change -> j
    for j in range(len(ed_ts)):
        if ed_ts[j] > gf:
            break
    if j == 0:
        i = gf
    else:
        i = gf - ed_ts[j-1]
    ls = all_snake_ls[j]
    mxs = all_snake_xs[j]
    mys = all_snake_ys[j]
    snake = all_snakes[j]
    head_image = all_heads[j]    
    move_step = all_move_steps[j]
    mx = mxs[i*move_step:i*move_step+ls]
    my = mys[i*move_step:i*move_step+ls]
    if i*move_step+ls > len(mxs):
        pbar(gf)
        return snake, head_image,
    snake.set_offsets(np.c_[mx, my])
    #head
    x_head_min = min(mx[-1],mx[-2])
    x_head_max = max(mx[-1],mx[-2])
    y_head_min = min(my[-1],my[-2])
    y_head_max = max(my[-1],my[-2])
    if mx[-1] == mx[-2]:
        angle = np.sign(my[-1]-my[-2]) * 90
    else:
        angle = np.arctan((my[-1]-my[-2])/(mx[-1]-mx[-2]))/np.pi*180
    if mx[-1] < mx[-2]:
        angle += 180
    x_st = x_head_min - 50
    x_ed = x_head_max + 50
    y_st = y_head_min - 50
    y_ed = y_head_max + 50 
    head_image.set_data(rotate(snake_head_img,angle))
    head_image.set_extent((x_st,x_ed,y_st,y_ed))
    pbar(gf)
    return snake, head_image,

def pbar(gf):
    ggf = gf + 1
    percentage = int(ggf/n_frame*100)
    n_bar = int(ggf/n_frame*50)
    dt = int(time.time()-t0)
    t_tot = int(dt * n_frame / ggf)
    print("\r", end="")
    print("进度: %d%%: |%s|%d:%d/%d:%d"%(percentage,
                                       "█"*n_bar+" "*(50-n_bar),
                                       dt//60,dt%60,t_tot//60,t_tot%60),
          end="")
    sys.stdout.flush()

if __name__ =="__main__":
    
    snake_size = 20
    move_step = 20
    y_margin = 500
    fps = 30
    t1 = 1
    t_wait = 0.5
    t_final_wait = 1
    c2f_dict = np.load("c2f.npy",allow_pickle=True).item()
    
    names = [input("请输入姓名\n")]
    for name in names:
        try:
            #Initialize configures
            gif_name = "%s.gif"%(name)
            if os.path.exists("wechat/%s"%(gif_name)):
                continue
            cs = "%s@@蛇年快乐"%(name)
            all_snake_xs = []
            all_snake_ys = []
            all_snake_ls = []
            all_snakes = []
            all_heads = []
            all_move_steps = []
            ed_ts = []
            #initialize th figure
            print("初始化...")
            fig,ax = plt.subplots(dpi=150)
            #loop each character
            max_length = max([len(line) for line in cs.split("@@")])
            for line_id,line in enumerate(cs.split("@@")):
                dy = line_id * 1024
                for i,c in enumerate(line):
                    #Calculate movements
                    dx = ((max_length-len(line))/2+i)*1024
                    #load stroke data
                    if c not in c2f_dict.keys():
                        print("%s不在保存的文字中，请使用new_character来更新!"%(c))
                        input("任意键退出")
                        sys.exit()
                    stroke_data = list(np.load(c2f_dict[c][0]).values())[0]
                    #find the stroke to be changed into snake
                    max_w_id = np.argmax(np.sum(stroke_data>0,axis=(1,2)))
                    trajs = np.array(c2f_dict[c][1][max_w_id])
                    #pack and resize the rest cahracter
                    stacked_stroke_data = stroke_data[[i for i in range(len(stroke_data)) if i != max_w_id]].sum(0)
                    height,width = stroke_data.shape[1:]
                    rgba = np.zeros((height,width,4))
                    for i in range(height):
                        for j in range(width):
                            if stacked_stroke_data[i,j]> 0:
                                rgba[i,j] = [0,0,0,255]
                            else:
                                rgba[i,j] = [255,255,255,0]
                    rgba = rgba.astype(np.int32)
                    #get the snake path
                    x,y = np.nonzero(stroke_data[max_w_id])
                    kx = (y.max()-y.min()) / (trajs[:,0].max()-trajs[:,0].min())
                    bx = y.max() - kx * trajs[:,0].max()
                    ky = (x.min()-x.max()) / (trajs[:,1].max()-trajs[:,1].min())
                    by = x.min() - ky * trajs[:,1].max()
                    mx = kx*trajs[:,0] + bx + dx
                    my = ky*trajs[:,1] + by + dy
                    path_xs,path_ys,l = in_path(mx,my)
                    ls = l
                    #show the character
                    ax.imshow(rgba,extent=(0+dx,1024+dx,1024+dy,0+dy))
                    #initialize the snake
                    l_tail = int(0.2*l)
                    s = np.linspace(1,snake_size,l_tail).tolist() + (l-l_tail) * [snake_size]
                    snake = ax.scatter(len(s)*[-100],len(s)*[-100], s=s,color='#9BBD4C')
                    snake_head_img = mpimg.imread('head.jpg') 
                    head_image = ax.imshow(snake_head_img, aspect='equal', extent=(0, 10, 0, 10), zorder=5)
                    #save information
                    all_snake_xs.append(path_xs)
                    all_snake_ys.append(path_ys)
                    all_snake_ls.append(l)
                    all_snakes.append(snake)
                    all_heads.append(head_image)
                    move_step = int((len(path_xs)-l)/(t1*fps))
                    all_move_steps.append(move_step)
                    if len(ed_ts) == 0:
                        ed_ts.append(int((len(path_xs)-l) / move_step + 1 + t_wait*fps))
                    else:
                        ed_ts.append(ed_ts[-1] + int((len(path_xs)-l) / move_step + 1 + t_wait*fps))
            #set figure configures
            ax.set_xlim(0,1024*max_length)
            ax.set_ylim(len(cs.split("@@"))*1024,0)
            plt.axis('off')
            #make animation
            n_frame = ed_ts[-1]+t_final_wait*fps
            t0 = time.time()
            ani = animation.FuncAnimation(fig, animate, frames=n_frame, interval=50, blit=True)
            ani.save(gif_name, writer='pillow', fps=fps,savefig_kwargs={'transparent': True})
            plt.close()
            print("\n成功！图片已保存为【%s】"%(gif_name))
            input("任意键退出")
            sys.exit()
            
        except Exception as e:
            print("出问题了，请查看fail.txt")
            f = open("fail.txt","w")
            f.write("%s: %s\n"%(name,e))
            f.close()
            input("任意键退出")
            sys.exit()

    
    
    

