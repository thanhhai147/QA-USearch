from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
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
        session_id = data['session_id']
        try:
            query = data['query']
            bot_answer, answer_source = query_search(query)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"Lỗi xử lý file: {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_chat = Chat(
                session_id=Session.objects.get(session_id=session_id), 
                chat_position=Chat.objects.filter(session_id=session_id).count() + 1,
                user_ask=query,
                bot_answer=bot_answer,
                source="-".join(answer_source)
            )
            new_chat.save()
        except Exception as e:
            print(e)
            return Response(
                {
                    "success": False,
                    "message": "Lỗi Database"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "success": True,
                "data": {
                    "session_id": session_id,
                    "chat_id": new_chat.chat_id,
                    "chat_position": new_chat.chat_position,
                    "user_ask": new_chat.user_ask,
                    "bot_answer": new_chat.bot_answer
                },
                "message": "Search thành công",
            },
            status=status.HTTP_200_OK
        )

class GetSourceByChatIdAPIView(GenericAPIView):
    def get(self, request):
        query = request.query_params
        chat_id = query['chat_id']

        try:
            source_chat_instances = SourceChat.objects.filter(chat_id=chat_id)
            sources = [
                source_chat_instance.source_id.file_name
                for source_chat_instance in source_chat_instances
            ]
        except:
            return Response(
                {
                    "success": False,
                    "message": "Lỗi Database"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "success": True,
                "data": {
                    "sources": sources
                },
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

