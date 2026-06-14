from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, User
from django.db.models import Q

def news_list(request):
    articles = Article.objects.filter(status='published')
    return render(request, 'news_list.html', {'articles': articles})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('news_list')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('news_list')

@login_required
def my_articles(request):
    articles = request.user.articles.all()
    return render(request, 'my_articles.html', {'articles': articles})

@login_required
def create_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Article.objects.create(
            title=title,
            content=content,
            author=request.user,
            status='moderation'
        )
        messages.success(request, 'Статья отправлена на модерацию')
        return redirect('my_articles')
    return render(request, 'create_article.html')

@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if article.status != 'rejected':
        messages.error(request, 'Редактировать можно только отклонённые статьи')
        return redirect('my_articles')
    
    if request.method == 'POST':
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.status = 'moderation'
        article.rejection_reason = None
        article.save()
        messages.success(request, 'Статья отправлена на повторную модерацию')
        return redirect('my_articles')
    
    return render(request, 'edit_article.html', {'article': article})

@login_required
def moderation_list(request):
    if request.user.role != 'moderator':
        messages.error(request, 'Доступ запрещён')
        return redirect('news_list')
    articles = Article.objects.filter(status='moderation')
    return render(request, 'moderation_list.html', {'articles': articles})

@login_required
def moderate_article(request, pk):
    if request.user.role != 'moderator':
        messages.error(request, 'Доступ запрещён')
        return redirect('news_list')
    
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'approve':
            article.publish()
            messages.success(request, 'Статья опубликована')
        elif action == 'reject':
            article.status = 'rejected'
            article.rejection_reason = request.POST.get('reason', '')
            article.save()
            messages.success(request, 'Статья отклонена')
        return redirect('moderation_list')
    
    return render(request, 'moderate_article.html', {'article': article})