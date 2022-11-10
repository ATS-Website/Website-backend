
import jwt

from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from Accounts.renderers import CustomRenderer
from Accounts.serializers import RegisterationSerializer, ResetPasswordSerializer
from Accounts.utils import Utils
from Accounts.models import Account

from .serializers import LoginSerializer, RegisterationSerializer, ChangePasswordSerializer, UserSerializer, SetNewPasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.renderers import BrowsableAPIRenderer
from django.contrib.auth.models import User
from django.conf import settings
from .permissions import IsAdmin
from .mixins import IsAdminOrReadOnlyMixin
from .permissions import IsValidRequestAPIKey


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class LoginView(IsValidRequestAPIKey, TokenObtainPairView):
    serializer_class = LoginSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class ChangePasswordAV(IsValidRequestAPIKey, generics.UpdateAPIView):
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class RegistrationView(IsAdminOrReadOnlyMixin, generics.CreateAPIView):
    serializer_class = RegisterationSerializer
    # permission_classes = [IsAdmin]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def post(self, request, *args, **kwargs):
        serializer = RegisterationSerializer(data=request.data)
        data = {}
        print(serializer.is_valid(), "dd")
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            first_name = serializer.validated_data.get("first_name")
            last_name = serializer.validated_data.get("last_name")
            email = serializer.validated_data.get("email")
            gender = serializer.validated_data.get("gender")
            print(gender)
            password = serializer.validated_data.get("password")
            # confirm_password = serializer.validated_data.get("password2")
            account = Account.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, gender=gender, email=email, password=password)
            data["status"] = "success"
            data["username"] = account.username
            data["email"] = account.email
            refresh_token = RefreshToken.for_user(account)
            data["refresh_token"] = str(refresh_token)
            data["access_token"] = str(refresh_token.access_token)
            return Response(data, status=status.HTTP_201_CREATED)
        data["error"] = serializer.errors
        data["status"] = "success"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


# class CreateTechStarView(generics.CreateAPIView):
#     serializer_class = TechStarSerializer
#     permission_classes = [IsAdmin]
#     renderer_classes = [CustomRenderer]

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             username = serializer.validated_data.get("username")
#             first_name = serializer.validated_data.get("first_name")
#             last_name = serializer.validated_data.get("last_name")
#             email = serializer.validated_data.get("email")
#             gender = serializer.validated_data.get("gender")
#             password = serializer.validated_data.get("password")
#             # confirm_password = serializer.validated_data.get("password2")
#             account = Account.objects.create_user(
#                 first_name=first_name, last_name=last_name, username=username, gender=gender, email=email, password=password)
#             data["status"] = "success"
#             data["username"] = account.username
#             data["email"] = account.email
#             refresh_token = RefreshToken.for_user(account)
#             data["refresh_token"] = str(refresh_token)
#             data["access_token"] = str(refresh_token.access_token)

#             return Response(data, status=status.HTTP_201_CREATED)
#         data["error"] = serializer.errors
#         data["status"] = "success"
#         return Response(data, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    # serializer_class = VerifyEmailSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description="Description", type=openapi.TYPE_STRING)

    @ swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, secret_key=settings.SECRET_KEY)
            account = Account.objects.get(id=payload.get('user_id'))

            if not account.is_active:
                account.is_active = True
                account.save()
                return Response({
                    "message": " Account Successfully activated!",
                    "status": "success",
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": " Account already activated!",
                    "status": "success",
                }, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as e:
            print(e)
            return Response({"error": f"Activation expired:{e}", "status": "fail", }, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({"error": f"Invalid token: {e}", "status": "success", }, status=status.HTTP_400_BAD_REQUEST)


class AccountsRetrieveAV(generics.ListAPIView):
    queryset = Account.objects.select_related("profile").all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return super(AccountsRetrieveAV, self).get_queryset()
        return self.queryset.filter(username=user.username)


# class TechStarRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
#     queryset = Account.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UpdateUserSerializer

#     def retrieve(self, request, *args, **kwargs):
#         serializer = self.serializer_class(self.request.user)
#         print(serializer)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def update(self, request, *args, **kwargs):
#         serializer_data = request.data.get('user', {})
#         user_data = request.data.get('user', {})

#         serializer_data = {
#             'username': user_data.get('username', request.user.username),
#             'email': user_data.get('email', request.user.email),
#             'profile': {
#                 'bio': user_data.get('bio', request.user.profile.bio),
#                 'image': user_data.get('image', request.user.profile.image)
#             }
#         }

#         serializer = self.serializer_class(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPassordAV(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        lower_email = serializer.validated_data.get("email").lower()
        if Account.objects.filter(email__iexact=lower_email).exists():
            account = Account.objects.get(email=lower_email)
            uuidb64 = urlsafe_base64_encode(account.id)
            token = PasswordResetTokenGenerator().make_token(account)
            current_site = get_current_site(
                request).domain
            relative_path = reverse(
                "reset-password", kwargs={"uuidb64": uuidb64, "token": token})
            abs_url = "http://" + current_site + relative_path

            mail_subject = "Please Reset your Account Password"
            message = "Hi" + account.username + "," + \
                " Please Use the Link below to reset your account passwors:" + "" + abs_url

            Utils.send_email(mail_subject, message, account.email)
        return Response({"status": "success", "message": "We have sent a password-reset link to the email you provided.Please check and reset  "}, status=status.HTTP_200_OK)


class ResetPassordAV(APIView):
    serializer_class = ResetPasswordSerializer
    renderer_classes = [CustomRenderer]

    def get(self, request, uuidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            account = Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(account, token):
                return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "message": "Your credentials valid", "uuidb64": uuidb64, "token": token}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoUnicodeDecodeError as e:
            return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAV(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    renderer_classes = [CustomRenderer]

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"status": "success", "message": "Password was successfully reset"}, status=status.HTTP_200_OK)
