from django.urls import path
from ..views.rag import AddFilesToUSearchAPIView, QuerySearchAPIView, GetUploadedFilesAPIView


urlpatterns = [
    path('add-files-to-usearch', AddFilesToUSearchAPIView.as_view(), name='add-files-to-usearch'),
    path('query_search', QuerySearchAPIView.as_view(), name='query_search'),
    path('get-uploaded-files', GetUploadedFilesAPIView.as_view(), name='query_search')
]