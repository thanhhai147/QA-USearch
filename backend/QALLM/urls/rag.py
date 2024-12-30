from django.urls import path
from ..views.rag import AddFilesToUSearchAPIView, QuerySearchAPIView, GetUploadedFilesAPIView, GetSourceByChatIdAPIView


urlpatterns = [
    path('add-files-to-usearch', AddFilesToUSearchAPIView.as_view(), name='add-files-to-usearch'),
    path('query-search', QuerySearchAPIView.as_view(), name='query-search'),
    path('get-uploaded-files', GetUploadedFilesAPIView.as_view(), name='get-uploaded-files'),
    path('get-source', GetUploadedFilesAPIView.as_view(), name='get-source'),
]