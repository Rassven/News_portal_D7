# D6.4 ... переделаем под рассылку писем
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

# Базовые
from project.mconfig import config
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article

# # D6.4 ... переделаем под рассылку писем
# @receiver(post_save, sender=Article)
# def article_created(instance, **kwargs):
#     print('Создана статья', instance)

# Еще сигналы (django.db.models.signals./ИМЯ/):
# pre_save, post_save — вызываются до и после вызова save() метода модели;
# pre_delete и post_delete — вызываются до и после вызова delete() метода модели или набора объектов (queryset);
# m2m_changed — вызывается, когда ManyToManyField в модели изменяется;
# request_started и request_finished — вызывается перед и после обработки HTTP-запроса.
# Документация по сигналам: https://docs.djangoproject.com/en/4.0/ref/signals/


# # D6.4 ... переделаем под рассылку писем
@receiver(post_save, sender=Article)
def article_created(instance, created, **kwargs):
    if not created:
        return
    # print('Creation!')
    emails = User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True)
    subject = f'Новая статья в категории {instance.category}'
    text_content = (
        f'Статья: {instance.name}\n'
        f'Опубликована: {instance.pub_time}\n\n'
        f'Кратко: {instance.text[:30]}'
        f'Полный текст: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Статья: {instance.name}<br>'
        f'Опубликована: {instance.pub_time}<br><br>'
        f'Кратко: {instance.text[:30]}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">Читать полностью</a>'
    )
    # Ссылка из почты на статью не работает!!!
    print('Sending emails...')
    for email in emails:
        # print(email)
        msg = EmailMultiAlternatives(subject, text_content, None, [config['ctrl_mail'], ])  # + email !
        msg.attach_alternative(html_content, "text/html")
        msg.send()
