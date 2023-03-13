from django.db import models


class Achievement(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Owner(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        Owner,
        related_name='cats',
        on_delete=models.CASCADE,
    )
    # Связь ManyToMany будет описана через вспомогательную модель
    # AchievementCat:
    achievements = models.ManyToManyField(
        Achievement, through='AchievementCat')


    def __str__(self):
        return self.name
    
# В этой модели будут связаны id котика и id его достижения
class AchievementCat(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'