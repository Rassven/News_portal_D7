from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView, DateDetailView, CreateView, UpdateView
from .models import Article
from datetime import datetime
from .filters import ArticlesFilter
from .forms import ArticleForm, OtherForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
# D5
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
# D6.4. Создание списка рассылок
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from .models import Subscription, Category
# D7.4
from django.http import HttpResponse
from django.views import View
from .tasks import hello, complete_order
from datetime import timedelta
from django.shortcuts import redirect

from .tasks import mailing, notify


class StartView(TemplateView):
    template_name = 'start.html'


class ArticleList(ListView):
    model = Article
    ordering = 'pub_time'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticlesFilter(self.request.GET, queryset)  # Instance attribute filterset defined outside __init__
        return self.filterset.qs  # Возвращаем из функции отфильтрованный список статей

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class AboutArticle(DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'


# лучшая статья
class BestArticle(ListView):
    model = Article
    # queryset = Article.objects.all().order_by('-rating').first()
    queryset = Article.objects.order_by('-rating').first()  # set to '-rating'
    template_name = 'best_article.html'
    context_object_name = 'article'


class SearchArticle(ListView):
    model = Article
    ordering = 'pub_time'
    # queryset = Article.objects.filter(category=1)  # только новости
    template_name = 'search.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticlesFilter(self.request.GET, queryset)  # Instance attribute filterset defined outside __init__
        return self.filterset.qs  # Возвращаем из функции отфильтрованный список статей

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class TestArticle(TemplateView):
    model = Article
    template_name = 'test.html'
    context_object_name = 'articles'


def create_article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect('/articles/')
            return HttpResponseRedirect('/portal/')

    return render(request, 'article_edit.html', {'form': form})


# class ArticleCreate(LoginRequiredMixin, CreateView):
class ArticleCreate(PermissionRequiredMixin, CreateView):
    # raise_exception = True
    permission_required = ('simpleapp.add_article',)
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'


# class ArticleUpdate(LoginRequiredMixin, UpdateView):
class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    # raise_exception = True
    permission_required = ('simpleapp.change_article',)
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'


# class ArticleDelete(LoginRequiredMixin, DeleteView):
class ArticleDelete(PermissionRequiredMixin, DeleteView):
    # raise_exception = True
    permission_required = ('simpleapp.delete_article',)
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('Article_list')


class AllNews(ListView):
    model = Article
    # ordering = 'pub_time'
    queryset = Article.objects.filter(category=2)  # только новости (2)
    template_name = 'all_news.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticlesFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AllArticles(ListView):
    model = Article
    # ordering = 'pub_time'
    queryset = Article.objects.filter(category=1)  # только статьи (1)
    template_name = 'all_articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticlesFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# class NewsCreate(LoginRequiredMixin, CreateView):
class NewsCreate(PermissionRequiredMixin, CreateView):
    # raise_exception = True
    permission_required = ('simpleapp.add_article',)
    form_class = OtherForm
    model = Article
    template_name = 'news_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.category_id = 1
        notify(artid=article.id, view_name='News_create')
        return super().form_valid(form)


# class ArticlesCreate(LoginRequiredMixin, CreateView):
class ArticlesCreate(PermissionRequiredMixin, CreateView):
    # raise_exception = True
    permission_required = ('simpleapp.add_article',)
    form_class = OtherForm
    model = Article
    template_name = 'article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.category_id = 3
        notify(artid=article.id, view_name='Articles_create')
        return super().form_valid(form)


# D6.4. Создание списка рассылок
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
