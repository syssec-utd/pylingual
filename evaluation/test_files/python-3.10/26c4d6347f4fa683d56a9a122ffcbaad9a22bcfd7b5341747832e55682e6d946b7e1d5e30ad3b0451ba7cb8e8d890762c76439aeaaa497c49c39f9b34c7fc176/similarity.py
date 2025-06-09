import json
import io
from enum import Enum
from copy import deepcopy
from .. import entities, exceptions

class CollectionTypes(str, Enum):
    SIMILARITY = 'collection'
    MULTIVIEW = 'multi'

class SimilarityTypeEnum(str, Enum):
    """
    State enum
    """
    ID = 'id'
    URL = 'url'

class CollectionItem:
    """
    Base CollectionItem
    """

    def __init__(self, type: SimilarityTypeEnum, ref):
        assert isinstance(ref, str)
        self.ref = ref
        self.type = type

    @classmethod
    def from_json(cls, _json):
        return cls(type=_json['type'], ref=_json['ref'])

    def to_json(self):
        _json = {'type': self.type, 'ref': self.ref}
        return _json

class SimilarityItem(CollectionItem):
    """
    Single similarity item
    """

    def __init__(self, type, ref, target=False):
        super().__init__(type=type, ref=ref)
        assert isinstance(ref, str)
        self.target = target

    def to_json(self):
        _json = super().to_json()
        if self.target:
            _json['target'] = self.target
        return _json

class MultiViewItem(CollectionItem):
    """
    Single multi view item
    """

    def __init__(self, type, ref):
        super().__init__(type=type, ref=ref)

class Collection:
    """
    Base Collection Entity
    """

    def __init__(self, type: CollectionTypes, name, items=None):
        self.type = type
        self.name = name
        self._items = self._items_to_list(items=items)

    @staticmethod
    def _items_to_list(items):
        items_list = list()
        if items:
            if not isinstance(items, list):
                items = [items]
            for item in items:
                if isinstance(item, entities.Item):
                    items_list.append({'type': SimilarityTypeEnum.ID, 'ref': item.id})
                elif isinstance(item, SimilarityItem) or isinstance(item, MultiViewItem):
                    items_list.append(item.to_json())
                elif isinstance(item, dict):
                    items_list.append(item)
                else:
                    raise exceptions.PlatformException('400', 'items must be a list of the following: Item, MultiViewItem, SimilarityItem, dict')
        return items_list

    def to_json(self):
        """
        Returns platform _json format of object

        :return: platform json format of object
        :rtype: dict
        """
        _json = {'type': self.type, 'shebang': 'dataloop', 'metadata': {'dltype': self.type}}
        return _json

    def to_bytes_io(self):
        byte_io = io.BytesIO()
        byte_io.name = self.name
        byte_io.write(json.dumps(self.to_json()).encode())
        byte_io.seek(0)
        return byte_io

    def add(self, ref, type: SimilarityTypeEnum=SimilarityTypeEnum.ID):
        """
        Add item to collection
        :param ref:
        :param type: url, id
        """
        item = {'ref': ref, 'type': type}
        self._items.append(item)

    def pop(self, ref):
        """
        :param ref:
        """
        for item in self._items:
            if item['ref'] == ref:
                self._items.remove(item)

class Similarity(Collection):
    """
    Similarity Entity
    """

    def __init__(self, ref, name=None, items=None):
        if name is None:
            name = ref
        super().__init__(type=CollectionTypes.SIMILARITY, name=name, items=items)
        assert isinstance(ref, str)
        self.ref = ref

    @property
    def items(self):
        """
        list of the collection items
        """
        return [SimilarityItem.from_json(_json=item) for item in self._items]

    @property
    def target(self):
        """
        Target item for similarity
        """
        if self.ref.isalnum():
            return SimilarityItem(ref=self.ref, type=SimilarityTypeEnum.ID, target=True)
        else:
            return SimilarityItem(ref=self.ref, type=SimilarityTypeEnum.URL, target=True)

    @classmethod
    def from_json(cls, _json):
        return cls(ref=_json['metadata']['target']['ref'], items=_json.get('items', list()))

    def _fixed_items(self):
        items = deepcopy(self._items)
        target_in_items = False
        for item in items:
            if item.get('ref', '') == self.ref:
                target_in_items = True
                item['target'] = True
            else:
                item.pop('target', None)
        if not target_in_items:
            items.append(self.target.to_json())
        return items

    def to_json(self):
        """
        Returns platform _json format of object

        :return: platform json format of object
        :rtype: dict
        """
        _json = super().to_json()
        _json['metadata']['target'] = {'type': self.target.type, 'ref': self.target.ref}
        _json['items'] = self._fixed_items()
        return _json

class MultiView(Collection):
    """
    Multi Entity
    """

    def __init__(self, name, items=None):
        super().__init__(type=CollectionTypes.MULTIVIEW, name=name, items=items)

    @property
    def items(self):
        """
        list of the collection items
        """
        return [MultiViewItem.from_json(_json=item) for item in self._items]

    @classmethod
    def from_json(cls, _json):
        return cls(items=_json.get('items', list()), name=None)

    def to_json(self):
        """
        Returns platform _json format of object

        :return: platform json format of object
        :rtype: dict
        """
        _json = super().to_json()
        _json['items'] = self._items
        return _json