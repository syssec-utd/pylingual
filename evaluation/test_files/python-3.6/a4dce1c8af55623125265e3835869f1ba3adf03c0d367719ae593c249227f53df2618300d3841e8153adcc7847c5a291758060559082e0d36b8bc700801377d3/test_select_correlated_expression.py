import pytest
import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils.compat import _select_args, get_scalar_subquery
from sqlalchemy_utils.relationships import select_correlated_expression

@pytest.fixture
def group_user_tbl(Base):
    return sa.Table('group_user', Base.metadata, sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')), sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id')))

@pytest.fixture
def group_tbl(Base):

    class Group(Base):
        __tablename__ = 'group'
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String)
    return Group

@pytest.fixture
def friendship_tbl(Base):
    return sa.Table('friendships', Base.metadata, sa.Column('friend_a_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True), sa.Column('friend_b_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True))

@pytest.fixture
def User(Base, group_user_tbl, friendship_tbl):

    class User(Base):
        __tablename__ = 'user'
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String)
        groups = sa.orm.relationship('Group', secondary=group_user_tbl, backref='users')
        friends = sa.orm.relationship('User', secondary=friendship_tbl, primaryjoin=id == friendship_tbl.c.friend_a_id, secondaryjoin=id == friendship_tbl.c.friend_b_id)
    friendship_union = sa.select(*_select_args(friendship_tbl.c.friend_a_id, friendship_tbl.c.friend_b_id)).union(sa.select(*_select_args(friendship_tbl.c.friend_b_id, friendship_tbl.c.friend_a_id))).alias()
    User.all_friends = sa.orm.relationship('User', secondary=friendship_union, primaryjoin=User.id == friendship_union.c.friend_a_id, secondaryjoin=User.id == friendship_union.c.friend_b_id, viewonly=True, order_by=User.id)
    return User

@pytest.fixture
def Category(Base, group_user_tbl, friendship_tbl):

    class Category(Base):
        __tablename__ = 'category'
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String)
        created_at = sa.Column(sa.DateTime)
        parent_id = sa.Column(sa.Integer, sa.ForeignKey('category.id'))
        parent = sa.orm.relationship('Category', backref='subcategories', remote_side=[id], order_by=id)
    return Category

@pytest.fixture
def Article(Base, Category, User):

    class Article(Base):
        __tablename__ = 'article'
        id = sa.Column('_id', sa.Integer, primary_key=True)
        name = sa.Column(sa.String)
        name_synonym = sa.orm.synonym('name')

        @hybrid_property
        def name_upper(self):
            return self.name.upper() if self.name else None

        @name_upper.expression
        def name_upper(cls):
            return sa.func.upper(cls.name)
        content = sa.Column(sa.String)
        category_id = sa.Column(sa.Integer, sa.ForeignKey(Category.id))
        category = sa.orm.relationship(Category, backref='articles')
        author_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
        author = sa.orm.relationship(User, primaryjoin=author_id == User.id, backref='authored_articles')
        owner_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
        owner = sa.orm.relationship(User, primaryjoin=owner_id == User.id, backref='owned_articles')
    return Article

@pytest.fixture
def Comment(Base, Article, User):

    class Comment(Base):
        __tablename__ = 'comment'
        id = sa.Column(sa.Integer, primary_key=True)
        content = sa.Column(sa.String)
        article_id = sa.Column(sa.Integer, sa.ForeignKey(Article.id))
        article = sa.orm.relationship(Article, backref='comments')
        author_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
        author = sa.orm.relationship(User, backref='comments')
    Article.comment_count = sa.orm.column_property(get_scalar_subquery(sa.select(*_select_args(sa.func.count(Comment.id))).where(Comment.article_id == Article.id).correlate_except(Article)))
    return Comment

@pytest.fixture
def model_mapping(Article, Category, Comment, group_tbl, User):
    return {'articles': Article, 'categories': Category, 'comments': Comment, 'groups': group_tbl, 'users': User}

@pytest.fixture
def init_models(Article, Category, Comment, group_tbl, User):
    pass

@pytest.fixture
def dataset(session, User, group_tbl, Article, Category, Comment):
    group = group_tbl(name='Group 1')
    group2 = group_tbl(name='Group 2')
    user = User(id=1, name='User 1', groups=[group, group2])
    user2 = User(id=2, name='User 2')
    user3 = User(id=3, name='User 3', groups=[group])
    user4 = User(id=4, name='User 4', groups=[group2])
    user5 = User(id=5, name='User 5')
    user.friends = [user2]
    user2.friends = [user3, user4]
    user3.friends = [user5]
    article = Article(name='Some article', author=user, owner=user2, category=Category(id=1, name='Some category', subcategories=[Category(id=2, name='Subcategory 1', subcategories=[Category(id=3, name='Subsubcategory 1', subcategories=[Category(id=5, name='Subsubsubcategory 1'), Category(id=6, name='Subsubsubcategory 2')])]), Category(id=4, name='Subcategory 2')]), comments=[Comment(content='Some comment', author=user)])
    session.add(user3)
    session.add(user4)
    session.add(article)
    session.commit()

@pytest.mark.usefixtures('dataset', 'postgresql_dsn')
class TestSelectCorrelatedExpression:

    @pytest.mark.parametrize(('model_key', 'related_model_key', 'path', 'result'), (('categories', 'categories', 'subcategories', [(1, 2), (2, 1), (3, 2), (4, 0), (5, 0), (6, 0)]), ('articles', 'comments', 'comments', [(1, 1)]), ('users', 'groups', 'groups', [(1, 2), (2, 0), (3, 1), (4, 1), (5, 0)]), ('users', 'users', 'all_friends', [(1, 1), (2, 3), (3, 2), (4, 1), (5, 1)]), ('users', 'users', 'all_friends.all_friends', [(1, 3), (2, 2), (3, 3), (4, 3), (5, 2)]), ('users', 'users', 'groups.users', [(1, 3), (2, 0), (3, 2), (4, 2), (5, 0)]), ('groups', 'articles', 'users.authored_articles', [(1, 1), (2, 1)]), ('categories', 'categories', 'subcategories.subcategories', [(1, 1), (2, 2), (3, 0), (4, 0), (5, 0), (6, 0)]), ('categories', 'categories', 'subcategories.subcategories.subcategories', [(1, 2), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)])))
    def test_returns_correct_results(self, session, model_mapping, model_key, related_model_key, path, result):
        model = model_mapping[model_key]
        alias = sa.orm.aliased(model_mapping[related_model_key])
        aggregate = select_correlated_expression(model, sa.func.count(sa.distinct(alias.id)), path, alias)
        query = session.query(model.id, aggregate.label('count')).order_by(model.id)
        assert query.all() == result

    def test_order_by_intermediate_table_column(self, session, model_mapping, group_user_tbl):
        model = model_mapping['users']
        alias = sa.orm.aliased(model_mapping['groups'])
        aggregate = select_correlated_expression(model, sa.func.json_build_object('id', alias.id), 'groups', alias, order_by=[group_user_tbl.c.user_id])
        assert session.execute(aggregate)

    def test_with_non_aggregate_function(self, session, User, Article):
        aggregate = select_correlated_expression(Article, sa.func.json_build_object('name', User.name), 'comments.author', User)
        query = session.query(Article.id, aggregate.label('author_json')).order_by(Article.id)
        result = query.all()
        assert result == [(1, {'name': 'User 1'})]