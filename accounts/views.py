import jwt

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.urls import reverse
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.renderers import BrowsableAPIRenderer
from django.conf import settings

from .serializers import ResetPasswordSerializer, UpdateAccountSerializer, \
    ProfileSerializer, LoginSerializer, RegisterationSerializer, ChangePasswordSerializer, UserSerializer, \
    SetNewPasswordSerializer
from .tasks import Utils
from .models import Account, Profile
from .permissions import IsAdmin
from .mixins import IsAdminOrReadOnlyMixin
from .permissions import IsValidRequestAPIKey

from tech_stars.utils import write_log_csv
from tech_stars.mixins import CustomRetrieveUpdateAPIView, CustomRetrieveUpdateDestroyAPIView
from tech_stars.renderers import CustomRenderer


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class LoginView(IsValidRequestAPIKey, TokenObtainPairView):
    serializer_class = LoginSerializer


class ChangePasswordAV(IsValidRequestAPIKey, CustomRetrieveUpdateAPIView):
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class RegistrationView(IsAdminOrReadOnlyMixin, generics.CreateAPIView):
    serializer_class = RegisterationSerializer

    # permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        avatar = request.FILES["profile_picture"]
        position = request.data.get("position")
        serializer = RegisterationSerializer(data=request.data)
        data = {}
        print(serializer.is_valid(), "dd")
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            first_name = serializer.validated_data.get("first_name")
            last_name = serializer.validated_data.get("last_name")
            email = serializer.validated_data.get("email")
            gender = serializer.validated_data.get("gender")
            password = serializer.validated_data.get("password")
            # confirm_password = serializer.validated_data.get("password2")
            account = Account.objects.create_user(
                first_name=first_name, last_name=last_name, username=username,
                gender=gender, email=email, password=password)
            try:
                profile = Profile.objects.create(account=account, avatar=avatar, position=position)
            except:
                account.delete()
                return Response({"message": "Kindly check the avatar and position sent"},
                                status=status.HTTP_400_BAD_REQUEST)
            data["status"] = "success"
            data["username"] = account.username
            data["email"] = account.email
            refresh_token = RefreshToken.for_user(account)
            data["refresh_token"] = str(refresh_token)
            data["access_token"] = str(refresh_token.access_token)
            data["profile_picture"] = profile.avatar.url
            data["position"] = profile.position
            return Response(data, status=status.HTTP_201_CREATED)
        data["error"] = serializer.errors
        data["status"] = "success"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    # serializer_class = VerifyEmailSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description="Description", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
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
            return Response({"error": f"Activation expired:{e}", "status": "fail", },
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({"error": f"Invalid token: {e}", "status": "success", }, status=status.HTTP_400_BAD_REQUEST)


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related("account")
    serializer_class = ProfileSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('account').get(
                account__pk=pk
            )
            print(profile)
            serializer = self.serializer_class(profile, data=request.data)
            if serializer.is_valid():
                profile = serializer.validated_data.get('profile', {})
                print(profile.account.email)
            data = {
                "username": profile.account.username,
                "bio": profile.position,
                "image": profile.avatar.url if profile.avatar.url else profile.avatar,
                "status": "success",
            }

            return Response(data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist as e:
            print("Error", e)
            return Response({"message": f"{e}"}, status=status.HTTP_404_NOT_FOUND)


# class ProfileRetrieveAPIView(generics.RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#
#     def retrieve(self, request, pk, *args, **kwargs):
#         try:
#             profile = Profile.objects.filter(account__pk=pk).first()
#             print(profile)
#             serializer = self.serializer_class(profile, data=request.data)
#             if serializer.is_valid():
#                 profile = serializer.validated_data.get('profile', {})
#                 print(profile.account.email)
#             data = {
#                 "username": "",
#                 "bio": profile.position,
#                 "image": profile.avatar.url if profile.avatar.url else profile.avatar,
#                 "status": "success",
#             }
#
#             return Response(data, status=status.HTTP_200_OK)
#
#         except Profile.DoesNotExist as e:
#             print("Error", e)
#             return Response({"message": f"{e}"}, status=status.HTTP_404_NOT_FOUND)


class AccountsRetrieveAV(generics.ListAPIView):
    queryset = Account.objects.select_related("profile").all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return super(AccountsRetrieveAV, self).get_queryset()
        return self.queryset.filter(username=user.username)


class ForgotPassordAV(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        print("here")
        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            lower_email = serializer.validated_data.get("email").lower()
            print(lower_email)
            if Account.objects.filter(email__iexact=lower_email).exists():
                account = Account.objects.get(email=lower_email)
                uuidb64 = urlsafe_base64_encode(
                    str(account.id).encode('utf-8'))
                token = PasswordResetTokenGenerator().make_token(account)
                current_site = get_current_site(
                    request).domain
                print(current_site)
                relative_path = reverse(
                    "reset-passwords", kwargs={"uuidb64": uuidb64, "token": token})

                abs_url = "http://" + current_site + relative_path

                mail_subject = "Please Reset your Account Password"
                message = "Hi" + account.username + "," + \
                          " Please Use the Link below to reset your account passwors:" + "" + abs_url

                Utils.send_email.delay(mail_subject, message, account.email)
                return Response({"status": "success",
                                 "message": "We have sent a password-reset link to the email you provided.Please check and reset  "},
                                status=status.HTTP_200_OK)
            return Response({"status": "error", "message": "The email provided doesn't exist in our records"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassordAV(APIView):
    serializer_class = ResetPasswordSerializer

    def get(self, request, uuidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            account = Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(account, token):
                return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {"status": "success", "message": "Your  credentials  have been validated", "uuidb64": uuidb64,
                 "token": token}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoUnicodeDecodeError as e:
            return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateAccountSerializer


class AccountRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateAccountSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # serializer_data = request.data.get('user', {})
        user_data = request.data.get('user', {})
        print(user_data)

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'profile': {
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image)
            }
        }
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message_obj = serializer.data.get((list(serializer.data.keys())[1]))
        write_log_csv(f"Updated {self.get_serializer().Meta.model.__name__}",
                      request.user.username, f"{message_obj} was updated")

        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountRetrieveUpdateDeleteAV(CustomRetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = UpdateAccountSerializer
    queryset = Account.active_objects.all()


class SetNewPasswordAV(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"status": "success", "message": "Password was successfully reset"}, status=status.HTTP_200_OK)


class ToggleContentManagerAV(APIView):

    def get(self, request, *args, **kwargs):
        account = Account.objects.filter(pk=kwargs.get("pk")).first()
        account.is_content_manager = not account.is_content_manager
        return Response({"message": f"{account.username} was successfully updated"}, status=status.HTTP_200_OK)


class ToggleMembershipManagerAV(APIView):

    def get(self, request, *args, **kwargs):
        account = Account.objects.filter(pk=kwargs.get("pk")).first()
        account.is_membership_manager = not account.is_membership_manager
        return Response({"message": f"{account.username} was successfully updated"}, status=status.HTTP_200_OK)


class ToggleAssessmentManagerAV(APIView):

    def get(self, request, *args, **kwargs):
        account = Account.objects.filter(pk=kwargs.get("pk")).first()
        account.is_assessment_manager = not account.is_assessment_manager
        return Response({"message": f"{account.username} was successfully updated"}, status=status.HTTP_200_OK)


class ToggleApplicationManagerAV(APIView):
    def get(self, request, *args, **kwargs):
        account = Account.objects.filter(pk=kwargs.get("pk")).first()
        account.is_application_manager = not account.is_application_manager
        return Response({"message": f"{account.username} was successfully updated"}, status=status.HTTP_200_OK)
