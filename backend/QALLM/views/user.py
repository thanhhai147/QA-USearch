from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from ..models.user import User
from ..validators.custom_validators import AdancedValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class SignupAPIView(GenericAPIView):
    def post(self, request):
        data = request.data
        try:
            user_name = data['user_name']
            password = data['password']
        except:
            return Response(
                {
                    "success": False,
                    "message": "Thông tin người dùng không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user_name or not AdancedValidator.check_user_name(user_name):
            return Response(
                {
                    "success": False,
                    "message": "Tên người dùng không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not password or not AdancedValidator.check_password(password):
            return Response(
                {
                    "success": False,
                    "message": "Mật khẩu không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            instance = User.objects.get(user_name=user_name)
        except User.DoesNotExist:
            instance = None

        if instance:
            return Response(
                {
                    "success": False,
                    "message": "Tên người dùng đã tồn tại"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            hashed_password = make_password(password)
            instance = User(user_name=user_name, password=hashed_password)
            instance.save()
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
                "message1": "Tạo thành công người dùng mới",
                "message2": "Vui lòng đăng nhập để tiếp tục",
                "data": {
                    "user_id": instance.user_id,
                    "user_name": instance.user_name
                }
            }, 
            status=status.HTTP_200_OK
        )

class LoginAPIView(GenericAPIView):
    def post(self, request):
        data = request.data
        try:
            user_name = data['user_name']
            password = data['password']
        except:
            return Response(
                {
                    "success": False,
                    "message": "Thông tin người dùng không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user_name or not AdancedValidator.check_user_name(user_name):
            return Response(
                {
                    "success": False,
                    "message": "Tên người dùng không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not password or not AdancedValidator.check_password(password):
            return Response(
                {
                    "success": False,
                    "message": "Mật khẩu không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            instance = User.objects.get(user_name=user_name)
            if not check_password(password, instance.password):
                return Response(
                    {
                        "success": False,
                        "message": "Mật khẩu không hợp lệ"
                    }, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            instance.login_at = timezone.now()
            instance.save()
            
        except User.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Người dùng không tồn tại"
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
        
        return Response(
            {
                "success": True,
                "message": "Đăng nhập thành công",
                "data": {
                    "user_id": instance.user_id,
                    "user_name": instance.user_name,
                    "login_at": instance.login_at
                }
            }, 
            status=status.HTTP_200_OK
        )
    
class LogoutAPIView(GenericAPIView):
    def post(self, request):
        data = request.data
        try:
            user_id = data['user_id']
        except:
            return Response(
                {
                    "success": False,
                    "message": "Thông tin người dùng không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user_id:
            return Response(
                {
                    "success": False,
                    "message": "Mã người dùng không hợp lệ"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            instance = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Người dùng không tồn tại"
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
        
        return Response(
            {
                "success": True,
                "message": "Đăng xuất thành công"
            }, 
            status=status.HTTP_200_OK
        )