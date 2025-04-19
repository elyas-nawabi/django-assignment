from django.utils.timezone import now
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .models import CustomUser, EmailOTP, generate_otp
from .serializers import RegisterSerializer, OTPVerifySerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate, login

OTP_EXPIRY_MINUTES = 10


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: None, 400: dict},
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            otp_code = generate_otp()
            EmailOTP.objects.create(user=user, otp_code=otp_code)

            # Send the OTP via email
            send_mail(
                subject="Verify your email",
                message=f"Your OTP code is: {otp_code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response(
                {"message": "User created. Check your email for OTP."}, status=201
            )
        return Response(serializer.errors, status=400)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=OTPVerifySerializer,
        responses={200: None, 400: dict},
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(email=serializer.validated_data["email"])
                otp = EmailOTP.objects.filter(
                    user=user,
                    otp_code=serializer.validated_data["otp_code"],
                    is_used=False,
                ).latest("created_at")

                # Check expiration
                if otp.created_at + timedelta(minutes=OTP_EXPIRY_MINUTES) < now():
                    return Response({"error": "OTP has expired"}, status=400)

                # Mark email as verified
                user.is_email_verified = True
                user.save()

                otp.is_used = True
                otp.save()

                return Response({"message": "Email verified successfully."})
            except (CustomUser.DoesNotExist, EmailOTP.DoesNotExist):
                return Response({"error": "Invalid email or OTP"}, status=400)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: dict, 401: dict},
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)

            if user and user.is_email_verified:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            return Response(
                {"error": "Invalid credentials or email not verified"}, status=401
            )
        return Response(serializer.errors, status=400)
