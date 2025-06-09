import base64
import csv
import os
import time
from io import BytesIO
from zipfile import ZipFile
import pandas as pd
import requests
from PIL import Image
from tqdm import tqdm
from utils import DATA_DIR

def img2base64(img):
    buffered = BytesIO()
    img.save(buffered, format='JPEG')
    return base64.b64encode(buffered.getvalue())

def facepp_compare(face1, face2, mode='image_base64'):
    payload = {'api_key': 'pqLY9sQp07cBuyXXgr3ntl47WY-p8a-F', 'api_secret': 'qljRujMaShVUmz1tqByEyjmdrsGMwhxT', f'{mode}_1': face1, f'{mode}_2': face2}
    res = requests.post('https://api-us.faceplusplus.com/facepp/v3/compare', data=payload)
    data = res.json()
    if 'error_message' in data and data['error_message'] == 'CONCURRENCY_LIMIT_EXCEEDED':
        time.sleep(3)
        return facepp_compare(face1, face2)
    return data
if __name__ == '__main__':
    fp_sample = f'{DATA_DIR}/yizhibo_faces_snippet_sampled3.csv'
    fp_center = f'{DATA_DIR}/yizhibo_faces_snippet_center3.csv'
    fp_src = f'{DATA_DIR}/yizhibo_faces_snippet.csv'
    fp_dst = 'D:\\yizhibo_facepp_compare.csv'
    if os.path.exists(fp_sample):
        df_sampled = pd.read_csv(fp_sample)
    else:
        df_uids = pd.read_csv(f'{DATA_DIR}/uids.csv')
        df_videos = pd.read_csv('../analysis/yizhibo_video_clothes.csv').dropna(subset=['sell'])
        df = pd.read_csv(fp_src)
        df = df[df['Yizhibo_VID'].isin(df_videos['Yizhibo_VID'])]
        df = df[df['probs'] > 0.99]
        df_sampled = df.groupby(['Yizhibo_UID', 'Yizhibo_VID']).sample(3, replace=True, random_state=99).drop_duplicates().reset_index(drop=True)
        df_sampled = df_uids.merge(df_sampled, how='right')
        df_sampled.to_csv(fp_sample, index=False)
    if os.path.exists(fp_center):
        df_center = pd.read_csv(fp_center)
    else:
        df_center = df_sampled.groupby(['Yizhibo_UID', 'Yizhibo_VID']).sample(3, replace=True, random_state=99).drop_duplicates().reset_index(drop=True)
        df_center.to_csv(fp_center, index=False)
    read = set()
    if not (writer_header := (not os.path.exists(fp_dst))):
        df_done = pd.read_csv(fp_dst)
        read = set(df_done.apply(lambda x: (f"D:/img/{x['Yizhibo_UID'][2:]}/{x['Yizhibo_VID_c'][2:]}/{x['snippet_c']:05d}.zip", f"D:/img/{x['Yizhibo_UID'][2:]}/{x['Yizhibo_VID_p'][2:]}/{x['snippet_p']:05d}.zip"), axis=1))
    p1p2 = []
    for uid in set(df_center['Yizhibo_UID']):
        this_center = df_center[df_center['Yizhibo_UID'] == uid]
        this_point = df_sampled[df_sampled['Yizhibo_UID'] == uid]
        for (_, row1) in this_center.iterrows():
            for (_, row2) in this_point.iterrows():
                path1 = f"D:/img/{row1['Yizhibo_UID'][2:]}/{row1['Yizhibo_VID'][2:]}/{row1['snippet']:05d}.zip"
                path2 = f"D:/img/{row2['Yizhibo_UID'][2:]}/{row2['Yizhibo_VID'][2:]}/{row2['snippet']:05d}.zip"
                if path1 == path2:
                    continue
                p1p2.append((path1, path2))
    with open(fp_dst, 'a', encoding='utf-8') as o, tqdm(total=len(p1p2)) as bar:
        csvwriter = csv.writer(o, lineterminator='\n')
        if writer_header:
            csvwriter.writerow(['Yizhibo_UID', 'Yizhibo_VID_c', 'snippet_c', 'frame_c', 'Yizhibo_VID_p', 'snippet_p', 'frame_p', 'confidence', 'threshold-3', 'threshold-4', 'threshold-5', 'face_tokens_c', 'face_tokens_p', 'image_id_c', 'image_id_p', 'request_id'])
        for uid in set(df_center['Yizhibo_UID']):
            this_center = df_center[df_center['Yizhibo_UID'] == uid]
            this_point = df_sampled[df_sampled['Yizhibo_UID'] == uid]
            for (_, row1) in this_center.iterrows():
                for (_, row2) in this_point.iterrows():
                    path1 = f"D:/img/{row1['Yizhibo_UID'][2:]}/{row1['Yizhibo_VID'][2:]}/{row1['snippet']:05d}.zip"
                    path2 = f"D:/img/{row2['Yizhibo_UID'][2:]}/{row2['Yizhibo_VID'][2:]}/{row2['snippet']:05d}.zip"
                    bar.set_description(f"{uid[2:]} {row1['Yizhibo_VID'][2:]},{row2['Yizhibo_VID'][2:]}")
                    bar.update(1)
                    if path1 == path2 or (path1, path2) in read:
                        continue
                    with ZipFile(path1) as myzip1, myzip1.open(f"{row1['frame']:05d}.jpg") as myfile1, ZipFile(path2) as myzip2, myzip2.open(f"{row2['frame']:05d}.jpg") as myfile2:
                        img1 = Image.open(myfile1)
                        img2 = Image.open(myfile2)
                        data = facepp_compare(img2base64(img1), img2base64(img2))
                        if 'confidence' not in data:
                            continue
                        csvwriter.writerow([uid, row1['Yizhibo_VID'], row1['snippet'], row1['frame'], row2['Yizhibo_VID'], row2['snippet'], row2['frame'], data['confidence'], data['thresholds']['1e-3'], data['thresholds']['1e-4'], data['thresholds']['1e-5'], '|'.join((face['face_token'] for face in data['faces1'])), '|'.join((face['face_token'] for face in data['faces2'])), data['image_id1'], data['image_id2'], data['request_id']])