from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:article_id>/', views.news_detail, name='news_detail'),
    path('search/', views.news_search, name='news_search'),
    path('create/', views.news_create, name='news_create'),  # Добавлено
    path('<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
