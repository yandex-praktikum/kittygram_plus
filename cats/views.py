from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cat, Owner
from .serializers import CatSerializer, OwnerSerializer, CatListSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    # Задача - по url 'cats/recent-white-cats/' отдавать информацию о пяти
    # последних добавленных котиках белого цвета
    # Декоратор @action для таких нестандартных действий настраивает метод и
    # создает эндпойнты. Параметры, которые в него передаются:
    # - methods=['get', 'delete', ...] - по умолчанию @action отслеживает
    #   только GET-запрос. Другие типы можно передать через 'methods='
    # - detail=... Если False - будет выдан список объектов. Если True - один
    #   объект.
    # - url_path= по умолчанию эндпойнт для метода будет определен как
    #   название метода ('recent_white_cats'), но нам нужно переопределить url
    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        cats =Cat.objects.filter(color='White')[:5]
        # Передадим queryset cats сериализатору и разрешим работу со списком
        # объектов
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CatListSerializer
        return CatSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset=Owner.objects.all()
    serializer_class = OwnerSerializer


class CreateRetrieveViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass


class LightCatViewSet(CreateRetrieveViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    ...