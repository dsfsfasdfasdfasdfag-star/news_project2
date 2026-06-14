from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('author', 'Автор'),
        ('moderator', 'Модератор'),
    ]
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='author',
        verbose_name="Роль"
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('moderation', 'На модерации'),
        ('rejected', 'Отклонена'),
        ('published', 'Опубликована'),
    ]

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст статьи")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='articles',
        verbose_name="Автор"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name="Статус"
    )
    rejection_reason = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Причина отклонения"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

    def publish(self):
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()