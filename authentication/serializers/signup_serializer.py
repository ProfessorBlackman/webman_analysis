from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=300, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        user = None
        try:
            password = validated_data.pop("password")
            user = User.objects.filter(email=validated_data.get("email")).update()
            user.set_password(password)
            user.save()
        except Exception:
            raise ValidationError("User does not exits")

        return user

    def validate(self, attrs):
        email_exits = User.objects.filter(email=attrs["email"]).exists()
        if email_exits:
            raise ValidationError("Email already exits")

        return super().validate(attrs)

class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)