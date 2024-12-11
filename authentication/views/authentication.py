from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User
from ..serializers.login_serializer import LoginSerializer
from ..serializers.signup_serializer import SignUpSerializer, OTPSerializer
from ..utils.otp import get_otp, verify_otp, generate_otp, save_otp, send_otp


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="Sign Up")
    def post(self, request):
        print("starting signup")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            otp = generate_otp()
            save_otp(email=serializer.data.get('email'), otp=otp)
            send_otp(email=serializer.data.get('email'), otp=otp)
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Verify Email", query_serializer=OTPSerializer)
    def get(self, request):
        print("verify otp")
        email = request.query_params.get('email')
        otp = request.query_params.get('otp')
        print(f"otp: {otp} | email: {email}")
        otp_from_cache = ''
        if email and otp:
            print("not null")
            otp_from_cache = get_otp(email=email)
            print(f"otp: {otp} | redis: {otp_from_cache}")
        if not otp_from_cache:
            new_otp = generate_otp()
            save_otp(email, new_otp)
            send_otp(email, new_otp)
            return Response({'message': "OTP has expired, check your email for a new one"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not verify_otp(otp_from_user=otp, stored_otp=otp_from_cache):
            return Response({'message': "Invalid otp"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user = User.objects.filter(email=email).first()
        if user:
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified'}, status=status.HTTP_200_OK)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def generate_user_tokens(self, user):
        if user is not None and not user.is_blocked:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

    @swagger_auto_schema(operation_summary="Login")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            print(f"email: {email} | password: {password}")

            try:
                authenticate(email=email, password=password)
            except Exception :
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            user: User = User.objects.filter(email=email).first()

            if user and user.is_verified:
                tokens = self.generate_user_tokens(user)
                if tokens:
                    return Response(tokens, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
