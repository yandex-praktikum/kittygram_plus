from dataclasses import fields
from rest_framework import serializers
import datetime as dt

from .models import Achievement, AchievementCat, Cat, Owner


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ('id', 'name')


class CatSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField(read_only=True)
    # переопределим поле 'achievements', чтобы получать не id достижений, а
    # объекты Achievements:
    achievements = AchievementSerializer(
        # read_only=True,  # убрали для возможности записи через
                           # переопределенный метод create() и update()
        many=True,
        required=False  # поле не является обязательным
        )
    age = serializers.SerializerMethodField()
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner',
                  'achievements', 'age')
        
    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data):
        # Если в исходном запросе не было поля achievements
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        
        # уберем список достижений из словаря validated_data и сохраним его:
        achievements = validated_data.pop('achievements')
        # создаем нового кота пока без достижений
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            # Создадим новую запись или получим существующий экземпляр из БД:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            AchievementCat.objects.create(
                achievement=current_achievement,
                cat=cat
            )
        return cat


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Owner
        # 'cats' - это related_name в модели Cat
        fields = ('first_name', 'last_name', 'cats')