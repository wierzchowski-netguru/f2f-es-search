from django.conf import settings

from elasticsearch_dsl import Boolean, Document, MetaField, Text


class UserDocument(Document):
    username = Text()
    first_name = Text()
    last_name = Text()
    is_staff = Boolean()

    class Index:
        name = settings.ES_INDEX_NAME

    class Meta:
        index = 'user'
        doc_type = 'user'


class ArticleDocument(Document):
    title = Text()
    text = Text()

    class Index:
        name = settings.ES_INDEX_NAME

    class Meta:
        index = 'article'
        doc_type = 'article'
        user = MetaField(type='user')
