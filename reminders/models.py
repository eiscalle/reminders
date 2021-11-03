from celery.result import AsyncResult
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class ReminderStatuses(models.TextChoices):
    init = 'init', 'Готово к отправке'
    sent = 'sent', 'Отправлено'
    cancelled = 'cancelled', 'Отменено'
    error = 'error', 'Ошибка'


class Reminder(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255, default='')
    description = models.TextField(verbose_name='Описание', default='')
    place = models.CharField(verbose_name='Место', max_length=255, default='')
    users = models.ManyToManyField(verbose_name='Участники', to=User, related_name='+', blank=True)
    status = models.CharField(verbose_name='Статус', choices=ReminderStatuses.choices, default=ReminderStatuses.init,
                              max_length=9)
    author = models.ForeignKey(verbose_name='Автор', to=User, on_delete=models.CASCADE, related_name='reminders')

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    publish_at = models.DateTimeField(verbose_name='Дата и время напоминания')

    task_id = models.CharField(verbose_name='ID задачи в Celery', max_length=255, default='')

    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'

    def __str__(self):
        return self.title

    def revoke_task(self):
        if self.task_id:
            AsyncResult(self.task_id).revoke()
