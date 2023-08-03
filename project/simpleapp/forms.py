from django import forms
from .models import Article
from django.core.exceptions import ValidationError


class ArticleForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Article
        # fields = '__all__'  # Так делать не стоит, чтобы не выводились поля запрещенные для редактирования
        fields = ['name', 'category', 'rating', 'text', ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name is not None and len(name) < 10:
            raise ValidationError({"name": "Название не может быть менее 10 символов."})
        text = cleaned_data.get("text")
        if text == name:
            raise ValidationError("Текст не должен повторять название.")
        if name[0].islower():
            raise ValidationError("Название должно начинаться с заглавной буквы")
        return cleaned_data


class OtherForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Article
        fields = ['name', 'text']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name is not None and len(name) < 10:
            raise ValidationError({"name": "Название не может быть менее 10 символов."})
        text = cleaned_data.get("text")
        if text == name:
            raise ValidationError("Текст не должен повторять название.")
        if name[0].islower():
            raise ValidationError("Название должно начинаться с заглавной буквы")
        return cleaned_data


# Вот так выглядело бы создание формы при написании его без использования Meta-класса.

# class ProductForm(forms.Form):
#     name = forms.CharField(label='Name')
#     description = forms.CharField(label='Description')
#     quantity = forms.IntegerField(label='Quantity')
#     category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all(), )
#     price = forms.FloatField(label='Price')
