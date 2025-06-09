import numpy as np
import torch
import os

def save_bbox_heatmap(bboxes, heatmap, save_base=os.getcwd() + '/heatmap_result', save_name='', kth_input=None):
    color = [1, 1, 1]
    save_base = os.path.join(save_base, save_name)
    print(save_base, flush=True)
    if not os.path.exists(save_base):
        os.makedirs(save_base)
    if kth_input is not None:
        for idx in range(heatmap.shape[0]):
            kth = kth_input
            kth = int(kth)
            obj_name = str(idx) + '_' + str(int(kth)) + '.obj'
            real_save_path = os.path.join(save_base, obj_name)
            file_out = open(real_save_path, 'w')
            norm = heatmap[idx][kth].max()
            for _, point in enumerate(bboxes):
                p = (heatmap[idx][kth][_].cpu() * 5).numpy()
                p = min(1, p)
                point = point[[0, 4, 1, 5, 3, 7, 2, 6], :]
                for i in range(8):
                    print('v %f %f %f %f %f %f' % (point[i][0], point[i][1], point[i][2], color[0] * (1 - p) + p, color[1] * (1 - p), color[2] * (1 - p)), file=file_out)
                bs = 8 * _
                print('f %d %d %d %d' % (1 + bs, 2 + bs, 4 + bs, 3 + bs), file=file_out)
                print('f %d %d %d %d' % (5 + bs, 6 + bs, 8 + bs, 7 + bs), file=file_out)
                print('f %d %d %d %d' % (1 + bs, 2 + bs, 6 + bs, 5 + bs), file=file_out)
                print('f %d %d %d %d' % (3 + bs, 4 + bs, 8 + bs, 7 + bs), file=file_out)
                print('f %d %d %d %d' % (1 + bs, 3 + bs, 7 + bs, 5 + bs), file=file_out)
                print('f %d %d %d %d' % (2 + bs, 4 + bs, 8 + bs, 6 + bs), file=file_out)
                print('l %d %d' % (1 + bs, 2 + bs), file=file_out)
                print('l %d %d' % (2 + bs, 4 + bs), file=file_out)
                print('l %d %d' % (4 + bs, 3 + bs), file=file_out)
                print('l %d %d' % (3 + bs, 1 + bs), file=file_out)
                print('l %d %d' % (5 + bs, 6 + bs), file=file_out)
                print('l %d %d' % (6 + bs, 8 + bs), file=file_out)
                print('l %d %d' % (8 + bs, 7 + bs), file=file_out)
                print('l %d %d' % (7 + bs, 5 + bs), file=file_out)
                print('l %d %d' % (2 + bs, 6 + bs), file=file_out)
                print('l %d %d' % (5 + bs, 1 + bs), file=file_out)
                print('l %d %d' % (4 + bs, 8 + bs), file=file_out)
                print('l %d %d' % (7 + bs, 3 + bs), file=file_out)
            file_out.close()
    else:
        raise NotImplementedError()