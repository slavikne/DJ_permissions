from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )



    def create(self, validated_data):
        """Метод для создания"""

        if len(Advertisement.objects.filter(creator=self.context["request"].user, status='OPEN')) > 9:

            raise ValidationError('Разрешено создание 10 объявлений')

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            if len(Advertisement.objects.filter(creator=self.context["request"].user, status='OPEN')) > 9:
                raise ValidationError('Открытых объявлений должно быть не более 10')

        return super().update(instance, validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        return data


