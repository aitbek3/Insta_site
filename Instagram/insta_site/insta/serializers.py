from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',

                  'user_role', 'gender']

        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']


class PostListSerializer(serializers.ModelSerializer):
    owner = UserProfileSimpleSerializer()

    class Meta:
        model = Post
        fields = ['id', 'owner', 'image', 'post_video']


class PostLikeSerializer(serializers.ModelSerializer):
    post = PostListSerializer(read_only=True, many=True)
    user = UserProfileSimpleSerializer()

    class Meta:
        model = PostLike
        fields = ['user', 'post', 'post_like']


class PostCreateSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Post
        fields = ['user', 'image', 'post_video', 'description', 'hashtag', 'created_data']


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = CommentLike
        fields = ['comment', 'user', 'comment_like']


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    comment_like = CommentLikeSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['post', 'user', 'text', 'parent', 'comment_like']


class StorySerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Story
        fields = ['user', 'image', 'video']


class SaveSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Save
        fields = ['user']


class SaveItemSerializer(serializers.ModelSerializer):
    save = SaveSerializer()

    class Meta:
        model = SaveItem
        fields = ['post', 'save']


class PostDetailSerializer(serializers.ModelSerializer):
    owner = UserProfileSimpleSerializer()
    post_like = PostLikeSerializer(many=True, read_only=True)
    comment_post = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['owner', 'image', 'post_video', 'description', 'post_like',
                  'comment_post', 'hashtag']
