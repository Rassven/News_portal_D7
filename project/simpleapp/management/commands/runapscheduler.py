import logging
from project.mconfig import config

from datetime import datetime, date, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from simpleapp.models import Article, Category, Subscription
from django.core.mail import mail_managers
from django.core.mail import EmailMultiAlternatives

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


# D6.5:
# 1. В категории должна быть возможность пользователей ПОДПИСАТЬСЯ на ?РАССЫЛКУ? новых статей.
#                   Подписка на категорию подразумевает рассылку, или они раздельно?
# D6.7:
#   - ? Страница должна ... по адресу https://127.0.0.1:8000/subscriptions/; (чем плох ...8000/portal/subscriptions/?)
#   - ???добавьте команду запуска периодических задач (куда?);
#   - ?сообщение должно содержать только статьи, которые появились с момента предыдущей рассылки (т.е. за неделю).
def subs_list():
    cat_list = Category.objects.values_list('id', 'name'); print('Run subs_list job')
    for cat_id, cat_name in cat_list:  # Перебор категорий и поиск подписчиков (их email)
        emails = User.objects.filter(subscriptions__category=cat_id).values_list('email', flat=True)
        if emails:  # Есть подписчики, поиск статей по условию.
            print('Find', emails.count(), 'subscriber/s')
            # datetime.timedelta(weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0)
            last_time = datetime.now()-timedelta(weeks=1, days=0)
            # Составление списка статей.
            art_list = Article.objects.filter(
                category=cat_id, pub_time__gte=last_time
                ).values_list('id', 'pub_time', 'name', 'text', 'category')
            # print(art_list[:1], 'find:', art_list.count())
            if art_list:  # Статьи найдены
                print('Find:', art_list.count(), 'article/s')
                # Сборка содержимого для отправки
                subject = f'Новые статьи в категории "{cat_name}" за неделю:'
                text_content = ''; html_content = ''
                text_content_message = []; html_content_message = []

                for art_id, art_time, art_name, art_text, art_cat in art_list:
                    text_content_message.append(
                        f'Статья: {art_name} (опубликована: {str(art_time)[:16]})\n'
                        f'Кратко: {art_text[:30]}...  '
                        f'Полный текст: http://127.0.0.1:8000/portal/{art_id}'
                        )
                    html_content_message.append(
                        f'({str(art_time)[:16]})   "<i>{art_name}</i>"<br>'
                        f'<b>Кратко:</b> {art_text[:30]}...   '
                        f'(<a href="http://127.0.0.1/portal/{art_id}">Читать полностью</a>)'
                        )
                text_content = '/n/n'.join(text_content_message)  # print(text_content)
                html_content = '<br><br>'.join(html_content_message)  # print(html_content)

                # print('Sending emails...')
                for email in emails:
                    msg = EmailMultiAlternatives(subject, text_content, None, [config['ctrl_mail'], ])  # + email !
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

            else:
                print('Not find')


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        print('def handle')
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            subs_list,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),  # trigger=CronTrigger(second="*/10"),
            id="subs_list",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'subs_list'.")  # ; print('logger.info("Added job "subs_list".")')
        # job_time = datetime.now()

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),  # trigger=CronTrigger(day="*/01"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")
        print(' logger.info("Added weekly job: '"delete_old_job_executions"'.")')

        try:
            # print('try:')
            logger.info("Starting scheduler...")  # ; print('logger.info("Starting scheduler...")')
            scheduler.start()  # ; print('scheduler.start()')
        except KeyboardInterrupt:
            # print("KeyboardInterrupt")
            logger.info("Stopping scheduler...")  # ; print('logger.info("Stopping scheduler...")')
            scheduler.shutdown()  # ; print('scheduler.shutdown()')
            logger.info("Scheduler shut down successfully!")  # print('logger.info('Scheduler shutdown successfully!')')
