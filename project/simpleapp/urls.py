from django.urls import path
# Импортируем созданное нами представление
from .views import ArticleList, AboutArticle, BestArticle, SearchArticle, TestArticle, create_article, StartView
from .views import ArticleCreate, ArticleUpdate, ArticleDelete, AllNews, AllArticles, NewsCreate, ArticlesCreate
# D6.4. Создание списка рассылок
from .views import subscriptions
# D8.3 кэширование
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', ArticleList.as_view(), name='Article_list'),
    path('<int:pk>', AboutArticle.as_view(), name='About_article'),
    path('start', StartView.as_view()),
    path('best', BestArticle.as_view()),
    path('search', SearchArticle.as_view()),
    path('test', cache_page(1*60)(TestArticle.as_view()),), # добавлено кэширование на 1 минуту.
    # path('create/', create_article, name='Article_create')
    path('article/create/', ArticleCreate.as_view(), name='Article_create'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('allnews/', AllNews.as_view(), name='news_only'),
    path('allarticles/', AllArticles.as_view(), name='articles_only'),
    path('articles/create/', ArticlesCreate.as_view(), name='Articles_create'),
    path('news/create/', NewsCreate.as_view(), name='News_create'),
    # D6.4
    path('subscriptions/', subscriptions, name='subscriptions'),
]
