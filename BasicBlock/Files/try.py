import matplotlib.pyplot as plt
import pydicom as pydcm
import numpy as np
import cv2 as cv
import cv2
import os
import  nibabel as nib

def readfile(path):
    filename = []
    for root, dir, files in os.walk(path):
        for file in files:
            #if ".dcm" in file.lower():
            filename.append(os.path.join(root, file))
    return filename


def tranform(file,save):
    data = pydcm.read_file(file, force=True)
    if 'NumberOfFrames' in dir(data):
        name = file.split("\\")[-1]
        name += '.avi'
        fps = 30
        frames, width, height, channels = data.pixel_array.shape
        fourcc = cv.VideoWriter_fourcc('M', 'J', 'P',
                                       'G')  # 输出格式'M', 'J', 'P', 'G'或'I', '4', '2', '0'或'P', 'I', 'M', 'I'
        out = cv.VideoWriter(os.path.join(save, name), fourcc, fps, (height, width), False)  # Attention if the  vedio is gray type.The false must be change into True
        print(os.path.join(save, name))
        # data = []
        if 'PixelSpacing' in dir(data):
            cur_spacing = float(data.PixelSpacing[0])
        for idx in range(frames):
            nii_data_array = data.pixel_array
            frame_img = nii_data_array[idx]
            if (len(frame_img.shape) == 2):  # gray image
                frame_img = cv.cvtColor(frame_img, cv.COLOR_GRAY2BGR)
            elif (len(frame_img.shape) == 3):  # color image
                frame_img = cv.cvtColor(frame_img, cv.COLOR_YUV2BGR)
                # frame_img = cv.cvtColor(frame_img, cv.COLOR_BGR2GRAY)
                # print(frame_img.shape)
            # data.append(frame_img)
            out.write(frame_img)

def Dicom2avi():
    change_list = ['二尖瓣短轴','乳头肌短轴','心尖短轴', '心尖两腔','心尖三腔','心尖四腔'] #二尖瓣短轴
    path = "G:\正常对照组造影动态视频DICOM\GEMS_IMG\_K084456"
    for root, dirs, files in  os.walk(path):
        for file in files:
            print(file)
            # if file in change_list :
            file_path = os.path.join(root,file)
            tranform(file_path,root)
            # os.remove(file_path)
# Dicom2avi()
# file = readfile(path)
# save = "E:/pythonProject/dicom_transform/data/disease/LXH007-ZUOXIAO/avi"
# for i in range(len(file)):
#     tranform(file[i])

def locate_slice(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("nii.gz"):
                file_path = os.path.join(root, file)
                data = nib.load(file_path).get_data()
                labeled_slices = []
                for i in range(data.shape[2]):
                    slice = data[:, :, i]
                    if np.max(slice) != 0:
                        labeled_slices.append(i)
                print(
                    f"Current file is {file_path}.The len of the labeled data is {len(labeled_slices)}, and is {labeled_slices}")


# 转移数据 并且检查数据格式是否正确 主要是命名 '二尖瓣短轴','乳头肌短轴','心尖短轴', '心尖两腔','心尖三腔','心尖四腔'
# 将 dicom 数据 转换为 avi格式 并删除原来的格式（ 可有可无 ） ： Dicom2avi
# 打开每个数据进行最后的切割 生成新的标注
# 解压avi的压缩文件  删除所有的压缩文件
# 统计标注位置及个数  ：locate_slice



import os
import cv2
import numpy as np
import nibabel as nib
import SimpleITK as sitk
from PIL import Image
import imageio
# img = nib.load("F:\desktop\数据\\2.nii.gz")          #下载niifile文件（其实是提取文件）
# img_fdata = img.get_fdata()      #获取niifile数据
# # img_fdata = img_fdata.transpose((0,1))
# (x,y,z) = img_fdata.shape            #获得数据shape信息：（长，宽，维度-切片数量）
# print(x,y,z)
# for k in range(z):
#     silce = img_fdata[:,:,k]         #三个位置表示三个不同角度的切片
#     print(type(silce))
#     # slice = slice.reshape(800,600)
#     print(silce.shape)
#     imageio.imwrite(os.path.join("F:\desktop\数据\label_imgs",'{}.png'.format(k)),silce)

def tranform2png(file):
    data = pydcm.read_file(file, force=True)
    if 'NumberOfFrames' in dir(data):
        name = file.split("\\")[-1]
        name += '.avi'
        fps = 30
        frames, width, height, channels = data.pixel_array.shape
        fourcc = cv.VideoWriter_fourcc('M', 'J', 'P',
                                       'G')  # 输出格式'M', 'J', 'P', 'G'或'I', '4', '2', '0'或'P', 'I', 'M', 'I'
        # out = cv.VideoWriter(os.path.join(save, name), fourcc, fps, (height, width), False)  # Attention if the  vedio is gray type.The false must be change into True
        # data = []
        if 'PixelSpacing' in dir(data):
            cur_spacing = float(data.PixelSpacing[0])
        for idx in range(22):
            nii_data_array = data.pixel_array
            frame_img = nii_data_array[idx]
            if (len(frame_img.shape) == 2):  # gray image
                frame_img = cv.cvtColor(frame_img, cv.COLOR_GRAY2BGR)
            elif (len(frame_img.shape) == 3):  # color image
                frame_img = cv.cvtColor(frame_img, cv.COLOR_YUV2BGR)
                # frame_img = cv.cvtColor(frame_img, cv.COLOR_BGR2GRAY)
                print(frame_img.shape)
            # data.append(frame_img)
            imageio.imwrite(os.path.join("F:\desktop\数据\data_imgs", '{}.png'.format(idx)), frame_img)
# tranform2png("F:\desktop\数据\\二尖瓣短轴")


import matplotlib.pyplot as plt
import imageio,os
images = []
filenames=[]
for i in range(9):
    filenames.append(os.path.join("F:\desktop\\1\\flow","vis_flow_"+str(i)+".png"))
# filenames = sorted(filenames)
print(filenames)
# filenames=sorted((fn for fn in os.listdir('F:\desktop\数据\label_imgs') if fn.endswith('.png')))
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('F:\desktop\\1\\flow\\gif.gif', images,duration=1)


# import cv2
# import os
# from PIL import Image
# import matplotlib.image as mpimg
# import numpy as np
# import matplotlib
# for i in range(17):
#     im_path = os.path.join("F:\desktop\\1\data_imgs","img_"+str(i)+".png")
#     ma_path = os.path.join("F:\desktop\\1\label_imgs",str(i)+".png")
#
#     image = cv.imread(im_path)
#     mask = cv.imread(ma_path)
#     mask[np.where(mask == (84,1,68))] = 0
#     img_show = cv.addWeighted(image, 0.5, mask, 0.5, 3)
#     cv.imwrite("./"+str(i)+".png",img_show)
#     # cv.imshow("img_show", img_show)

