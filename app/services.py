from django.conf import settings

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections


class ESService:
    connection = None

    @classmethod
    def get_hosts(cls):
        return [f'{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}']

    @classmethod
    def get_connector(cls):
        return cls.setup_connection()

    @classmethod
    def delete_index(cls, index_name):
        return cls.get_connector().indices.delete(index=index_name, ignore=[400, 404])

    @classmethod
    def setup_connection(cls):
        if not cls.connection:
            cls.connection = connections.create_connection(hosts=cls.get_hosts())
        return cls.connection

    @classmethod
    def search_text_in_index(cls, index, phrase):
        client = cls.setup_connection()
        response = Search(using=client, index=index).query('match', text=phrase).execute()
        return [x['_source'] for x in response.to_dict()['hits']['hits']]
