from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserRegisterSerializer, UserDetailSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class UserRegisterView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserRegisterSerializer

    def get_serializer_class(self):
        serializer_class = UserRegisterSerializer
        if self.action == 'change_password':
            serializer_class = ChangePasswordSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):
        """
        register as normal user
        """
        serialized = UserRegisterSerializer(data=request.data, context={'request': request})
        if serialized.is_valid(raise_exception=True):
            users = serialized.create()
            serialized = UserDetailSerializer(users)
            return Response(serialized.data, status=201)
        raise Http404

    @action(methods=['POST'], detail=False)
    def blogger(self, request, *args, **kwargs):
        """
        register as blogger
        """
        serialized = UserRegisterSerializer(data=request.data, context={'request': request})
        if serialized.is_valid(raise_exception=True):
            users = serialized.blogger()
            serialized = UserDetailSerializer(users)
            return Response(serialized.data, status=201)
        raise Http404

    @action(methods=['GET', ], detail=False, permission_classes=[IsAuthenticated])
    def get_user(self, request):
        """
        details of  user
        """
        serialized = UserRegisterSerializer()
        users = serialized.details(by=request.user)
        serialized = UserDetailSerializer(users)
        return Response(serialized.data, status=200)

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serialized = self.get_serializer(data=request.data, context={'request': request})
        if serialized.is_valid(raise_exception=True):
            users = serialized.change_password(by=request.user)
            serialized = UserDetailSerializer(users)
            return Response(serialized.data, status=200)
        raise Http404



class ObtainAccessTokenSerializer(TokenObtainPairSerializer):
    """get jwt token over ride """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_writer'] = user.is_writer
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if not self.user.is_superuser:
            data['first_name'] = self.user.first_name
            data['last_name'] = self.user.last_name
            data['is_writer'] = self.user.is_writer
        return data


class ObtainAccessTokenView(TokenObtainPairView):
    serializer_class = ObtainAccessTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
