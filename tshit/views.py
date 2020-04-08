import os

import cv2
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from tshit.clustering import kmeans_clustering


def index(request):
    return render(request, 'tshit/index_3.html')


def ajax_view(request):
    IMG_FOLDER = "tshit/static/tshit/img/"
    CROPPED_IMG = IMG_FOLDER + "img.png"
    RESULT_IMG = IMG_FOLDER + "result.png"

    img = request.FILES['img']
    content = ContentFile(img.read())
    if os.path.exists(RESULT_IMG):
        os.remove(RESULT_IMG)
    if os.path.exists(CROPPED_IMG):
        os.remove(CROPPED_IMG)
    path = default_storage.save(CROPPED_IMG, content)
    cv2_img = cv2.imread(CROPPED_IMG)
    cv2_img = kmeans_clustering(cv2_img)
    cv2.imwrite(RESULT_IMG, cv2_img)
    response = {
        'msg': 'Success'
    }
    return JsonResponse(response)
