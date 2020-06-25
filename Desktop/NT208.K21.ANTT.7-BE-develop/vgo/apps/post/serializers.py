from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)

    # favorited = serializers.SerializerMethodField()
    # favoritesCount = serializers.SerializerMethodField(
    #     method_name='get_favorites_count'
    # )

    # tagList = TagRelatedField(many=True, required=False, source='tags')

    # Django REST Framework makes it possible to create a read-only field that
    # gets it's value by calling a function. In this case, the client expects
    # `created_at` to be called `createdAt` and `updated_at` to be `updatedAt`.
    # `serializers.SerializerMethodField` is a good way to avoid having the
    # requirements of the client leak into our API.
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Post
        fields = (
            'author',
            'body',
            'createdAt',
            'description',
            # 'favorited',
            # 'favoritesCount',
            'slug',
            # 'tagList',
            'title',
            'updatedAt',
        )

    def create(self, validated_data):
        author = self.context.get('author', None)

        tags = validated_data.pop('tags', [])

        post = Post.objects.create(author=author, **validated_data)

        # for tag in tags:
        #     post.tags.add(tag)

        return post

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):
        post = self.context['post']
        author = self.context['author']

        return Comment.objects.create(
            author=author, post=post, **validated_data
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
