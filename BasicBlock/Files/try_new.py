import matplotlib.pyplot as plt
import pydicom as pydcm
import numpy as np
import cv2 as cv
import os


def readfile(path):
    filename = []
    for root, dir, files in os.walk(path):
        for file in files:
            #if ".dcm" in file.lower():
            filename.append(os.path.join(root, file))
    return filename


def tranform(file):
    data = pydcm.read_file(file, force=True)
    if data.SeriesNumber == 1:
        if 'NumberOfFrames' in dir(data):
            name = file.split("\\")[-1]
            name += '.avi'
            fps = 30
            frames, width, height, channels = data.pixel_array.shape
            fourcc = cv.VideoWriter_fourcc('M', 'J', 'P',
                                           'G')  # 输出格式'M', 'J', 'P', 'G'或'I', '4', '2', '0'或'P', 'I', 'M', 'I'
            out = cv.VideoWriter(os.path.join(save, name), fourcc, fps, (height, width), True)
            print(os.path.join(save, name))
            # data = []
            if 'PixelSpacing' in dir(data):
                cur_spacing = float(data.PixelSpacing[0])
            for idx in range(frames):
                nii_data_array = data.pixel_array
                frame_img = nii_data_array[idx]
                img1 = frame_img[:,:,0]
                img2 = frame_img[:,:,1]
                img3 = frame_img[:,:,2]
                # plt.imshow(img1, cmap='gray')
                # plt.show()
                # plt.imshow(img2, cmap='gray')
                # plt.show()
                # plt.imshow(img3, cmap='gray')
                # plt.show()

                if (len(frame_img.shape) == 2):  # gray image
                    frame_img = cv.cvtColor(frame_img, cv.COLOR_GRAY2BGR)
                elif (len(frame_img.shape) == 3):  # color image
                    frame_img = cv.cvtColor(frame_img, cv.COLOR_YUV2BGR)
                    # frame_img = cv.cvtColor(frame_img, cv.COLOR _HSV2RGB)
                    # frame_img = cv.cvtColor(frame_img, cv.COLOR_)
                # data.append(frame_img)
                out.write(frame_img)

        else:
            # 二维静态图 series number=1, NumberOfFrames 不存在
            data = pydcm.read_file(file, force=True)
            mini_data = data.pixel_array
            name = file.split("\\")[-1]
            name +='.png'
            if (len(mini_data.shape) == 3):  # color image
                mini_data = cv.cvtColor(mini_data, cv.COLOR_YUV2BGR)  # COLOR_BGR2RGB
            data = mini_data.copy()
            cv.imwrite(os.path.join(save, name), data)
            print(os.path.join(save, name))


path = "G:\正常对照组造影动态视频DICOM\GEMS_IMG\_K084456"
file = readfile(path)
save = "G:\正常对照组造影动态视频DICOM\GEMS_IMG\_K084456"
for i in range(len(file)):
    tranform(file[i])






