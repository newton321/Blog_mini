#coding: utf-8
from datetime import datetime
from . import db


class ArticleType(db.Model):
    __tablename__ = 'articleTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    introduction = db.Column(db.String(128))
    articles = db.relationship('Article', backref='articleType', lazy='dynamic')

    @staticmethod
    def insert_articleTypes():
        article_types = {'Python': u'记录Python的点点滴滴',
                 'Linux': u'我的Linux成长之路',
                 u'开源技术': u'感兴趣的开源技术，当然也有我自己的开源软件',
                 u'网络技术': u'大而全的网络技术，没有具体的方向',
                 u'思科网络技术': u'主要是思科的路由交换技术',
                 'CCIE': u'因为曾经CCIE这个名词对我有特殊的意义，所以特留一个板块',
                 u'学校那些事': u'小学 初中 高中 大学，总有一些刻骨铭心的事',
                 u'感情那些事': u'各种情感的交织',
                 u'不一样的自己': u'奋斗中的自己'}
        for t in article_types:
            article_type = ArticleType.query.filter_by(name=t).first()
            if article_type is None:
                article_type = ArticleType(name=t, introduction=article_types[t])
            db.session.add(article_type)
        db.session.commit()

    def __repr__(self):
        return '<Type %r>' % self.name


class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    articles = db.relationship('Article', backref='source', lazy='dynamic')

    @staticmethod
    def insert_sources():
        sources = (u'原创',
                   u'转载',
                   u'翻译')
        for s in sources:
            source = Source.query.filter_by(name=s).first()
            if source is None:
                source = Source(name=s)
            db.session.add(source)
        db.session.commit()

    def __repr__(self):
        return '<Source %r>' % self.name


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        article_count = Article.query.count()
        for i in range(count):
            a = Article.query.offset(randint(0, article_count - 1)).first()
            c = Comment(content=forgery_py.lorem_ipsum.sentences(randint(3, 5)),
                        timestamp=forgery_py.date.date(True),
                        author_name=forgery_py.internet.user_name(True),
                        author_email=forgery_py.internet.email_address(),
                        article=a)
            db.session.add(c)
            db.session.commit()


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    num_of_view = db.Column(db.Integer, default=0)
    articleType_id = db.Column(db.Integer, db.ForeignKey('articleTypes.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        articleType_count = ArticleType.query.count()
        source_count = Source.query.count()
        for i in range(count):
            aT = ArticleType.query.offset(randint(0, articleType_count - 1)).first()
            s = Source.query.offset(randint(0, source_count - 1)).first()
            a = Article(title=forgery_py.lorem_ipsum.title(randint(3, 5)),
                        content=forgery_py.lorem_ipsum.sentences(randint(15, 35)),
                        summary=forgery_py.lorem_ipsum.sentences(randint(2, 5)),
                        num_of_view=randint(100, 15000),
                        articleType=aT,source=s)
            db.session.add(a)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Article %r>' % self.title
