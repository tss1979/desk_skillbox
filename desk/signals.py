from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.defaulttags import comment
from django.contrib.auth.models import User

from .models import Comment, Post, OneTimeCode
from .utils import generate_code



@receiver(post_save, sender=Comment)
def send_new_comment_notification(sender, instance, created, **kwargs):
    comment = instance
    user = comment.target_user
    send_mail(
        subject='Новое письмо на Desk',
        message='http://127.0.0.1:8000/comments',
        from_email='serege1.tashkinov@yandex.ru',
        recipient_list=[user.email,]
    )


@receiver(post_save, sender=Comment)
def update_comment_is_confirmed(sender, instance, created, **kwargs):
    if instance.is_confirmed and not created:
        send_mail(
            subject='Ваше сообщение принято',
            message=f'Ваше сообщение {comment.text} принято',
            from_email='serege1.tashkinov@yandex.ru',
            recipient_list=[instance.sender.email,]
        )

@receiver(post_save, sender=User)
def create_user_send_code(sender, instance, created, **kwargs):
    code = generate_code()
    if instance:
        OneTimeCode.objects.create(user=instance, code=code)
        send_mail(
            subject='Добро пожаловать в Desk',
            message=f'Ваш код подтверждения - {code}',
            from_email='serege1.tashkinov@yandex.ru',
            recipient_list=[instance.email,]
        )