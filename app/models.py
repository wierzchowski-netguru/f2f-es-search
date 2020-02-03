from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from elasticsearch.exceptions import NotFoundError

from app.documents import ArticleDocument
from app.services import ESService


class ESMixin:

    class ESMeta:
        document = None

    def es_data(self):
        """
        Return dict with all data that has to be put in Elasticsearch
        (data needs to be compliant with corresponding Document.
        """
        raise NotImplementedError('Override this method in Model class')

    def es_put(self):
        """
        Method responsible for create / update
        """
        ESService.get_connector()
        result = self.document_class(**self.es_data()).save()
        if result not in ['created', 'updated']:
            print(f'[ELASTICSEARCH] Failed saving Article id = {self.id}, result = {result}')
        print(f'[ELASTICSEARCH] Success saving Article id = {self.id}')
        return result

    def es_delete(self):
        """
        Method responsible for delete
        """
        try:
            ESService.get_connector().delete(index=settings.ES_INDEX_NAME, id=self.id_es)
            print(f'[ELASTICSEARCH] Success deleting Article id = {self.id}')
        except NotFoundError as e:
            # fail silently but print error details
            print(f'[ELASTICSEARCH] Failed deleting Article id = {self.id}\n{e}')

    @property
    def document_class(self):
        """
        Getter for document class created for Model
        """
        if not getattr(self, 'ESMeta', None) or not getattr(self.ESMeta, 'document', None):
            raise NotImplementedError('Please set \'document\' inside ESMeta')
        return self.ESMeta.document

    @property
    def id_es(self):
        return f'{self.__class__.__name__.lower()}.{self.id}'


class User(ESMixin, AbstractUser):

    def es_data(self):
        pass


class Article(ESMixin, models.Model):
    user = models.ForeignKey('app.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')

    title = models.CharField(max_length=255)
    text = models.TextField()

    class ESMeta:
        document = ArticleDocument

    def es_data(self):
        return dict(
            meta={'id': self.id_es},
            title=self.title,
            text=self.text
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.es_put()

    def delete(self, *args, **kwargs):
        self.es_delete()
        return super().delete(*args, **kwargs)
