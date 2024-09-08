from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Comment, Post
from django.contrib.auth.models import User
from .tasks import send_notification_post_created


@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, **kwargs):
    send_notification_post_created.apply_async(instance=instance)

@receiver(post_save, sender=Comment)
def send_new_comment_notification(sender, instance, created, **kwargs):
    comment = instance
    user = comment.target_user
    send_mail(
        subject='Новое письмо на Desk',
        message='http://127.0.0.1:8000/in-comments',
        from_email='serege1.tashkinov@yandex.ru',
        recipient_list=[user.email,]
    )


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     user = instance
#     common_group = Group.objects.get(name='common')
#     common_group.user_set.add(user)
#     send_mail(
#         subject='Welcome to the NewsPortal',
#         message='Greeting from The NewsPortal',
#         from_email='tashkinov2@gmail.com',
#         recipient_list=[user.email]
#     )