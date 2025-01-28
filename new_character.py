# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:45:06 2025

@author: 15308
"""
import numpy as np
import os,sys

old_dict = "c2f.npy"
new_dict = "c2f_new.npy"
c2f_dict = np.load(old_dict,allow_pickle=True).item()
print("这个程序通过将几个汉字的部分笔画组合来形成新的汉字。")
print("例如，你可以用‘好’的前三画和‘冼’的后六画来组成‘姺’。")
c = input("请先输入逆向组成的新字\n")
i = 1
traj = []
data = []
print("好的，下面我们用已有的字来组成这个字。要按照新字的顺序。")
while True:
    c0 = input("请输入第%d个已有的汉字。输入'-1'结束\n"%(i))
    if c0 == "-1":
        break
    if c0 not in c2f_dict.keys():
        print("很可惜，'%s'也不是已有的汉字"%(c0))
        continue
    info = c2f_dict[c0]
    stroke_matrix = list(np.load(info[0]).values())[0]
    s_info = input("请输入要选取的笔画，以空格间隔。比如第3-7画，就输入'3 4 5 6 7'\n")
    try:
        s = [int(si)-1 for si in s_info.split()]
    except:
        print("'%s'不是一个正整数！")
        continue
    if max(s) >= len(stroke_matrix) or min(s) < 0:
        print("输入的笔画数有误！大于最大笔画数或小于0。")
    for j in s:
        traj.append(info[1][j])
    data.append(list(np.load(info[0]).values())[0][s])
    i += 1

if len(data) < 2:
    print("没有输入足够的汉字！")
    input("任意键退出")
    sys.exit()
data = np.vstack(data)
file_id = max([
    int(f.split(".npz")[0].split("_")[-1]) for f in os.listdir(
        "Chinese-Character-Stroke-Sequence-Dataset-main/data/npz/")
    ]) + 1
filename = "Chinese-Character-Stroke-Sequence-Dataset-main/data/npz/chinese_kaiti_%d.npz"%(
    file_id)
np.savez_compressed(filename,binary=data)
c2f_dict[c] = (filename,traj)
np.save(new_dict,c2f_dict)
print("已成功更新到c2f_new.npy。\n如需使用，请把c2f_new.npy重命名为c2f.npy。")
input("任意键退出")
sys.exit()
