from dataclasses import fields
from rest_framework import serializers
import datetime as dt
import webcolors

from .models import Achievement, AchievementCat, Cat, Owner

# Each tuple in the CHOICES constant represents a color option and consists of
# two elements:
#    the first element is the actual value that will be stored in the database
#    when the option is selected (e.g. 'Gray', 'Black', 'White', etc.).
#    the second element is the human-readable text that will be displayed in
#    the  UI to describe the option (e.g. 'Серый', 'Чёрный', 'Белый', etc.).
#
# By using these nested tuples, you can define a mapping between the internal
# database value and the external display value for each option, which makes
# it easier to display and select color options in a user-friendly way.
CHOICES = (
        ('Gray', 'Серый'),
        ('Black', 'Чёрный'),
        ('White', 'Белый'),
        ('Ginger', 'Рыжий'),
        ('Mixed', 'Смешанный'),
    )

class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value
    
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')
    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


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
    # color = Hex2NameColor()
    color = serializers.ChoiceField(choices=CHOICES)
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


class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Owner
        # 'cats' - это related_name в модели Cat
        fields = ('first_name', 'last_name', 'cats')