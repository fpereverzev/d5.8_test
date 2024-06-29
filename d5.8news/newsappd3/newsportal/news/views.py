from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import Article
from .forms import ArticleForm, NewsForm
from .filters import NewsFilter


@login_required
@permission_required('newsportal.add_article', raise_exception=True)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect('news_detail', article_id=news.id)
    else:
        form = NewsForm()
    return render(request, 'news_create.html', {'form': form})


def news_list(request):
    articles = Article.objects.filter(post_type='news').order_by('-published_date')
    paginator = Paginator(articles, 10)  # Пагинация: 10 статей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_list.html', {'page_obj': page_obj})


def news_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'news_detail.html', {'article': article})


def news_search(request):
    article_list = Article.objects.all()
    news_filter = NewsFilter(request.GET, queryset=article_list)
    paginator = Paginator(news_filter.qs, 10)  # Пагинация: 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_search.html', {'filter': news_filter, 'page_obj': page_obj})


# Представления для новостей

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    form_class = NewsForm
    template_name = 'news/news_form.html'
    permission_required = 'newsportal.add_article'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'news'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news_list')


class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = NewsForm
    template_name = 'news/news_form.html'
    permission_required = 'newsportal.change_article'

    def get_success_url(self):
        return reverse_lazy('news_list')


class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'newsportal.delete_article'


# Представления для статей

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/article_form.html'
    permission_required = 'newsportal.add_article'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'article'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news_list')


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/article_form.html'
    permission_required = 'newsportal.change_article'

    def get_success_url(self):
        return reverse_lazy('news_list')


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')
    permission_required = 'newsportal.delete_article'
