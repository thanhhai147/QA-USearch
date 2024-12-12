from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils import timezone
from rest_framework import status
from ..models.session import Session
from ..models.chat import Chat
from ..AI.QALLM import infer

class CreateChatAPIView(GenericAPIView):
    def post(self, request):
        data = request.data
        try:
            session_id = data['session_id']
            user_ask = data['user_ask']
            model = data['model']
            prompting = data['prompting']
        except:
            return Response(
                {
                    "success": False,
                    "message": "Thông tin trò chuyện không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not session_id:
            return Response(
                {
                    "success": False,
                    "message": "Mã phiên không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user_ask:
            return Response(
                {
                    "success": False,
                    "message": "Câu hỏi không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not model:
            return Response(
                {
                    "success": False,
                    "message": "Mô hình không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not prompting:
            return Response(
                {
                    "success": False,
                    "message": "Prompting không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            _ = Session.objects.get(session_id=session_id)
        except Session.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Phiên không tồn tại"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            return Response(
                {
                    "success": False,
                    "message": "Lỗi Database"
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            chat_position = Chat.objects.filter(session_id=session_id).count() + 1
        except Chat.DoesNotExist:
            chat_position = 1
        except:
            return Response(
                {
                    "success": False,
                    "message": "Lỗi Database"
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            session_instance = Session.objects.get(session_id=session_id)
            bot_answer = infer(source=model, technique_prompt=prompting, context=session_instance.context, question=user_ask)
            chat_instance = Chat(session_id=session_instance, model=model, prompting=prompting, chat_position=chat_position, user_ask=user_ask, bot_answer=bot_answer)
            chat_instance.save()
            session_instance.updated_at = timezone.now()
            session_instance.save()
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
                "message": "Tạo thành công trò chuyện mới",
                "data": {
                    "chat_id": chat_instance.chat_id,
                    "session_id": session_id,
                    "chat_position": chat_position,
                    "model": model,
                    "prompting": prompting,
                    "user_ask": user_ask,
                    "bot_answer": bot_answer
                }
            }, 
            status=status.HTTP_200_OK
        )
    
class GetChatAPIView(GenericAPIView):
    def get(self, request):
        params = request.query_params
        try:
            session_id = params['session_id']
        except:
            return Response(
                {
                    "success": False,
                    "message": "Thông tin trò chuyện không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not session_id:
            return Response(
                {
                    "success": False,
                    "message": "Mã phiên không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            _ = Session.objects.get(session_id=session_id)
        except Session.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Phiên không tồn tại"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            return Response(
                {
                    "success": False,
                    "message": "Lỗi Database"
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            chat_instances = Chat.objects.filter(session_id=session_id).order_by('chat_position')
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
                "message": "Lấy thành công trò chuyện",
                "data": {
                    "chats": sorted(
                        [
                            {
                                "chat_id": chat.chat_id,
                                "session_id": chat.session_id.session_id,
                                "model": chat.model,
                                "prompting": chat.prompting,
                                "chat_position": chat.chat_position,
                                "user_ask": chat.user_ask,
                                "bot_answer": chat.bot_answer
                            }
                            for chat in chat_instances.iterator()
                        ],
                        key=lambda chat: chat['chat_position'], reverse=False
                    )
                }
            }, 
            status=status.HTTP_200_OK
        )
    
class DeleteChatAPIView(GenericAPIView):
    def post(self, request):
        data = request.data
        try:
            session_id = data['session_id']
        except:
            return Response(
                {
                    "success": False,
                    "message": "Thông tin trò chuyện không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not session_id:
            return Response(
                {
                    "success": False,
                    "message": "Mã phiên không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            _ = Session.objects.get(session_id=session_id)
        except Session.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Phiên không tồn tại"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            return Response(
                {
                    "success": False,
                    "message": "Lỗi Database"
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            chat_instances = Chat.objects.filter(session_id=session_id)
            for chat in chat_instances:
                chat.delete()
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
                "message": "Xóa thành công trò chuyện"
            }, 
            status=status.HTTP_200_OK
        )