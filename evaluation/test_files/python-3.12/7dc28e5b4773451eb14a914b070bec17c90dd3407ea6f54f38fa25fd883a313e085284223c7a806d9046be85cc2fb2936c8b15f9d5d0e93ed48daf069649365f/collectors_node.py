import uuid
from datetime import datetime
from marshmallow import post_load
from sqlalchemy import or_, func, orm
from core.managers.db_manager import db
from core.managers.log_manager import logger
from shared.schema.collectors_node import CollectorsNodeSchema, CollectorsNodePresentationSchema

class NewCollectorsNodeSchema(CollectorsNodeSchema):

    @post_load
    def make_collectors_node(self, data, **kwargs):
        return CollectorsNode(id=data['id'], name=data['name'], description=data['description'], api_url=data['api_url'], api_key=data['api_key'])

class CollectorsNode(db.Model):
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())
    api_url = db.Column(db.String(), nullable=False)
    api_key = db.Column(db.String(), nullable=False)

    def __init__(self, id, name, description, api_url, api_key):
        self.id = id if id != '' else str(uuid.uuid4())
        self.name = name
        self.description = description
        self.api_url = api_url
        self.api_key = api_key
        self.tag = 'mdi-animation-outline'
        self.type = 'collector'

    @orm.reconstructor
    def reconstruct(self):
        self.tag = 'mdi-animation-outline'
        self.type = 'collector'

    @classmethod
    def exists_by_api_key(cls, api_key):
        return db.session.query(db.exists().where(CollectorsNode.api_key == api_key)).scalar()

    @classmethod
    def get_by_api_key(cls, api_key):
        return cls.query.filter_by(api_key=api_key).first()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(CollectorsNode.name)).all()

    @classmethod
    def get(cls, search):
        query = cls.query
        if search is not None:
            search_string = f'%{search.lower()}%'
            query = query.filter(or_(func.lower(CollectorsNode.name).like(search_string), func.lower(CollectorsNode.description).like(search_string)))
        return (query.order_by(db.asc(CollectorsNode.name)).all(), query.count())

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_first(cls):
        return cls.query.first()

    @classmethod
    def get_json_by_id(cls, id):
        return CollectorsNodeSchema().dump(cls.get_by_id(id))

    @classmethod
    def get_all_json(cls, search):
        nodes, count = cls.get(search)
        node_schema = CollectorsNodePresentationSchema(many=True)
        items = node_schema.dump(nodes)
        return {'total_count': count, 'items': items}

    @classmethod
    def add_new(cls, node_data):
        new_node_schema = NewCollectorsNodeSchema()
        node = new_node_schema.load(node_data)
        db.session.add(node)
        db.session.commit()
        return node

    @classmethod
    def update(cls, node_id, node_data):
        new_node_schema = NewCollectorsNodeSchema()
        updated_node = new_node_schema.load(node_data)
        node = cls.query.get(node_id)
        node = updated_node
        db.session.commit()
        return node

    @classmethod
    def delete(cls, node_id):
        node = cls.query.get(node_id)
        db.session.delete(node)
        db.session.commit()