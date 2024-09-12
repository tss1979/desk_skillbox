# runapscheduler.py
import logging
import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.core.mail import send_mail
from django.contrib.auth.models import User
from desk.models import Post, Subscription, OneTimeCode

logger = logging.getLogger(__name__)


def send_new_posts_notification():
    message = ''
    period = datetime.datetime.now() - datetime.timedelta(weeks=1)
    subscriptions = Subscription.objects.all().select_related('user')
    mails = [sbs.user.email for sbs in subscriptions]
    posts = Post.objects.filter(created_at__gte=period)
    titles = [post.title for post in posts]
    links = ['http://127.0.0.1:8000/' + str(post.pk) for post in posts]
    for t, l in zip(titles, links):
        message += f'{t} - {l}\n'
    send_mail(
        subject='Привес с Desk, новые посты',
        message=message,
        from_email='serege1.tashkinov@yandex.ru',
        recipient_list=mails
    )

def clear_table_one_code():
        OneTimeCode.objects.all().delete()

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_new_posts_notification,
            trigger=CronTrigger(week="*/1"),  # Every 1 week
            id="send_new_posts_notification",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        scheduler.add_job(
            clear_table_one_code,
            trigger=CronTrigger(week="*/1"),  # Every 1 week
            id="clear_table_one_code",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_new_posts_notification'.")
        logger.info("Added job 'clear_table_one_code'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="09", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")