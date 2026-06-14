from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Для авторов
    path('my-articles/', views.my_articles, name='my_articles'),
    path('create-article/', views.create_article, name='create_article'),
    path('edit-article/<int:pk>/', views.edit_article, name='edit_article'),
    
    # Для модераторов
    path('moderation/', views.moderation_list, name='moderation_list'),
    path('moderate/<int:pk>/', views.moderate_article, name='moderate_article'),
]