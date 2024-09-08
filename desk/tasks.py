from celery import shared_task
from .models import OneTimeCode, Subscription
from django.core.mail import send_mail


@shared_task
def clear_table_one_code():
    OneTimeCode.objects.all().delete()

@shared_task
def send_notification_post_created(instance):
    subject = f'Новый Пост - {instance.title}'
    message = 'http://127.0.0.1:8000/' + str(instance.pk)
    subs = Subscription.objects.all()
    mails = []
    for sub in subs:
            mails.append(sub.user.email)

    send_mail(
        subject=subject,
        message=message,
        from_email='serege1.tashkinov@yandex.ru',
        recipient_list=mails
    )