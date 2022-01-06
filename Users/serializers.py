from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=30,
        min_length=7,
        write_only=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
        )

    def validate(self, args):
        username = args.get("username", "")
        if not username.isalnum():
            raise serializers.ValidationError(
                "the username must only contain letters and numbers"
            )
        return args

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)
    username = serializers.CharField(max_length=600, read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "tokens",
            "username",
        ]

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])
        tokens = RefreshToken.for_user(user)
        return {
            "refresh": str(tokens),
            "access_token": str(user.tokens["access_token"]),
        }

    def validate(self, args):

        email = args.get("email", "")
        password = args.get("password", "")
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(
                "The provided credentials are not correct. Please try again"
            )
        if not user.is_developer_account:  # check if it's a dev account
            raise AuthenticationFailed(
                "Please make sure to login with your developer account"
            )
        if not user.is_verified:  # check if the email has been verified
            raise AuthenticationFailed(
                "Please visit the link sent to your email to activate your account"
            )

        return {"username": user.username, "email": user.email, "tokens": user.tokens}
