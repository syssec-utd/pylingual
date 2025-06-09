"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云-权限中心Python SDK(iam-python-sdk) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from iam.collection import FancyDict

def get_filter_obj(filter_data, filter_keys):
    filter_obj = FancyDict()
    _filter_data = filter_data or {}
    for key in filter_keys:
        filter_obj[key] = _filter_data.get(key)
    return filter_obj

class Page(object):

    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset

    @property
    def slice_from(self):
        return self.offset

    @property
    def slice_to(self):
        if self.limit == 0:
            return None
        return self.offset + self.limit

def get_page_obj(page_data):
    return Page(limit=page_data.get('limit', 0), offset=page_data.get('offset', 0))