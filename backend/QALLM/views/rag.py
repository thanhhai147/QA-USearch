from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils import timezone
from rest_framework import status
from ..models.session import Session
from ..models.chat import Chat
from ..AI.QALLM import add_files_to_usearch_from_memory, query_search, get_sources
import base64

class AddFilesToUSearchAPIView(GenericAPIView):
    def post(self, request):
        data = request.data
        try:
            files = data['files']

            # Decode nội dung PDF từ base64 và lấy tên file
            files_data = [
                {
                    "content": base64.b64decode(file['content'].split(",")[1]),
                    "name": file['name'],
                }
                for file in files
            ]

            # Gọi hàm xử lý file từ nội dung trong bộ nhớ
            add_files_to_usearch_from_memory(files_data)

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"Lỗi xử lý file: {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": "Tạo thành công và thêm dữ liệu vào USearch",
            },
            status=status.HTTP_200_OK
        )

class QuerySearchAPIView(GenericAPIView):
    def post(self, request):
        data = request.data
        try:
            query = data['query']
            response_text, formatted_response = query_search(query)
            data = {
                "response_text" : response_text,
                "formatted_response" : formatted_response
            }
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"Lỗi xử lý file: {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "data": data,
                "message": "Search thành công",
            },
            status=status.HTTP_200_OK
        )


class GetUploadedFilesAPIView(GenericAPIView):
    def get(self, request):
        try:
            data = get_sources()
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"Lỗi lấy sources: {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "data": data,
                "message": "Lấy sources thành công",
            },
            status=status.HTTP_200_OK
        )

