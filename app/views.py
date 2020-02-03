from django.contrib.postgres.search import TrigramSimilarity

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from app.decorators import request_stats
from app.models import Article
from app.serializers import ArticleSerializer
from app.services import ESService


class SearchBaseView(APIView):
    def get_query_param(self):
        if (phrase := self.request.query_params.get('q')) is None:
            raise ValidationError({'query_params': ['Please provide query parameter q']})
        return phrase

    def get_data(self):
        raise NotImplementedError('Implement get_data in View that inherits SearchBaseView')

    @request_stats  # custom decorator to show request time, db connections count and (optionally) sql queries
    def get(self, request, format=None):
        serializer = ArticleSerializer(data=self.get_data(), many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class PSQLSearchView(SearchBaseView):
    def get_data(self):
        return list(Article.objects.annotate(
            similarity=TrigramSimilarity('text', self.get_query_param())
        ).order_by('-similarity').values('title', 'text')[:20])


class ESSearchView(SearchBaseView):
    def get_data(self):
        return ESService.search_text_in_index('articles', self.get_query_param())
