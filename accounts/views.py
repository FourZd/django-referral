# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserSerializer,
    AuthRequestSerializer,
    VerifyCodeSerializer,
    ActivateInviteSerializer,
)
from django.core.exceptions import ObjectDoesNotExist
import time
import random
import string
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer, extend_schema

class RequestCodeView(APIView):
    @extend_schema(
        request=AuthRequestSerializer,
        responses={200: inline_serializer(
            name='RequestCodeResponse',
            fields={
                'message': serializers.CharField(),
                'code': serializers.CharField()
            }
        )},
        description="Sends a 4-digit verification code to the given phone number."
    )
    def post(self, request):
        serializer = AuthRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = ''.join(random.choices(string.digits, k=4))
            user, created = User.objects.update_or_create(
                phone_number=phone_number,
                defaults={'code_sent_time': timezone.now()}
            )
            user.set_verification_code(code)
            user.save()
            time.sleep(2)  # Имитация задержки отправки
            return Response({"message": "Code sent", "code": code}, status=200)
        return Response(serializer.errors, status=400)


class VerifyCodeView(APIView):
    @extend_schema(
        request=VerifyCodeSerializer,
        responses={
            200: inline_serializer(
                name='VerifyCodeResponse',
                fields={
                    'message': serializers.CharField(),
                    'access': serializers.CharField(),
                    'refresh': serializers.CharField()
                }
            ),
            400: {'description': 'Invalid or expired code'},
            404: {'description': 'User not found'}
        },
        description="Verifies the 4-digit code sent to the phone number and returns JWT tokens."
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            try:
                user = User.objects.get(phone_number=phone_number)
                if user.code_sent_time and timezone.now() - user.code_sent_time <= timezone.timedelta(minutes=5):
                    if User.check_verification_code(code, user.verification_code_hash):
                        # Генерация JWT токенов
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            "message": "Verification successful",
                            "access": str(refresh.access_token),
                            "refresh": str(refresh)
                        }, status=200)
                    else:
                        return Response({"message": "Invalid or expired code"}, status=400)
                else:
                    return Response({"message": "Code expired"}, status=400)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=404)
        return Response(serializer.errors, status=400)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer},
        description="Fetches the profile of the authenticated user."
    )
    def get(self, request):
        try:
            user = User.objects.get(
                phone_number=request.user.phone_number
            )
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=404)


class ActivateInviteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ActivateInviteSerializer,
        responses={
            200: {'description': 'Invite code activated successfully'},
            400: {'description': 'Invite code already activated or invalid'},
            409: {'description': 'Cannot activate own invite code'}
        },
        description="Activates an invite code for the authenticated user."
    )
    def post(self, request):
        serializer = ActivateInviteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(phone_number=request.user.phone_number)
                invite_code = serializer.validated_data["invite_code"]
                
                # Check if the invite code belongs to the user
                if invite_code == user.invite_code:
                    return Response(
                        {"message": "Cannot activate own invite code"}, status=409
                    )

                referrer = User.objects.get(invite_code=invite_code)
                
                # Check if the user has already a referrer
                if user.referrer:
                    return Response(
                        {"message": "Invite code already activated"}, status=400
                    )
                
                user.referrer = referrer
                user.save()
                return Response({"message": "Invite code activated successfully"})
            except User.DoesNotExist:
                return Response({"message": "Invalid invite code"}, status=400)
        return Response(serializer.errors, status=400)
