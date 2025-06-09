from __future__ import print_function
import time
from volcengine.visual.VisualService import VisualService
if __name__ == '__main__':
    visual_service = VisualService()
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    form = {'urls': ['url_1', 'url_2']}
    resp = visual_service.image_search_image_add(form)
    print(resp)