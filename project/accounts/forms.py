from project.mconfig import config
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Добавление в группы при регистрации
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
# D6.2 отправка писем
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives  # текстовое сообщение и приложенная версия с HTML-разметкой
from django.core.mail import mail_managers, mail_admins


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", )


# Добавление в группы при регистрации
class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)

        # D6.2
        # send_mail(subject='Добро пожаловать на портал новостей!',
        #           message=f'{user.username}, вы успешно зарегистрировались! ({request.get_host()})',
        #           from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
        #           recipient_list=[user.email], )

        # D6.2
        subject = 'Добро пожаловать на портал новостей!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте (host: ({request.get_host()}))!'
        html = (f'<b>{user.username}</b>, вы успешно зарегистрировались на '
                f'<a href="http://127.0.0.1:8000/portal">сайте</a> (host: {request.get_host()}, '
                f'user.date_joined: {user.date_joined})!')
        # msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[user.email])
        msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[config['ctrl_mail'], ])  # !+email
        msg.attach_alternative(html, "text/html")
        msg.send()

        mail_managers(subject='[M] Новый пользователь!', message=f'[M] {user.username} в {user.date_joined}  '
                                                                 f'зарегистрировался на сайте.')
        mail_admins(subject='[A] Новый пользователь!', message=f'[A] {user.username} в {user.date_joined}  '
                                                               f'зарегистрировался на сайте.')
        # html_message=
        return user

# add TestUser@mail.ru + NfNB7D_yyeD0

