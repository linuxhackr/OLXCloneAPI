import pyotp
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from OLXCloneAPI.utilities import send_otp_email
from account.api.serializers import UserSerializer
from account.models import User
from account.utils import get_token


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)
    else:
        mobile = request.data.get('mobile', None)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        fullname = request.data.get('fullname', None)
        email = request.data.get('email', None)

        if not username or not mobile or not email or not password or not fullname:
            return Response({'msg': 'All fields are required'}, status.HTTP_400_BAD_REQUEST)

        user = None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        if user:
            return Response({'msg': 'Username is not available'}, status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            pass
        if user:
            return Response({'msg': 'Mobile number is already in use'}, status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        if user:
            return Response({'msg': 'Email ID is already in use'}, status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=username, fullname=fullname, email=email, mobile=mobile)
        user.set_password(password)
        user.save()

        token = get_token(user)
        serializer = UserSerializer(user)
        return Response({'user':serializer.data, 'token':token}, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.user.is_authenticated:
        token = get_token(request.user)
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data, 'token': token}, status.HTTP_200_OK)
    else:
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'msg': 'Invalid Credentials.'}, status.HTTP_401_UNAUTHORIZED)

        token = get_token(user)
        serializer = UserSerializer(user)
        return Response({'user':serializer.data, 'token':token}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    # pass token & get user object
    serializer = UserSerializer(request.user, context={'request': request})
    data = serializer.data
    token = get_token(request.user)
    return Response({"user": data, "token": token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get('email', None)
    if email:
        user = get_object_or_404(User, email=email)
        if user:
            # generate OTP
            time_otp = pyotp.TOTP(user.key)
            time_otp = time_otp.now()

            send_otp_email(user.email, time_otp)

            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Email ID is not registered!"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Email ID is required!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):

    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    if email is None:
        return Response({"message": "Email ID is required!"}, status=status.HTTP_400_BAD_REQUEST)
    if otp is None:
        return Response({"message": "OTP is required!"}, status=status.HTTP_400_BAD_REQUEST)
    if new_password is None:
        return Response({"message": "New Password is required!"}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, email=email)

    t = pyotp.TOTP(user.key)
    is_verified = t.verify(otp, valid_window=20)  # valid_window 20 minutes => otp will be valid for 30*20 SECONDS

    if not is_verified:
        return Response({"message": "Invalid OTP!"}, status=status.HTTP_401_UNAUTHORIZED)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def update_account(request):
    fullname = request.data.get('fullname', None)
    pic = request.FILES.get('pic', None)

    user = request.user

    if fullname is not None:
        fullname = str(fullname).strip()
        user.fullname = fullname

    if pic is not None:
        user.pic = pic

    user.save()
    serializer = UserSerializer(user, context={'request': request})
    data = serializer.data
    token = get_token(user)

    return Response({"user": data, "token": token}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({'message': 'success'}, status=status.HTTP_200_OK)
