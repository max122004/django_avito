from rest_framework import serializers

from ads.models import Category, Ad, Like, Comment


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author', 'price', 'image']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    ad = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all()
    )

    class Meta:
        model = Comment
        fields = ['user', 'ad', 'created']


class AdDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ["id", 'image', "name", "username", "price", "description", "is_published", "name_category"]

    def get_likes_count(self, obj):
        # В данном случае obj будет представлять одну конкретную статью
        # (экземпляр модели Article), для которой нужно подсчитать
        # количество лайков.
        return obj.likes.count()


class AdCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    image = serializers.ImageField(required=False)

    class Meta:
        model = Ad
        fields = ["name", "author", "price", "description", "category", 'image']

    def create(self, validates_data):
        ad = Ad.objects.create(**validates_data)
        return ad


class AdUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Ad
        fields = ['name', 'price', 'description', 'is_published', 'image']

    def save(self):
        ad = super().save()
        ad.save()
        return ad


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    ad = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all()
    )

    class Meta:
        model = Like
        fields = ['user', 'ad', 'created']



