from django.db import models
from django.contrib.auth.models import User

KIND_DICT = {'T': 'Танки', 'Н': 'Хилы', 'D': 'ДД', 'S': 'Торговцы', 'G': 'Гилдмастеры',
             'KV': 'Квестгиверы', 'KZ': 'Кузнецы', 'KQ': 'Кожевники', 'Z': 'Зельевары',
             'M': 'Мастера заклинаний'}

NULLABLE = {'blank': True, 'null': True}
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post_kind = models.CharField(max_length=2, choices=KIND_DICT)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pk} - {self.title}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += -1
        self.save()


class Comment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()

class OneTimeCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    code = models.CharField(max_length=20)








