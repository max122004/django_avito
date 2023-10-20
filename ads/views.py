from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from ads.models import Category, Ad, Like, Comment
from ads.serializer import CategoryListSerializer, AdListSerializer, AdDetailSerializer, \
    AdCreateSerializer, AdUpdateSerializer, AdDeleteSerializer, LikeSerializer, CommentSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        ad_name = request.GET.get('name', None)
        if ad_name:
            self.queryset = self.queryset.filter(
                name__icontains=ad_name
            )
        if request.GET.get('price_to', None):
            self.queryset = self.queryset.filter(
                price__gte=request.GET.get('price_to')
            )

        if request.GET.get('price_from', None):
            self.queryset = self.queryset.filter(
                price__lte=request.GET.get('price_from')
            )
        if request.GET.get('cat', None):
            self.queryset = self.queryset.filter(
                category__name__icontains=request.GET.get('cat')
            )
        if request.GET.get('location', None):
            locations_q = None
            for location in request.GET.get('location'):
                if locations_q is None:
                    locations_q = Q(author__locations__name__icontains=location)
                else:
                    locations_q |= Q(author__locations__name__icontains=location)
            if locations_q:
                self.queryset = self.queryset.filter(locations_q)
        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer

    def perform_create_like(self, ad):
        # Создаем сериализатор для объекта лайка, используя данные из запроса
        serializer_like = LikeSerializer(data=self.request.data)
        # Проверяем, что данные валидны
        serializer_like.is_valid(raise_exception=True)
        # Сохраняем лайк, связывая его с пользователем и статьей
        serializer_like.save(user=self.request.user, ad=ad)

    def get(self, request, *args, **kwargs):
        # Вызываем метод get() суперкласса для получения статьи
        response = super().get(request, *args, **kwargs)
        # Получаем объект статьи
        ad = self.get_object()
        # Получаем все лайки, связанные со статьей
        likes = ad.likes.all()
        # Создаем сериализатор для списка лайков
        like_serializer = LikeSerializer(likes, many=True)
        # Получаем данные статьи, используя сериализатор для детального представления
        response_data = self.serializer_class(ad).data
        # Добавляем данные о лайках в объект ответа
        response_data['likes'] = like_serializer.data
        # Возвращаем объект ответа, содержащий данные о статье и ее лайках
        return Response(response_data)


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })


class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        ad_id = self.request.data.get('ad')
        ad = Ad.objects.get(id=ad_id)
        serializer.save(
            user=self.request.user,
            ad=ad
        )


class LikedAdAPIView(ListAPIView):
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        liked_ad = Ad.objects.filter(likes__user=self.request.user)
        serializer = self.serializer_class(liked_ad, many=True)
        return Response(serializer.data)


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        ad_id = self.request.data.get('ad')
        ad = Ad.objects.get(id=ad_id)
        serializer.save(
            user=self.request.user,
            ad=ad
        )

