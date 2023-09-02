from django.contrib import admin
from .models import Category, Article


# D11.5
# напишем уже знакомую нам функцию обнуления товара на складе (action не появляется... ???)
def nullfy_rating(modeladmin, request, queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из них
    # это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили
    # галочками.
    queryset.update(rating=0)
    nullfy_rating.short_description = 'Обнулить рейтинги'  # описание для более понятного представления в админ панеле
    # задаётся, как будто это объект


# D11.5 создаём новый класс для представления товаров в админке
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rating', 'pub_time', 'on_stock')
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in Article._meta.get_fields()]  # генерируем список имён всех полей для более
    # красивого отображения
    # list_filter = ('name', 'rating', 'category')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('name', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_rating]  # добавляем действия в список


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
# admin.site.unregister(Product) # разрегистрируем наши товары
