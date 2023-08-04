from celery import shared_task
import time
from .models import Article, Category
from django.contrib.auth.models import User

from project.mconfig import config
from django.urls import reverse


@shared_task
def mailing():
    cat_list = Category.objects.values_list('id', 'name')
    print('Run subs_list job')
    for cat_id, cat_name in cat_list:  # Перебор категорий и поиск подписчиков (их email)
        emails = User.objects.filter(subscriptions__category=cat_id).values_list('email', flat=True)
        if emails:  # Есть подписчики, поиск статей по условию.
            print('Find', emails.count(), 'subscriber/s')
            last_time = datetime.now() - timedelta(weeks=1, days=0)
            art_list = Article.objects.filter(
                category=cat_id, pub_time__gte=last_time
            ).values_list('id', 'pub_time', 'name', 'text', 'category')
            if art_list:  # Статьи найдены
                print('Find:', art_list.count(), 'article/s')
                # Сборка содержимого для отправки
                subject = f'Новые статьи в категории "{cat_name}" за неделю:'
                text_content_message = [];
                html_content_message = []
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
                for email in emails:
                    msg = EmailMultiAlternatives(subject, text_content, None, [config['ctrl_mail'], ])  # + email !
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
            else:
                print('Not find')


@shared_task
def notify(artid, view_name):
    article = Article.objects.get(pk=artid)
    cat_id = article.category_id
    last_time = datetime.now() - timedelta(weeks=1, days=0)
    art_list = Article.objects.filter(
        category=cat_id, pub_time__gte=last_time
    ).values_list('id', 'pub_time', 'name', 'text', 'category')
    if art_list:  # Статьи найдены
        print('Find:', art_list.count(), 'article/s')
        # Сборка содержимого для отправки
        subject = f'Новые статьи в категории "{cat_name}" за неделю:'
        text_content_message = []
        html_content_message = []
        for art_id, art_time, art_name, art_text, art_cat in art_list:
            a_link = reverse(view_name, args=(artid, ))  # args=[art_id] -списком вместо кортежа
            text_content_message.append(
                f'Статья: {art_name} (опубликована: {str(art_time)[:16]})\n'
                f'Кратко: {art_text[:30]}...  '
                f'Полный текст: {a_link}'
            )
            html_content_message.append(
                f'({str(art_time)[:16]})   "<i>{art_name}</i>"<br>'
                f'<b>Кратко:</b> {art_text[:30]}...   '
                f'(<a href="{a_link}">Читать полностью</a>)'
            )
        text_content = '/n/n'.join(text_content_message)  # print(text_content)
        html_content = '<br><br>'.join(html_content_message)  # print(html_content)
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [config['ctrl_mail'], ])  # + email !
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    else:
        print('Not find')

