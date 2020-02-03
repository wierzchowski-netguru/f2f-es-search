from django.urls import path

from app.views import ESSearchView, PSQLSearchView

urlpatterns = [
    path('psql/', PSQLSearchView.as_view(), name='search-view-psql'),
    path('es/', ESSearchView.as_view(), name='search-view-es'),
]
