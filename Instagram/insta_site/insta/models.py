from django.contrib.auth.models import AbstractUser
from django.db import models


GENDER = (
        ('Женский', 'Женский'),
        ('Мужской', 'Мужской'),
        ('Пропустить', 'Пропустить'),
        ('Не указывать', 'Не указывать'),
)


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('ownerUser', 'ownerUser'),
        ('klientUser', 'klientUser'),
    )
    user_role = models.CharField(max_length=18, choices=ROLE_CHOICES, default='klientUser')
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    website = models.URLField(max_length=222, null=True, blank=True)
    gender = models.CharField(max_length=99, choices=GENDER, default='Другой')

    def __str__(self):
        return self.username if self.username else "Unnamed User"


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} - {self.following}'


class Post(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_post')
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    post_video = models.FileField(upload_to='post_video/', verbose_name='video', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hashtag = models.CharField(max_length=100, null=True, blank=True)
    created_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} - {self.description}'
      #  return f'{self.owner.username} - {self.description[:20]}'


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_like', on_delete=models.CASCADE)
    post_like = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.image}"


    def get_likes_count(self, obj):
        return obj.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment_post',  on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.text}'


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment_like',  on_delete=models.CASCADE)
    comment_like = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def get_likes_count(self, obj):
        return obj.likes.count()


class Story(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story_img', null=True, blank=True)
    video = models.FileField(upload_to='story_video/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)




class Save(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)



class SaveItem(models.Model):
    post_item = models.ForeignKey(Post, on_delete=models.CASCADE)
    save_item = models.ForeignKey(Save, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)



class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
