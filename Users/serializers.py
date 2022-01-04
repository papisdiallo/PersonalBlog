from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

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

    def validate(self, attrs):
        username = attrs.get("username", "")
        print(username)
        print(username.isalnum())
        if not username.isalnum():
            raise serializers.ValidationError(
                "the username must only contain letters and numbers"
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
