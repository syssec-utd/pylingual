import matplotlib.pyplot as plt
from PIL import Image
from collections import OrderedDict
import os
import numpy
import cv2
mask_root_path = '/home/xjm/xjm/xjm_pycharm/PENet/results/PFNet/'
orige_img_path = '/home/xjm/xjm/xjm_pycharm/PENet/data/heart_old/test/'
sub_dir = ['HEART']
for dir in sub_dir:
    img_root_path = os.path.join(orige_img_path, 'Imgs')
    mask_ori_path = os.path.join(orige_img_path, 'mask')
    for img in os.listdir(img_root_path):
        img_path = os.path.join(img_root_path, img)
        mask_dir = img.split('.')[0] + '.png'
        result_name = img.split('.')[0] + '_result.png'
        mask_pre_path = os.path.join(mask_root_path, dir, img)
        mask_ori_pic_path = os.path.join(mask_ori_path, img.replace('_img.png', '.png'))
        or_img = Image.open(img_path)
        print(or_img.size)
        or_img_data = numpy.asarray(or_img)
        or_img = Image.open(img_path).convert('RGB')
        mask_pre = Image.open(mask_pre_path).convert('RGB')
        mask_ori = Image.open(mask_ori_pic_path).convert('RGB')
        '\n        plt.subplots的使用，用完以后要记得plt.close\n        另外plt.subplots(1,3, figsize = (7, 7))中的figsize中的数字回自动乘以100，所以一般取个位数即可\n        plt.savefig可以保存整个fig\n        '
        fig, axes = plt.subplots(2, 2, figsize=(7, 7))
        axes[0, 0].set_title('original')
        axes[0, 0].imshow(or_img)
        axes[0, 1].set_title('original mask')
        axes[0, 1].imshow(mask_ori)
        axes[1, 0].set_title('prediction')
        axes[1, 0].imshow(mask_pre)
        img_cv2 = numpy.asarray(or_img)
        img_cv2 = img_cv2 / 255
        mask_cv2 = numpy.asarray(mask_pre)
        '\n        热力图必须先将原图片，和伪彩图片归一化，再相加，最后再归一化\n        并且要注意，伪彩图本来是BGR模式的\n        '
        heatmap = cv2.applyColorMap(mask_cv2, cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        heatmap = heatmap / 255
        final_img = heatmap + img_cv2
        final_img = final_img / numpy.max(final_img)
        axes[1, 1].set_title('result')
        axes[1, 1].imshow(final_img)
        plt.show()
        plt.savefig('/home/xjm/xjm/xjm_pycharm/PENet/eval_show/heart200/' + result_name, bbox_inches='tight')
        plt.close(fig)