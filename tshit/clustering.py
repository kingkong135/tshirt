import cv2
import numpy as np


def kmeans_clustering(img, K=3, attempts=10, display=False):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    vector = img.reshape((-1, 3))
    vector = np.float32(vector)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    ret, label, center = cv2.kmeans(vector, K, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    out_img = res.reshape((img.shape))

    areas = {}
    for i in range(K):
        total_pixel = np.count_nonzero(out_img == center[i])
        areas.update({i: total_pixel})

    areas = {k: v for k, v in sorted(areas.items(), key=lambda item: item[1], reverse=True)}

    index, index1 = list(areas)[:2]

    mask = np.where((out_img == center[index]), 0, 1).astype('uint8')
    mask1 = np.where((out_img == center[index]), 0, 255).astype('uint8')
    mask1 = mask1[:, :, 0]
    result_img = img * mask
    result_img = cv2.cvtColor(result_img, cv2.COLOR_HSV2BGR)

    b_channel, g_channel, r_channel = cv2.split(result_img)
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, mask1))
    img_BGRA = img_BGRA.astype('uint8')
    return img_BGRA
