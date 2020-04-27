from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.hashers import make_password
from django.http import Http404


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_writer',)


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50, style={'input_type': 'email', 'placeholder': 'Email*'})
    first_name = serializers.CharField(max_length=50, style={'input_type': 'text', 'placeholder': 'First Name*'})
    last_name = serializers.CharField(max_length=50, style={'input_type': 'text', 'placeholder': 'Last Name*'})
    password = serializers.CharField(max_length=25, min_length=8,
                                     style={'input_type': 'password', 'placeholder': 'password'})
    confirm_password = serializers.CharField(max_length=25, min_length=8,
                                             style={'input_type': 'password', 'placeholder': 'confirm_password'})

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate(self, data):

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "password and confirm password not match."})
        return data

    def create(self, *args, **kwargs):
        if User.objects.filter(email=self.validated_data['email']):
            raise serializers.ValidationError({"email": "User already exists with this email."})

        user = User.objects.create(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'].capitalize(),
            last_name=self.validated_data['last_name'].capitalize(),
            password=make_password(self.validated_data['password']),
            is_staff=False,
        )
        return user

    def blogger(self, *args, **kwargs):
        if User.objects.filter(email=self.validated_data['email']):
            raise serializers.ValidationError({"email": "User already exists with this email."})

        user = User.objects.create(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'].capitalize(),
            last_name=self.validated_data['last_name'].capitalize(),
            password=make_password(self.validated_data['password']),
            is_staff=False,
            is_writer=True,
        )
        user.save()
        return user

    def details(self, by):
        users = User.objects.filter(email=by.email).first()
        if not users:
            raise Http404
        return users


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=25, min_length=8,
                                         style={'input_type': 'password', 'placeholder': 'old password'})
    new_password = serializers.CharField(max_length=25, min_length=8,
                                     style={'input_type': 'password', 'placeholder': 'new password'})
    confirm_password = serializers.CharField(max_length=25, min_length=8,
                                             style={'input_type': 'password', 'placeholder': 'confirm password'})

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "password and confirm password not match."})
        return data

    def change_password(self, by):
        user = User.objects.filter(email=by.email).first()
        if not user.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'old password does not match'})

        if self.validated_data['new_password'] != self.validated_data['old_password']:
            user.set_password(self.validated_data['new_password'])
            user.save()
            return user
        else:
            raise serializers.ValidationError({'old_password': 'old password and new password can not be same'})
